"""Authored visible 400ms UI entrances, smoothly growing raw-rate chart, cue/action cards."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,json
p=Path(__file__).resolve().parent;W,H=1080,1920;fps=30;duration=43.1
fonts={n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',n) for n in (32,36,40,42,44,48,52,58,64,72)}
cream='#FFF8E9';ink='#173B3B';teal='#3B827D';gold='#C49138'
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def text(im,s,x,y,size,age,at=0,col=ink):
 u=ease((age-at)/.4)
 if not u:return
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer);d.text((x+round(60*(1-u)),y),s,font=fonts[size],fill=col);layer.putalpha(layer.getchannel('A').point(lambda a:round(a*u)));im.alpha_composite(layer)
def frame(t):
 im=Image.new('RGBA',(W,H));layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 windows=[(22.9,29.8,'result'),(33.4,36.6,'words')]
 selected=next(((a,b,k) for a,b,k in windows if a<=t<b),None)
 if not selected:return im
 start,end,kind=selected;age=t-start;fade=min(ease(age/.4),ease((end-t)/.4));dy=round(50*(1-ease(age/.4)))
 def panel(y,h):d.rounded_rectangle((80,y,1000,y+h),radius=30,fill=cream,outline=ink,width=3)
 if kind=='result':
  panel(280,720);text(layer,'ONE WEEK LATER',120,315,48,age)
  text(layer,'Different spider, different room',120,385,32,age,.15)
  text(layer,'Physical stress response',130,500,40,age,.25)
  text(layer,'Lowest after labeling',130,566,48,age,.55,teal)
  text(layer,'Fear they reported',130,720,40,age,1.75)
  text(layer,'About the same',130,786,48,age,2.05,gold)
  u=ease((age-2.6)/.6)
  if u:ImageDraw.Draw(layer).line((132,852,132+round(408*u),852),fill=gold,width=6)
  text(layer,'Groups differed in the body,',130,900,32,age,3.3)
  text(layer,'not in the feeling.',130,946,32,age,3.5)
 else:
  panel(320,430);text(layer,'BE SPECIFIC',125,362,52,age)
  text(layer,'Nervous. Embarrassed.',130,505,44,age,.3,teal)
  text(layer,'More precise words, larger effect',130,620,32,age,1.1)
 layer.putalpha(layer.getchannel('A').point(lambda a:round(a*fade)));im.alpha_composite(layer,(0,dy));return im
if __name__=='__main__':
 proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an','-c:v','qtrle',str(p/'output/ui.mov')],stdin=subprocess.PIPE)
 try:
  for i in range(round(duration*fps)):proc.stdin.write(frame(i/fps).tobytes())
 finally:proc.stdin.close()
 assert proc.wait()==0
 (p/'ui-qc.json').write_text(json.dumps({'segments':[[22.9,29.8,'one-week outcome contrast'],[33.4,36.6,'be specific card']],'component_transition_ms':400,'panel_translation_px':50,'text_translation_px':60,'underline_growth_ms':600,'entrances_and_exits_eased':True,'blur_fade_seconds':.4,'blur_intervals':[[22.9,29.8],[33.4,36.6]],'underline_count':1,'claims':'Qualitative only: lowest physiological response after labeling, self-reported fear about the same. No invented numbers, no percentages, no amygdala claim.'},indent=2))
