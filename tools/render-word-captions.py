#!/usr/bin/env python3
"""Render flat provider word timestamps to the channel-locked ASS style."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def ts(sec):
 cs=max(0,round(sec*100)); h,r=divmod(cs,360000); m,r=divmod(r,6000); s,c=divmod(r,100)
 return f'{h}:{m:02d}:{s:02d}.{c:02d}'
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--timestamps',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--style',type=Path,default=Path(__file__).parents[1]/'config/caption-style.json'); ap.add_argument('--highlights',default='')
 a=ap.parse_args(); st=json.loads(a.style.read_text()); data=json.loads(a.timestamps.read_text()); raw=data['words']; hi={x.upper() for x in a.highlights.split(',') if x}
 words=[]; prev=0.0
 for item in raw:
  text=re.sub(r"[^A-Za-z0-9']+",'',item['text']);
  if not text: continue
  if st['uppercase']: text=text.upper()
  start=max(float(item['start']),prev); end=max(float(item['end']),start+st['minimum_word_ms']/1000); prev=end
  words.append((start,end,text))
 p=st['pop']; x=st['position']['x']; y=st['position']['y']
 head=f'''[Script Info]\nScriptType: v4.00+\nPlayResX: {st['canvas']['width']}\nPlayResY: {st['canvas']['height']}\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Word,{st['font']},{st['font_size']},{st['primary_ass']},{st['primary_ass']},{st['outline_ass']},&H00000000,{-1 if st['bold'] else 0},0,0,0,100,100,0,0,1,{st['outline_px']},{st['shadow_px']},5,20,20,0,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
 lines=[]
 for start,end,text in words:
  color=rf'\c{st["highlight_ass"]}&' if text in hi else ''
  anim=rf'{{\an5\pos({x},{y})\fscx{p["start_scale"]}\fscy{p["start_scale"]}\alpha{p["start_alpha_ass"]}\t(0,{p["overshoot_ms"]},\fscx{p["overshoot_scale"]}\fscy{p["overshoot_scale"]}\alpha&H00&)\t({p["overshoot_ms"]},{p["settle_ms"]},\fscx{p["settle_scale"]}\fscy{p["settle_scale"]})}}'
  lines.append(f'Dialogue: 0,{ts(start)},{ts(end)},Word,,0,0,0,,{anim}{{{color}}}{text}')
 a.output.write_text(head+'\n'.join(lines)+'\n'); print(f'events={len(lines)} style={st["id"]}')
if __name__=='__main__': main()
