#!/usr/bin/env python3
"""Detect and optionally remove uniform near-white edge mattes from generated scenes."""
from __future__ import annotations
import argparse, shutil
from pathlib import Path
import numpy as np
from PIL import Image

def runlen(mask):
 n=0
 for value in mask:
  if not value: break
  n+=1
 return n

def borders(a, threshold=242, ratio=.88):
 near=(a[:,:,0]>=threshold)&(a[:,:,1]>=threshold)&(a[:,:,2]>=threshold)
 rows=near.mean(axis=1)>=ratio; cols=near.mean(axis=0)>=ratio
 return {'top':runlen(rows),'bottom':runlen(rows[::-1]),'left':runlen(cols),'right':runlen(cols[::-1])}

def main():
 p=argparse.ArgumentParser(); p.add_argument('image',type=Path); p.add_argument('--fix-output',type=Path); p.add_argument('--target-width',type=int,default=1080); p.add_argument('--target-height',type=int,default=1920); p.add_argument('--max-border-px',type=int,default=4)
 a=p.parse_args(); im=Image.open(a.image).convert('RGB'); arr=np.asarray(im); b=borders(arr); bad={k:v for k,v in b.items() if v>a.max_border_px}; print(' '.join(f'{k}={v}' for k,v in b.items()))
 if a.fix_output:
  pad=3; l=min(im.width-2,b['left']+(pad if b['left'] else 0)); r=max(l+2,im.width-b['right']-(pad if b['right'] else 0)); t=min(im.height-2,b['top']+(pad if b['top'] else 0)); bot=max(t+2,im.height-b['bottom']-(pad if b['bottom'] else 0)); im=im.crop((l,t,r,bot))
  target=a.target_width/a.target_height; current=im.width/im.height
  if current>target:
   nw=round(im.height*target); x=(im.width-nw)//2; im=im.crop((x,0,x+nw,im.height))
  else:
   nh=round(im.width/target); y=(im.height-nh)//2; im=im.crop((0,y,im.width,y+nh))
  a.fix_output.parent.mkdir(parents=True,exist_ok=True); im.resize((a.target_width,a.target_height),Image.Resampling.LANCZOS).save(a.fix_output)
  print(f'fixed={a.fix_output}')
 raise SystemExit(1 if bad and not a.fix_output else 0)
if __name__=='__main__': main()
