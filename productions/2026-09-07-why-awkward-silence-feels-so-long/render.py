#!/usr/bin/env python3
"""Reproducible edit. Images are original generated art; Fish alignment is provider-native."""
import json, subprocess, wave, math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
P=Path(__file__).resolve().parent
O=P/'output';O.mkdir(exist_ok=True)
FPS=30; DURATION=json.loads((P/'timeline.json').read_text())['duration']
# Times derived from native Fish word alignment. Revisited detail shots are intentional.
SCENES=[(x['image'],x['start'],x['end'],x['motion']) for x in json.loads((P/'timeline.json').read_text())['scenes']]
def run(c):subprocess.run(c,check=True)
def segment(item):
 i,(src,start,end,motion)=item;frames=round(end*FPS)-round(start*FPS)
 n=max(frames-1,1); z=f'1+0.04*on/{n}';x='iw/2-iw/zoom/2';y='ih/2-ih/zoom/2'
 if motion=='pull':z=f'1.04-0.04*on/{n}'
 if motion=='pan':z='1.06';x=f'(iw-iw/zoom)*on/{n}'
 if motion=='detail':z=f'1.26+0.04*on/{n}';y='(ih-ih/zoom)*0.3'
 vf=f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s=1080x1920:fps=30,setsar=1"
 run(['ffmpeg','-y','-v','error','-i',str(P/src),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','19','-threads','2','-pix_fmt','yuv420p',str(O/f'{i:02}.mp4')]);print('scene',i,'done',flush=True)
def sfx():
 sr=48000;audio=np.zeros(round(DURATION*sr));rng=np.random.default_rng(9)
 cues=[(.02,'whoosh',.017,'opening cafe reveal'),(SCENES[6][1]+.08,'bell',.023,'connected speech bubbles'),(SCENES[7][1]+.08,'tick',.012,'connection gap'),(SCENES[9][1]+.12,'ceramic',.027,'friend and cup'),(SCENES[11][1]+.08,'brush',.014,'pause and hourglass'),(SCENES[13][1]+.09,'bell',.021,'friendly follow-up')]
 for at,kind,gain,reason in cues:
  length=.28 if kind in ('whoosh','brush') else .23;n=int(length*sr);t=np.arange(n)/sr
  if kind=='whoosh':v=np.convolve(rng.normal(size=n),np.ones(30)/30,mode='same')*np.sin(np.pi*t/length)**2
  elif kind=='brush':v=np.convolve(rng.normal(size=n),np.ones(9)/9,mode='same')*np.exp(-t*21)*(1-np.exp(-t*90))
  elif kind=='ceramic':v=(np.sin(2*np.pi*1371*t)+.47*np.sin(2*np.pi*2249*t)+.22*np.sin(2*np.pi*3307*t))*np.exp(-t*27)*(1-np.exp(-t*1600))
  elif kind=='tick':v=(np.sin(2*np.pi*720*t)+.3*np.sin(2*np.pi*1430*t))*np.exp(-t*70)*(1-np.exp(-t*1800))
  else:v=(np.sin(2*np.pi*523.25*t)+.25*np.sin(2*np.pi*1046.5*t))*np.exp(-t*17)*(1-np.exp(-t*100))
  v*=gain/(np.max(np.abs(v))+1e-9);j=int(at*sr);m=min(n,len(audio)-j)
  if m>0:audio[j:j+m]+=v[:m]
 with wave.open(str(P/'audio/sfx.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((audio*32767).astype('<i2').tobytes())
 (P/'audio/sfx.json').write_text(json.dumps([{'at':a,'kind':k,'peak_amplitude':g,'motivation':r,'origin':'original procedurally synthesized effect'} for a,k,g,r in cues],indent=2)+'\n')
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(segment,enumerate(SCENES)))
 (O/'concat.txt').write_text(''.join(f"file '{O/f'{i:02}.mp4'}'\n" for i in range(len(SCENES))))
 run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(O/'concat.txt'),'-c','copy',str(O/'silent.mp4')]);sfx()
 run(['ffmpeg','-y','-v','error','-i',str(O/'silent.mp4'),'-i',str(P/'audio/narration.wav'),'-i',str(P/'audio/sfx.wav'),'-filter_complex',f"[0:v]ass={P/'captions.ass'}[v];[1:a]loudnorm=I=-16:TP=-2.0:LRA=9[voice];[voice][2:a]amix=inputs=2:normalize=0,alimiter=limit=0.94:level=false[a]",'-map','[v]','-map','[a]','-t',str(DURATION),'-c:v','libx264','-preset','fast','-crf','19','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(O/'awkward-silence-final.mp4')]);print('FINAL_READY',flush=True)
