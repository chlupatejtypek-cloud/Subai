"""Reproducible authored FFmpeg edit: real hook, separate zoom, subtle still motion."""
from pathlib import Path
import subprocess,json,math,concurrent.futures
p=Path(__file__).resolve().parent;out=p/'output';out.mkdir(exist_ok=True);fps=30;end=48.3
# Frame boundaries: exact30fps, no overlap/drift; repeated identical art is intentional continuity.
plan=[(0,3,'01-counter','Real coin motion'),(3,6.2,'02-gift','Hypothetical windfall'),(6.2,9.2,'03-add','Gain framing'),(9.2,12.2,'04-larger-start','Larger starting point'),(12.2,15.4,'05-subtract','Same final amount'),(15.4,18.6,'07-study','Original hypothetical choice study'),(18.6,22.2,'06-two-wallets','Identical final prospects'),(22.2,25.2,'08-reference','Reference dependence'),(25.2,28.4,'04-larger-start','Starting point not just total'),(28.4,32.5,'09-headlines','Calculator versus headlines joke'),(32.5,36.5,'05-subtract','No universal loss multiplier'),(36.5,40.4,'10-check','Compare actual terms'),(40.4,44.5,'06-two-wallets','Probabilities and costs'),(44.5,48.3,'01-counter','Closing same-deal perspective')]
(p/'storyboard.json').write_text(json.dumps({'end':end,'fps':fps,'distinct_used_illustrations':10,'generated_images':10,'max_illustration_hold_seconds':max(b-a for a,b,_,_ in plan),'scenes':[{'start':a,'end':b,'source':s,'purpose':why} for a,b,s,why in plan]},indent=2))
def render(pair):
 i,(a,b,src,why)=pair;n=round(b*fps)-round(a*fps);f=out/f'scene-{i:02}.mp4';base=['ffmpeg','-y','-v','error','-threads','1']
 if i==0:
  # Real generated image-to-video plus explicit independent100→105→100% zoom over first1.25s.
  vf="trim=duration=3,setpts=PTS,fps=30,tpad=stop_mode=clone:stop_duration=0.2,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,zoompan=z='1+0.05*max(0,1-abs(on-15)/15)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30"
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
# Blur is crossfaded rather than switched on/off. Only irrelevant illustration background is blurred.
blur="max(if(between(T,6.2,15.3),min(1,min((T-6.2)/0.4,(15.3-T)/0.4)),0),if(between(T,38,44.4),min(1,min((T-38)/0.4,(44.4-T)/0.4)),0))"
fc=f"[0:v]split[sharp][b];[b]gblur=sigma=10[soft];[sharp][soft]blend=all_expr='A*(1-({blur}))+B*({blur})'[bg];[bg][1:v]overlay=0:0[com];[com]ass={p/'captions.ass'}:fontsdir={p/'assets'}[v]"
subprocess.run(['ffmpeg','-y','-v','error','-i',str(out/'picture.mp4'),'-i',str(out/'ui.mov'),'-i',str(p/'audio/final-mix.wav'),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',str(end),'-c:v','libx264','-preset','fast','-crf','21','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'reference-frame-final.mp4')],check=True)
print('FINAL',out/'reference-frame-final.mp4',flush=True)
