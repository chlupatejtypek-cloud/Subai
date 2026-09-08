"""Reproducible authored FFmpeg edit: real hook, separate zoom, subtle still motion."""
from pathlib import Path
import subprocess,json,math,concurrent.futures
p=Path(__file__).resolve().parent;out=p/'output';out.mkdir(exist_ok=True);fps=30;end=50.1
# Frame boundaries: exact30fps, no overlap/drift; repeated identical art is intentional continuity.
plan=[(0,2.8,'01-cafe-fixed','Real cafe farewell'),(2.8,6.4,'02-walk-home','Post-chat worry'),(6.4,9.2,'03-cafe-chat','Liking gap setup'),(9.2,12.8,'04-study','Independent ratings'),(12.8,16.8,'05-other-view','Reported versus estimated liking'),(16.8,20.2,'02-walk-home','Internal commentary'),(20.2,23.4,'05-other-view','Actual conversation'),(23.4,26.2,'06-film-critic','Brief situational joke'),(26.2,29.6,'07-not-everyone','Not universal'),(29.6,32.6,'04-study','Average not individual verdict'),(32.6,36.2,'08-journal','Separate fact and guess'),(36.2,40.4,'03-cafe-chat','Observation and interpretation UI'),(40.4,44.6,'10-phone','Optional low-pressure message'),(44.6,47.3,'09-next-day','No perfection required'),(47.3,50.1,'01-cafe-fixed','Closing perspective')]
(p/'storyboard.json').write_text(json.dumps({'end':end,'fps':fps,'distinct_used_illustrations':10,'generated_images':10,'max_illustration_hold_seconds':max(b-a for a,b,_,_ in plan),'scenes':[{'start':a,'end':b,'source':s,'purpose':why} for a,b,s,why in plan]},indent=2))
def render(pair):
 i,(a,b,src,why)=pair;n=round(b*fps)-round(a*fps);f=out/f'scene-{i:02}.mp4';base=['ffmpeg','-y','-v','error','-threads','1']
 if i==0:
  # Real generated image-to-video plus explicit independent100→105→100% zoom over first1.25s.
  vf="trim=duration=1.5,setpts=PTS*28/15,fps=30,tpad=stop_mode=clone:stop_duration=0.2,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,zoompan=z='1+0.05*max(0,1-abs(on-15)/15)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30"
  cmd=base+['-i',str(p/'assets/hook.mp4')]
 else:
  # Increase working raster for smooth subpixel drift instead of visible integer-pixel jitter.
  z=f'1.018+0.012*on/{max(n-1,1)}' if i%2 else f'1.03-0.012*on/{max(n-1,1)}'
  vf=f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s=1080x1920:fps=30"
  cmd=base+['-i',str(p/'assets'/f'{src}.png')]
 subprocess.run(cmd+['-vf',vf,'-frames:v',str(n),'-an','-c:v','libx264','-preset','fast','-crf','21','-threads','1','-pix_fmt','yuv420p',str(f)],check=True)
 print('Rendered',i,why,flush=True);return f
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:files=list(pool.map(render,enumerate(plan)))
(out/'concat.txt').write_text(''.join("file '"+str(f)+"'\n" for f in files))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(out/'concat.txt'),'-c','copy',str(out/'picture.mp4')],check=True)
# UI is separately authored RGBA animation: actual evidence comparison and fact/guess state change.
subprocess.run(['python',str(p/'render-ui.py')],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(out/'picture.mp4'),'-i',str(out/'ui.mov'),'-i',str(p/'audio/final-mix.wav'),'-filter_complex',f"[0:v]gblur=sigma=8:enable='between(t,9.5,16.8)+between(t,34,40.4)'[bg];[bg][1:v]overlay=0:0[com];[com]ass={p/'captions.ass'}:fontsdir={p/'assets'}[v]",'-map','[v]','-map','2:a','-t',str(end),'-c:v','libx264','-preset','fast','-crf','21','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'liking-gap-final.mp4')],check=True)
print('FINAL',out/'liking-gap-final.mp4',flush=True)
