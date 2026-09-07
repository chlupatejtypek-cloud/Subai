#!/usr/bin/env python3
from __future__ import annotations
import subprocess
from pathlib import Path
R=Path(__file__).resolve().parent; FPS=30; DUR=4.0
# Only clips that passed sampled first/middle/last creative QC.
AGNES={1,6,7,9}
MOTION={2:'pull',3:'pan_lr',4:'push',5:'pull',8:'pan_rl',10:'push'}
def run(c): print('+',' '.join(map(str,c))); subprocess.run(c,check=True)
def make_segments():
 d=R/'output-v2/segments'; d.mkdir(parents=True,exist_ok=True)
 for i in range(1,11):
  out=d/f'{i:02d}.mp4'
  if i in AGNES:
   src=R/f'visuals-v2/scene-{i:02d}-agnes.mp4'
   base=f'scale=1080:2006:flags=lanczos,crop=1080:1920:0:43,fps={FPS}'
   if i==1:
    # Quick 5% punch-in over ~0.23 s, then return to 100% through the hook.
    z="if(lte(on,7),1+0.05*on/7,1.05-0.05*(on-7)/112)"
    vf=base+f",zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps={FPS},trim=duration=4,setpts=PTS-STARTPTS"
   else: vf=base+',trim=duration=4,setpts=PTS-STARTPTS'
   run(['ffmpeg','-y','-loglevel','error','-i',str(src),'-an','-vf',vf,'-frames:v','120','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',str(out)])
  else:
   src=R/f'visuals-v2/scene-{i:02d}-clean.png'; m=MOTION[i]; n=119
   if m=='push': z=f'1+0.035*on/{n}'; x='iw/2-iw/zoom/2'
   elif m=='pull': z=f'1.035-0.035*on/{n}'; x='iw/2-iw/zoom/2'
   elif m=='pan_lr': z='1.07'; x=f'(iw-iw/zoom)*on/{n}'
   else: z='1.07'; x=f'(iw-iw/zoom)*(1-on/{n})'
   vf=f"scale=1080:1935:flags=lanczos,zoompan=z='{z}':x='{x}':y='ih/2-ih/zoom/2':d=120:s=1080x1920:fps=30,trim=duration=4,setsar=1"
   run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',str(src),'-an','-vf',vf,'-frames:v','120','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',str(out)])
 concat=R/'output-v2/concat.txt'; concat.write_text(''.join(f"file '{(d/f'{i:02d}.mp4').as_posix()}'\n" for i in range(1,11)))
 run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(R/'output-v2/silent.mp4')])
def make_sfx():
 s=R/'sfx'; s.mkdir(exist_ok=True)
 run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','anoisesrc=d=0.55:c=white:r=48000:a=0.18','-af','highpass=f=450,lowpass=f=4200,afade=t=in:d=0.06,afade=t=out:st=0.12:d=0.43,volume=0.28',str(s/'whoosh.wav')])
 run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','sine=f=1350:d=0.10:r=48000','-af','afade=t=out:st=0.015:d=0.085,volume=0.11',str(s/'click.wav')])
 run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','sine=f=92:d=0.48:r=48000','-af','afade=t=out:st=0.03:d=0.45,volume=0.10',str(s/'hit.wav')])
 run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','sine=f=740:d=0.70:r=48000','-af','afade=t=in:d=0.02,afade=t=out:st=0.12:d=0.58,volume=0.07',str(s/'chime.wav')])
 # Keep effects subtle under dialogue; Fish expression tags provide the vocal performance.
 run(['ffmpeg','-y','-loglevel','error','-i',str(R/'audio/dialogue-v2.wav'),'-i',str(s/'whoosh.wav'),'-i',str(s/'click.wav'),'-i',str(s/'hit.wav'),'-i',str(s/'chime.wav'),'-filter_complex',
      '[0:a]loudnorm=I=-16:TP=-2:LRA=7,apad=pad_dur=40[v];[1:a]adelay=0|0[w];[2:a]adelay=12000|12000[c];[3:a]adelay=20000|20000[h];[4:a]adelay=35400|35400[q];[v][w][c][h][q]amix=inputs=5:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=8[m]', '-map','[m]','-t','40','-ar','48000','-ac','1','-c:a','pcm_s16le',str(R/'audio/dialogue-v2-mix.wav')])
def final():
 silent=R/'output-v2/silent.mp4'; cap=R/'captions-v2.ass'; a=R/'audio/dialogue-v2-mix.wav'; p720=R/'output-v2/captioned-720.mp4'; out=R/'output-v2/procrastination-relief-v2.mp4'
 run(['ffmpeg','-y','-loglevel','error','-i',str(silent),'-i',str(a),'-vf',f'scale=720:1280:flags=lanczos,ass={cap}','-map','0:v','-map','1:a','-c:v','libx264','-preset','ultrafast','-crf','18','-threads','1','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','40',str(p720)])
 run(['ffmpeg','-y','-loglevel','error','-i',str(p720),'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','ultrafast','-crf','18','-threads','1','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(out)])
 run(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,r_frame_rate,sample_rate,channels:format=duration,size','-of','json',str(out)])
if __name__=='__main__': make_segments(); make_sfx(); final()
