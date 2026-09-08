"""Smooth staged UI: every component fades/slides; a single bounded circle; no spawned labels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,json,math
p=Path(__file__).resolve().parent;W,H=1080,1920;fps=30;duration=48.3
fonts={n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',n) for n in (32,36,40,44,48,52,58,64,72)}
cream='#FFF8E9';ink='#173B3B';teal='#3B827D';gold='#C49138'
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def text(im,s,x,y,size,age,at=0,col=ink):
 u=ease((age-at)/.32)
 if not u:return
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer);d.text((x,y+round(22*(1-u))),s,font=fonts[size],fill=col);layer.putalpha(layer.getchannel('A').point(lambda a:round(a*u)));im.alpha_composite(layer)
def frame(t):
 im=Image.new('RGBA',(W,H));layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 windows=[(6.2,15.3,'equation'),(19,23.2,'prospects'),(38,44.4,'check')]
 selected=next(((a,b,k) for a,b,k in windows if a<=t<b),None)
 if not selected:return im
 start,end,kind=selected;age=t-start;fade=min(ease(age/.32),ease((end-t)/.32));dy=round(26*(1-ease(age/.32)))
 def panel(y,h):d.rounded_rectangle((80,y,1000,y+h),radius=30,fill=cream,outline=ink,width=3)
 if kind=='equation':
  panel(265,760);text(layer,'FOLLOW THE TOTAL',120,305,58,age)
  text(layer,'GAIN FRAME',125,427,36,age,.25,teal)
  text(layer,'1,000',135,490,64,age,.35);text(layer,'+ 500',375,490,64,age,1.1,teal);text(layer,'= 1,500',640,490,58,age,1.65,teal)
  text(layer,'LOSS FRAME',125,627,36,age,2.55,gold)
  text(layer,'2,000',135,690,64,age,2.65);text(layer,'− 500',375,690,64,age,3.55,gold);text(layer,'= 1,500',640,690,58,age,4.15,teal)
  text(layer,'SAME FINAL AMOUNT',135,855,44,age,5.25)
  text(layer,'1,500',665,923,52,age,5.55,teal)
  # One circle draws once around the common result; no repeated flashing.
  c=ease((age-6.0)/.55);ca=ease((8.6-age)/.35)
  if c>0 and ca>0:
   ring=Image.new('RGBA',(W,H));rd=ImageDraw.Draw(ring);rd.arc((628,901,871,1001),start=-90,end=-90+359*c,fill=gold,width=6);ring.putalpha(ring.getchannel('A').point(lambda a:round(a*ca)));layer.alpha_composite(ring)
 elif kind=='prospects':
  panel(270,730);text(layer,'SAME FINAL CHOICES',120,310,52,age)
  text(layer,'IN BOTH FRAMES',120,390,36,age,.15)
  text(layer,'SURE',135,493,40,age,.25,teal);text(layer,'1,500',585,475,72,age,.45,teal)
  text(layer,'OR A GAMBLE',135,655,40,age,.7,gold)
  text(layer,'50% → 1,000',155,742,48,age,.9);text(layer,'50% → 2,000',155,837,48,age,1.2)
  text(layer,'Hypothetical study choices',135,939,32,age,1.45)
 else:
  panel(280,725);text(layer,'COMPARE THE TERMS',120,330,52,age)
  for n,(label,at) in enumerate([('Final amounts',.2),('Probabilities',.95),('Real costs',1.7)]):
   y=490+n*155;u=ease((age-at)/.32)
   if u:
    box=Image.new('RGBA',(W,H));bd=ImageDraw.Draw(box);bd.rounded_rectangle((122,y-10,958,y+105),radius=20,fill='#DCE9DF');box.putalpha(box.getchannel('A').point(lambda a:round(a*u)));layer.alpha_composite(box)
   text(layer,label,170,y+10,48,age,at)
  text(layer,'Not just “gain” or “lose”.',140,938,36,age,2.35)
 # Entire panel also eases in/out; every conditional text has its own alpha ramp.
 layer.putalpha(layer.getchannel('A').point(lambda a:round(a*fade)));im.alpha_composite(layer,(0,dy));return im
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an','-c:v','qtrle',str(p/'output/ui.mov')],stdin=subprocess.PIPE)
try:
 for i in range(round(duration*fps)):proc.stdin.write(frame(i/fps).tobytes())
finally:proc.stdin.close()
assert proc.wait()==0
(p/'ui-qc.json').write_text(json.dumps({'segments':[[6.2,15.3,'staged equations'],[19,23.2,'equivalent final sure/gamble prospects'],[38,44.4,'progressive checklist']],'component_transition_ms':320,'panel_translation_px':26,'text_translation_px':22,'entrances_and_exits_eased':True,'blur_fade_seconds':.4,'blur_intervals':[[6.2,15.3],[38,44.4]],'circle_count':1,'circle_interval':[12.2,14.8],'arithmetic':'1000+500=2000-500=1500; both gambles1000/2000 at50% each','units':'Hypothetical generic money units, no claim of modern-dollar study'},indent=2))
