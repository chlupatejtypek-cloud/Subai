"""Reproducible authored FFmpeg edit: real hook, separate zoom, subtle still motion."""
from pathlib import Path
import subprocess,json,math,concurrent.futures
p=Path(__file__).resolve().parent;out=p/'output';out.mkdir(exist_ok=True);fps=30;end=68.2
# Frame boundaries: exact30fps, no overlap/drift; repeated identical art is intentional continuity.
plan=[(0,3.2,'01-waiting','Animated waiting'),(3.2,5.4,'02-small-unclear','Small is not clear'),(5.4,12.333333333,'03-choices','Which physical action?'),(12.333333333,16.2,'04-cleanest-desk','Comic avoidance'),(16.2,21.4,'05-goal-action','Goal versus action'),(21.4,27.733333333,'06-questionnaire','Small experiments'),(27.733333333,31.5,'07-email-arrival','Measured submission, not motivation'),(31.5,35.4,'02-small-unclear','No magic cure'),(35.4,39.2,'05-goal-action','Keep goal, change instruction'),(39.2,45.8,'08-first-sentence','Concrete writing example'),(45.8,51.6,'09-rough-draft','Observable rough output, joke'),(51.6,56,'08-first-sentence','Continue action, not planning'),(56,61.233333333,'10-exhaustion','Limits and compassion'),(61.233333333,68.2,'05-goal-action','Resolve the opening question')]
(p/'storyboard.json').write_text(json.dumps({'end':end,'fps':fps,'distinct_used_illustrations':10,'generated_images':10,'max_illustration_hold_seconds':max(b-a for a,b,_,_ in plan),'scenes':[{'start':a,'end':b,'source':s,'purpose':why} for a,b,s,why in plan]},indent=2))
def render(pair):
 i,(a,b,src,why)=pair;n=round(b*fps)-round(a*fps);f=out/f'scene-{i:02}.mp4';base=['ffmpeg','-y','-v','error','-threads','1']
 if i==0:
  # Real generated image-to-video plus explicit independent100→105→100% zoom over first1.25s.
  vf="trim=duration=2.4,setpts=PTS*4/3,fps=30,tpad=stop_mode=clone:stop_duration=0.2,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,zoompan=z='1+0.05*max(0,1-abs(on-15)/15)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30"
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
# Sparse readable contextual cards at the TOP; canonical captions remain fixed and untouched.
ass=(p/'captions.ass').read_text();style='Style: Context,DejaVu Sans,54,&H003B3930,&H003B3930,&H00EAF4FA,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,65,65,90\n'
ass=ass.replace('[Events]',style+'\n[Events]')
def ts(s):
 cs=round(s*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
cards=[(.1,3.05,'2 MINUTES.\\N3 DAYS LATER?'),(3.3,5.25,'SMALL ≠ CLEAR'),(16.4,21.1,'GOAL → ACTION'),(27.9,31.3,'MEASURED: REPLY TIME'),(35.6,39,'KEEP THE GOAL.\\NCHANGE THE INSTRUCTION.'),(39.5,45.6,'OPEN THE DRAFT.\\NWRITE ONE ROUGH SENTENCE.'),(56.2,60.95,'NOT A CURE-ALL'),(64.4,68.1,'WHAT DOES STARTING\\NLOOK LIKE?')]
for a,b,text in cards:ass+=f'Dialogue: 1,{ts(a)},{ts(b)},Context,,0,0,0,,{{\\fad(120,120)}}{text}\n'
(p/'final-captions.ass').write_text(ass)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(out/'picture.mp4'),'-i',str(p/'audio/final-mix.wav'),'-vf',f"ass={p/'final-captions.ass'}:fontsdir={p/'assets'}",'-map','0:v','-map','1:a','-t',str(end),'-c:v','libx264','-preset','fast','-crf','21','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'first-step-final.mp4')],check=True)
print('FINAL',out/'first-step-final.mp4',flush=True)
