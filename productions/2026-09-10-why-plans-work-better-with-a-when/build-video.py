"""Reproducible authored FFmpeg edit: real hook, separate zoom, subtle still motion."""
from pathlib import Path
import subprocess,json,math,concurrent.futures
p=Path(__file__).resolve().parent;out=p/'output';out.mkdir(exist_ok=True);fps=30;end=48.3
# Frame boundaries: exact30fps, no overlap/drift; repeated identical art is intentional continuity.
plan=[(0,4.1,'01-calendar','Real sticky-note placement and separate zoom'),(4.1,6.6,'02-vague','Vague walking goal'),(6.6,9.7,'10-adjust','Undecided starting moment'),(9.7,12.8,'04-clinic','Workplace trial context'),(12.8,15.5,'03-mail','Date/time prompt'),(15.5,18.3,'05-evidence','Actual uptake comparison'),(18.3,21,'04-clinic','Modest effect not magic'),(21,24.7,'02-vague','Implementation intentions explanation'),(24.7,28.3,'06-sink','Concrete cue'),(28.3,31,'07-shoes','Specified action'),(31,34.7,'08-walk','Follow-through not negotiation'),(34.7,38.7,'05-evidence','Noticeable and feasible'),(38.7,42.1,'09-rain','Real barriers'),(42.1,45,'10-adjust','Revise when circumstances change'),(45,48.3,'08-walk','Cue-to-action payoff')]
(p/'storyboard.json').write_text(json.dumps({'end':end,'fps':fps,'distinct_used_illustrations':10,'generated_images':10,'max_illustration_hold_seconds':max(b-a for a,b,_,_ in plan),'scenes':[{'start':a,'end':b,'source':s,'purpose':why} for a,b,s,why in plan]},indent=2))
def render(pair):
 i,(a,b,src,why)=pair;n=round(b*fps)-round(a*fps);f=out/f'scene-{i:02}.mp4';base=['ffmpeg','-y','-v','error','-threads','1']
 if i==0:
  # Real generated image-to-video plus explicit independent100→105→100% zoom over first1.25s.
  vf="trim=duration=4,setpts=PTS,fps=30,tpad=stop_mode=clone:stop_duration=0.2,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,zoompan=z='1+0.05*max(0,1-abs(on-15)/15)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30"
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
if not (out/'ui.mov').exists(): subprocess.run(['python',str(p/'render-ui.py')],check=True)
# Alpha fades crossfade selective blurred background without expensive per-pixel time expressions.
fc=f"[0:v]split[sharp][b];[b]gblur=sigma=9,format=yuva420p,split[b1][b2];[b1]fade=t=in:st=13.2:d=0.4:alpha=1,fade=t=out:st=19.2:d=0.4:alpha=1[f1];[b2]fade=t=in:st=25.4:d=0.4:alpha=1,fade=t=out:st=31.8:d=0.4:alpha=1[f2];[sharp][f1]overlay[tmp];[tmp][f2]overlay[bg];[bg][1:v]overlay=0:0[com];[com]ass={p/'captions.ass'}:fontsdir={p/'assets'}[v]"
subprocess.run(['ffmpeg','-y','-v','error','-filter_complex_threads','2','-i',str(out/'picture.mp4'),'-i',str(out/'ui.mov'),'-i',str(p/'audio/final-mix.wav'),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',str(end),'-c:v','libx264','-preset','fast','-crf','21','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'plan-trigger-final.mp4')],check=True)
print('FINAL',out/'plan-trigger-final.mp4',flush=True)
