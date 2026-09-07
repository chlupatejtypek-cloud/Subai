#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=json.loads((ROOT/'dialogue-v2.json').read_text())
segdir=ROOT/'audio/segments-v2'; segdir.mkdir(parents=True,exist_ok=True)

def run(c): subprocess.run(c,check=True)
for i,line in enumerate(spec,1):
    out=segdir/f'{i:02d}-{line["speaker"]}.opus'
    if not out.exists():
        run(['python3',str(ROOT.parents[1]/'tools/fish-tts-with-timestamps.py'),'--text',line['text'],'--reference-id',line['voice'],'--model','s2.1-pro-free','--format','opus','--speed','1.05','--output',str(out)])
    run(['ffmpeg','-y','-loglevel','error','-i',str(out),'-ac','1','-ar','48000','-c:a','pcm_s16le',str(out.with_suffix('.wav'))])

words=[]; pcm=[]; cursor=0.0; silence=0.07
for i,line in enumerate(spec,1):
    op=segdir/f'{i:02d}-{line["speaker"]}.opus'; wav=op.with_suffix('.wav')
    with wave.open(str(wav),'rb') as w:
        assert w.getnchannels()==1 and w.getframerate()==48000 and w.getsampwidth()==2
        raw=w.readframes(w.getnframes()); dur=w.getnframes()/48000
    data=json.loads(op.with_suffix('.opus.timestamps.json').read_text())
    chunks={}
    for c in data['alignment_chunks']:
        off=float(c.get('chunk_audio_offset_sec') or 0); segs=c.get('alignment',{}).get('segments',[])
        if len(segs)>len(chunks.get(off,[])): chunks[off]=segs
    for off,segs in sorted(chunks.items()):
        for s in segs:
            text=s['text'].strip()
            if not text or text.startswith('[') or text.endswith(']'): continue
            words.append({'text':text,'start':cursor+off+float(s['start']),'end':cursor+off+float(s['end']),'speaker':line['speaker']})
    pcm.append(raw)
    if i<len(spec): pcm.append(b'\0\0'*round(48000*silence))
    cursor += dur + (silence if i<len(spec) else 0)
with wave.open(str(ROOT/'audio/dialogue-v2.wav'),'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes(b''.join(pcm))
(ROOT/'audio/dialogue-v2.timestamps.json').write_text(json.dumps({'provider':'Fish Audio','model':'s2.1-pro-free','speed':1.05,'duration':cursor,'words':words},indent=2)+'\n')
print(f'duration={cursor:.3f} words={len(words)}')
