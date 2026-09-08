"""Original animated explanatory UI; exact primary means/CI, no invented percentage."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,math,json
p=Path(__file__).resolve().parent;W,H=1080,1920;fps=30;duration=50.1
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fonts={n:ImageFont.truetype(FONT,n) for n in (32,36,40,44,48,52,58,64)}
cream='#FFF8E9';ink='#173B3B';teal='#3B827D';gold='#C49138';light='#DCE9DF'
def txt(d,xy,s,size=44,fill=ink):d.text(xy,s,font=fonts[size],fill=fill)
def panel(d,x,y,w,h):
 d.rounded_rectangle((x+8,y+12,x+w+8,y+h+12),radius=32,fill=(0,0,0,55));d.rounded_rectangle((x,y,x+w,y+h),radius=32,fill=cream,outline=ink,width=3)
def ease(x):x=max(0,min(1,x));return 1-(1-x)**3
def frame(t):
 im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
 if 9.5<=t<16.8:
  age=t-9.5;panel(d,72,255,936,785);txt(d,(120,290),'THE LIKING GAP',58);txt(d,(120,370),'Estimated vs reported liking',36)
  # Shared1–7 axis and exact study1a predicted marginal means. Bars animate from1, not from invented baseline zero.
  x=lambda v:155+(v-1)/6*730
  for y,label,value,ci,col,delay in [(540,'Your estimate',5.17,(4.85,5.49),gold,0),(735,'Partner report',5.82,(5.49,6.14),teal,2.3)]:
   txt(d,(120,y-68),label,44)
   d.rounded_rectangle((155,y,885,y+30),radius=15,fill=light)
   u=ease((age-delay)/.8)
   if u>0:
    at=1+(value-1)*u;d.rounded_rectangle((155,y,max(175,x(at)),y+30),radius=15,fill=col)
   if u>.99:
    d.line((x(ci[0]),y+15,x(ci[1]),y+15),fill=ink,width=4)
    for v in ci:d.line((x(v),y-3,x(v),y+33),fill=ink,width=4)
    txt(d,(785,y-68),f'{value:.2f}',44,col)
  for n in range(1,8):
   d.line((x(n),810,x(n),824),fill=ink,width=2);txt(d,(x(n)-12,840),str(n),32)
  txt(d,(120,911),'Study 1a · 34 people · scale 1–7',36)
  txt(d,(120,963),'Lines show 95% confidence intervals',32)
 elif 34<=t<40.4:
  age=t-34;panel(d,65,305,950,675);txt(d,(108,347),'WHAT DO YOU KNOW?',52)
  d.rounded_rectangle((105,455,975,625),radius=22,fill=light);txt(d,(135,477),'OBSERVATION',36,teal)
  if age>.3:txt(d,(135,542),'“I paused.”',52)
  d.rounded_rectangle((105,655,975,885),radius=22,fill='#F2E1BC');txt(d,(135,677),'INTERPRETATION',36,gold)
  if age>2:txt(d,(135,738),'“They were bored.”',48)
  if age>4:
   d.rounded_rectangle((535,823,945,870),radius=12,fill=ink);txt(d,(557,829),'NOT VERIFIED',32,cream)
 elif 41<=t<44.6:
  age=t-41;panel(d,105,240,870,410);txt(d,(150,285),'A LOW-PRESSURE FOLLOW-UP',36)
  d.rounded_rectangle((150,375,930,480),radius=23,fill=light)
  message='Nice chatting earlier';shown=message[:min(len(message),int(age*19))];txt(d,(180,402),shown,44)
  if age>1.5:
   d.rounded_rectangle((700,525,925,603),radius=25,fill=teal);txt(d,(751,539),'SEND',40,cream)
  # No fabricated response or guarantee of reciprocation.
 return im
cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an','-c:v','qtrle',str(p/'output/ui.mov')]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
 for i in range(round(duration*fps)):proc.stdin.write(frame(i/fps).tobytes())
finally:proc.stdin.close()
assert proc.wait()==0
(p/'ui-qc.json').write_text(json.dumps({'segments':[[9.5,16.8,'actual study comparison, animated paired ratings'],[34,40.4,'observed versus assumed, revealed verification state'],[41,44.6,'typed optional follow-up, no invented reply']],'study_data':{'n':34,'scale':[1,7],'estimate':5.17,'estimate_ci':[4.85,5.49],'report':5.82,'report_ci':[5.49,6.14]},'background_blur':'Only first two UI segments; UI and captions composited afterwards remain sharp','not_just_headings':True},indent=2))
for t in [15.5,39.5,43.5]:frame(t).save(p/'output'/f'ui-{t}.png')
