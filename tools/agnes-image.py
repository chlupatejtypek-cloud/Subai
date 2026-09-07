#!/usr/bin/env python3
"""Generate ONE Agnes still with optional public reference images.
Official docs: https://agnes-ai.com/en/docs/agnes-image-20-flash
No automatic retry on an ambiguous request failure; preserve spend/count control.
"""
import argparse,base64,io,json,os,time
from pathlib import Path
from urllib.parse import urlparse
import requests
from PIL import Image

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prompt-file',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--image',action='append',default=[]);ap.add_argument('--model',default='agnes-image-2.0-flash');ap.add_argument('--size',default='768x1376');a=ap.parse_args()
 key=os.environ.get('AGNES_API_KEY')
 if not key:raise ValueError('AGNES_API_KEY missing')
 body={'model':a.model,'prompt':a.prompt_file.read_text().strip(),'size':a.size,'extra_body':{'response_format':'b64_json'}}
 if a.image:body['extra_body']['image']=a.image
 r=requests.post('https://apihub.agnes-ai.com/v1/images/generations',headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},json=body,timeout=240)
 if r.status_code!=200:
  reason=''
  try:reason=str(r.json().get('code',''))
  except Exception:pass
  raise ValueError('Agnes still HTTP '+str(r.status_code)+' '+reason+'; no automatic duplicate retry')
 d=r.json();item=d.get('data',[{}])[0]
 if item.get('b64_json'):raw=base64.b64decode(item['b64_json'])
 elif item.get('url'):
  u=item['url'];parsed=urlparse(u)
  if parsed.scheme!='https':raise ValueError('Unexpected download scheme')
  q=requests.get(u,timeout=90);q.raise_for_status();raw=q.content
 else:raise ValueError('No image in successful response')
 im=Image.open(io.BytesIO(raw)).convert('RGB');a.output.parent.mkdir(parents=True,exist_ok=True);im.save(a.output)
 meta={'provider':'Agnes AI','model':a.model,'endpoint':'/v1/images/generations','requested_size':a.size,'actual_size':list(im.size),'reference_urls':a.image,'prompt':body['prompt'],'http_status':200,'generated_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 a.output.with_suffix('.metadata.json').write_text(json.dumps(meta,indent=2)+'\n');print('AGNES_IMAGE_OK',a.output.name,im.size,flush=True)
if __name__=='__main__':
 try:main()
 except Exception as e:
  print('ERROR:',str(e) if isinstance(e,ValueError) else type(e).__name__,flush=True);raise SystemExit(1)
