from pathlib import Path
import json,subprocess,hashlib,re
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont
p=Path(__file__).resolve().parent;final=p/'output/first-step-final.mp4';d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(final)]));v=next(x for x in d['streams'] if x['codec_type']=='video');a=next(x for x in d['streams'] if x['codec_type']=='audio');duration=float(d['format']['duration']);assert 60<=duration<=80;assert (v['width'],v['height'],v['r_frame_rate'])==(1080,1920,'30/1');assert int(v['nb_frames'])==2046
lines=[x for x in (p/'captions.ass').read_text().splitlines() if x.startswith('Dialogue:')];ts=lambda x:sum(float(v)*k for v,k in zip(x.split(':'),(3600,60,1)));caps=[(ts(x.split(',')[1]),ts(x.split(',')[2])) for x in lines];assert len(caps)==231 and all(a<b for a,b in caps) and all(caps[i][1]<=caps[i+1][0] for i in range(len(caps)-1));assert caps[-1][1]<=duration
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',54);maxwidth=0
for l in (p/'final-captions.ass').read_text().splitlines():
 if l.startswith('Dialogue:') and ',Context,' in l:
  txt=re.sub(r'\{[^}]*\}','',l.split(',',9)[9])
  for line in txt.split('\\N'):maxwidth=max(maxwidth,font.getlength(line))
assert maxwidth<950
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(final),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);loud=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0];assert float(loud['input_tp'])<=-1
report={'duration_seconds':duration,'resolution':[1080,1920],'fps':30,'frames':int(v['nb_frames']),'codecs':[v['codec_name'],a['codec_name']],'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'bytes':final.stat().st_size,'caption_events':len(caps),'captions_no_overlap':True,'last_caption_end':caps[-1][1],'context_max_line_width_px':maxwidth,'context_safe_width_px':950,'loudness':loud,'asr':json.loads((p/'asr-qc.json').read_text())['exact_match'],'generated_and_used_illustrations':10,'longest_illustration_hold_seconds':json.loads((p/'storyboard.json').read_text())['max_illustration_hold_seconds'],'review_boundary':'Technical checks and inspected frame samples, not claimed full human audio/video review; owner style hold remains'}
(p/'technical-qc.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
times=[.4,2.7,4.2,8,14,18.5,24,29.5,33,37,42,48,53,58,63,66.5];sheet=Image.new('RGB',(1120,2080),'#eae2d5')
for i,t in enumerate(times):
 f=p/'output'/f'qc-{i:02}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(final),'-frames:v','1',str(f)],check=True);sheet.paste(ImageOps.fit(Image.open(f),(270,480)),((i%4)*280,(i//4)*520));ImageDraw.Draw(sheet).text(((i%4)*280,(i//4)*520+484),f'{t}s',fill='black')
sheet.save('/home/user/first-step-final-qc.jpg')
