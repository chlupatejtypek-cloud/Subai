#!/usr/bin/env python3
"""Reproducible edit. Images are original generated art; Adam alignment is provider-native."""
import json, subprocess, wave, math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
P=Path(__file__).resolve().parent
O=P/'output';O.mkdir(exist_ok=True)
FPS=30; DURATION=38.4
# Times derived from native ElevenLabs word alignment. Revisited detail shots are intentional.
SCENES=[('01.png',0,4.95,'push'),('02.png',4.95,9.58,'pull'),('03.png',9.58,13.32,'push'),('03.png',13.32,16.86,'detail'),('02.png',16.86,23.06,'pan'),('04.png',23.06,26.99,'pull'),('05.png',26.99,32.95,'push'),('06.png',32.95,38.4,'pull')]
def run(c):subprocess.run(c,check=True)
def segment(item):
 i,(src,start,end,motion)=item;frames=round(end*FPS)-round(start*FPS)
 n=max(frames-1,1); z=f'1+0.04*on/{n}';x='iw/2-iw/zoom/2';y='ih/2-ih/zoom/2'
 if motion=='pull':z=f'1.04-0.04*on/{n}'
 if motion=='pan':z='1.06';x=f'(iw-iw/zoom)*on/{n}'
 if motion=='detail':z=f'1.26+0.04*on/{n}';y='(ih-ih/zoom)*0.3'
 vf=f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s=1080x1920:fps=30,setsar=1"
 run(['ffmpeg','-y','-v','error','-i',str(P/'visuals'/src),'-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','19','-threads','2','-pix_fmt','yuv420p',str(O/f'{i:02}.mp4')]);print('scene',i,'done',flush=True)
def sfx():
 # Original locally synthesized effects, no stock recordings/licensing or third-party assets.
 sr=48000;n=round(DURATION*sr);a=np.zeros(n);rng=np.random.default_rng(7)
 t=np.arange(int(.38*sr))/sr;noise=rng.normal(size=len(t));noise=np.convolve(noise,np.ones(12)/12,mode='same');whoosh=noise*np.sin(np.pi*t/.38)**2*.12;a[:len(t)]+=whoosh
 for start,f,d,amp in [(0.86,1250,.12,.018),(26.99,760,.15,.018)]:
  t=np.arange(int(d*sr))/sr;v=np.sin(2*np.pi*f*t)*np.exp(-t*35)*amp;idx=round(start*sr);a[idx:idx+len(v)]+=v
 with wave.open(str(P/'audio/sfx.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((a*32767).astype('<i2').tobytes())
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(segment,enumerate(SCENES)))
 (O/'concat.txt').write_text(''.join(f"file '{O/f'{i:02}.mp4'}'\n" for i in range(len(SCENES))))
 run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(O/'concat.txt'),'-c','copy',str(O/'silent.mp4')]);sfx()
 run(['ffmpeg','-y','-v','error','-i',str(O/'silent.mp4'),'-i',str(P/'audio/adam.mp3'),'-i',str(P/'audio/sfx.wav'),'-filter_complex',f"[0:v]ass={P/'captions.ass'}[v];[1:a]loudnorm=I=-16:TP=-1.5:LRA=9[voice];[voice][2:a]amix=inputs=2:normalize=0,alimiter=limit=0.94:level=false[a]",'-map','[v]','-map','[a]','-t',str(DURATION),'-c:v','libx264','-preset','fast','-crf','19','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(O/'spotlight-effect-final.mp4')]);print('FINAL_READY',flush=True)
