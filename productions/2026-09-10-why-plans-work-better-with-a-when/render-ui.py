"""Authored visible 400ms UI entrances, smoothly growing raw-rate chart, cue/action cards."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,json
p=Path(__file__).resolve().parent;W,H=1080,1920;fps=30;duration=48.3
fonts={n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',n) for n in (32,36,40,42,44,48,52,58,64,72)}
cream='#FFF8E9';ink='#173B3B';teal='#3B827D';gold='#C49138'
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def text(im,s,x,y,size,age,at=0,col=ink):
 u=ease((age-at)/.4)
 if not u:return
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer);d.text((x+round(60*(1-u)),y),s,font=fonts[size],fill=col);layer.putalpha(layer.getchannel('A').point(lambda a:round(a*u)));im.alpha_composite(layer)
def frame(t):
 im=Image.new('RGBA',(W,H));layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 windows=[(13.2,19.6,'chart'),(25.4,32.2,'plan'),(35,38.6,'check')]
 selected=next(((a,b,k) for a,b,k in windows if a<=t<b),None)
 if not selected:return im
 start,end,kind=selected;age=t-start;fade=min(ease(age/.4),ease((end-t)/.4));dy=round(50*(1-ease(age/.4)))
 def panel(y,h):d.rounded_rectangle((80,y,1000,y+h),radius=30,fill=cream,outline=ink,width=3)
 if kind=='chart':
  panel(270,745);text(layer,'WORKPLACE FLU SHOTS',120,305,48,age)
  text(layer,'Reminder alone',130,430,40,age,.2)
  text(layer,'33.1%',710,422,52,age,.35,gold)
  text(layer,'Reminder + date / time',130,630,36,age,1.2)
  text(layer,'37.1%',710,675,52,age,1.4,teal)
  for y,rate,col,at in [(515,.331,gold,.4),(754,.371,teal,1.5)]:
   u=ease((age-at)/.75);a=ease((age-at)/.4)
   if a:
    g=Image.new('RGBA',(W,H));gd=ImageDraw.Draw(g);gd.rounded_rectangle((135,y,935,y+42),radius=12,fill='#E4E4D4');gd.rounded_rectangle((135,y,135+max(10,800*rate*u),y+42),radius=12,fill=col);g.putalpha(g.getchannel('A').point(lambda v:round(v*a)));layer.alpha_composite(g)
  text(layer,'0%',130,565,32,age,.4);text(layer,'100%',840,565,32,age,.4)
  text(layer,'+4.0 percentage points',130,861,48,age,2.25,teal)
  text(layer,'Raw rates · one employer',130,953,32,age,2.5)
 elif kind=='plan':
  panel(270,760);text(layer,'GIVE THE PLAN A CUE',120,310,48,age)
  text(layer,'WHEN',130,439,40,age,.25,gold)
  text(layer,'Lunch plate → sink',130,504,52,age,.45)
  # Connector visibly grows before the second condition, not an instantaneous arrow.
  u=ease((age-2)/.55)
  if u:
   dr=ImageDraw.Draw(layer);dr.line((170,600,170,600+86*u),fill=teal,width=6)
   if u>.8:
    q=(u-.8)/.2;dr.line((170-13*q,674,170,686),fill=teal,width=5);dr.line((170+13*q,674,170,686),fill=teal,width=5)
  text(layer,'THEN',130,720,40,age,2.65,teal)
  text(layer,'Shoes on → walk',130,790,52,age,2.85)
  text(layer,'A specific cue. A specific action.',130,958,32,age,4.15)
 else:
  panel(305,540);text(layer,'MAKE IT USABLE',125,350,52,age)
  text(layer,'A cue you will notice',130,515,44,age,.25,gold)
  text(layer,'An action you can do',130,675,44,age,1.65,teal)
 layer.putalpha(layer.getchannel('A').point(lambda a:round(a*fade)));im.alpha_composite(layer,(0,dy));return im
if __name__=='__main__':
 proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an','-c:v','qtrle',str(p/'output/ui.mov')],stdin=subprocess.PIPE)
 try:
  for i in range(round(duration*fps)):proc.stdin.write(frame(i/fps).tobytes())
 finally:proc.stdin.close()
 assert proc.wait()==0
 (p/'ui-qc.json').write_text(json.dumps({'segments':[[13.2,19.6,'raw uptake chart'],[25.4,32.2,'cue action plan'],[35,38.6,'feasibility checklist']],'component_transition_ms':400,'panel_translation_px':50,'text_translation_px':60,'chart_growth_ms':750,'entrances_and_exits_eased':True,'blur_fade_seconds':.4,'blur_intervals':[[13.2,19.6],[25.4,32.2]],'circle_count':0,'study_chart':'Raw33.1%control vs37.1%date/time; difference4.0percentage points; full0–100%tracks; no adjusted/raw mixing'},indent=2))
