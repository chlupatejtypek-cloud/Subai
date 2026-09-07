#!/usr/bin/env python3
"""Shorten verified silent gaps only; preserve words, pitch and mapped timestamps."""
import json,re,subprocess,wave
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;SRC=P.parent/'audio';SPEED=1.06;RATE=48000
words=json.loads((SRC/'words.json').read_text())['words']
detection=subprocess.run(['ffmpeg','-hide_banner','-i',str(SRC/'narration.opus'),'-af','silencedetect=noise=-40dB:d=0.25','-f','null','-'],capture_output=True,text=True,check=True)
log=detection.stderr
(P/'audio/silence-detection.log').write_text(log)
silences=[(float(a),float(b)) for a,b in re.findall(r'silence_start: ([\d.]+).*?silence_end: ([\d.]+)',log,re.S)]
cuts=[]
for a,b in silences:
 if b-a<.42:continue
 # Cutting only the intersection of detected silence and a native word boundary gap.
 for left,right in zip(words,words[1:]):
  lo=max(a+.06,float(left['end'])+.035);hi=min(b-.06,float(right['start'])-.035)
  if hi<=lo:continue
  wanted=(b-a)-.28;remove=min(wanted,hi-lo)
  if remove<=.08:continue
  mid=(lo+hi)/2;start=round((mid-remove/2)*RATE)/RATE;end=round((mid+remove/2)*RATE)/RATE
  cuts.append({'start':start,'end':end,'removed_seconds':end-start,'original_silence_seconds':b-a,'retained_detected_silence_seconds':(b-a)-(end-start)});break
cuts.sort(key=lambda x:x['start'])
subprocess.run(['ffmpeg','-y','-v','error','-i',str(SRC/'narration.opus'),'-ac','1','-ar',str(RATE),'-c:a','pcm_s16le',str(P/'audio/source.wav')],check=True)
with wave.open(str(P/'audio/source.wav'),'rb') as f:audio=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy()
parts=[];cursor=0
for cut in cuts:
 a,b=round(cut['start']*RATE),round(cut['end']*RATE);parts.append(audio[cursor:a].copy());cursor=b
parts.append(audio[cursor:].copy())
# Tiny fades entirely within the retained silence, no crossfade duration drift.
for i,part in enumerate(parts):
 n=min(144,len(part))
 if i>0:part[:n]=(part[:n]*np.linspace(0,1,n)).astype('<i2')
 if i<len(parts)-1:part[-n:]=(part[-n:]*np.linspace(1,0,n)).astype('<i2')
compact=np.concatenate(parts)
with wave.open(str(P/'audio/compacted.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(compact.tobytes())
subprocess.run(['ffmpeg','-y','-v','error','-i',str(P/'audio/compacted.wav'),'-af',f'atempo={SPEED}','-c:a','pcm_s16le',str(P/'audio/narration-v2.wav')],check=True)
def remap(t):return (t-sum(max(0,min(t,c['end'])-c['start']) for c in cuts))/SPEED
out=[{'text':w['text'],'start':remap(float(w['start'])),'end':remap(float(w['end']))} for w in words]
(P/'audio/words.json').write_text(json.dumps({'words':out,'source':'native Fish timing mapped through explicit silence edit and atempo 1.06'},indent=2)+'\n')
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(P/'audio/narration-v2.wav')]))
report={'original_audio_seconds':len(audio)/RATE,'cuts':cuts,'total_silence_removed_seconds':sum(c['removed_seconds'] for c in cuts),'pitch_preserving_speed':SPEED,'new_audio_seconds':dur,'word_count':len(out),'maximum_original_detected_pause_seconds':max(b-a for a,b in silences)}
(P/'audio-edit.json').write_text(json.dumps(report,indent=2)+'\n')
# Ten distinct scenes, each used once. Old spoken boundaries remapped to the new waveform.
starts=[0,1.68,6.4,10.48,12.96,15.04,17.0512471655,20.0112471655,25.5312471655,28.9712471655]
end=round((dur+.32)*30+0.5)/30
scene_times=[remap(t) for t in starts]+[end]
(P/'timeline.json').write_text(json.dumps({'duration':end,'speed':SPEED,'scenes':[{'image':f'{i+1:02}.png','start':scene_times[i],'end':scene_times[i+1],'motion':['push','pull','pan','push','pull','pan','pull','push','pull','push'][i]} for i in range(10)]},indent=2)+'\n')
print(json.dumps(report,indent=2));print('Final timeline duration',end)
