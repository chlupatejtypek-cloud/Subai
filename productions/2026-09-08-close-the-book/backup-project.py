"""Signed Cloudinary backup; re-download and verify every delivered object."""
from pathlib import Path
import os,io,tarfile,json,hashlib,base64,time,requests,math
p=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
files=[f for f in p.rglob('*') if f.is_file() and not set(f.relative_to(p).parts)&{'output','__pycache__'} and f.name not in {'assets.json','cloudinary.md','source-manifest.json','.media-keep','cleanup.md'} and f.relative_to(p).as_posix() not in {'audio/final-mix.wav','audio/sfx.wav','audio/source.wav','audio/compacted.wav'}]
files.sort();manifest=[{'file':str(f.relative_to(p)),'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size} for f in files];(p/'source-manifest.json').write_text(json.dumps(manifest,indent=2));files.append(p/'source-manifest.json');buf=io.BytesIO()
with tarfile.open(fileobj=buf,mode='w:gz') as tar:
 for f in files:tar.add(f,arcname=str(f.relative_to(p)),recursive=False)
raw=buf.getvalue();count=math.ceil(len(raw)/4000000);final=p/'output/close-book-final.mp4';uploads=[final]
for i in range(count):
 f=p/'output'/f'project-part-{i+1}.json';f.write_text(json.dumps({'format':'tar.gz/base64','part':i+1,'parts':count,'archive_sha256':sha(raw),'payload':base64.b64encode(raw[i*4000000:(i+1)*4000000]).decode()},separators=(',',':')));uploads.append(f)
results=[];folder='subai/productions/stiles-psychology/2026-09-08-close-book'
for f in uploads:
 ts=str(int(time.time()));pid=f.name if f.suffix=='.json' else f.stem;params={'folder':folder,'overwrite':'true','public_id':pid,'timestamp':ts};signature=hashlib.sha1(('&'.join(f'{k}={v}' for k,v in sorted(params.items()))+os.environ['CLOUDINARY_API_SECRET']).encode()).hexdigest()
 with f.open('rb') as h:r=requests.post(f"https://api.cloudinary.com/v1_1/{os.environ['CLOUDINARY_CLOUD_NAME']}/auto/upload",data={**params,'api_key':os.environ['CLOUDINARY_API_KEY'],'signature':signature},files={'file':(f.name,h)},timeout=180)
 r.raise_for_status();url=r.json()['secure_url'];v=requests.get(url,timeout=120);v.raise_for_status();assert sha(v.content)==sha(f.read_bytes());results.append({'file':f.name,'url':url,'sha256':sha(v.content),'bytes':len(v.content),'verified_http':v.status_code});print('Verified',f.name,len(v.content),flush=True)
(p/'assets.json').write_text(json.dumps(results,indent=2));(p/'cloudinary.md').write_text('# Verified familiar-claims backup\n\n'+ '\n'.join(f"- {x['file']}: {x['url']} — downloaded SHA256 `{x['sha256']}` matched." for x in results)+'\n');print('Archive files:',len(files),'sha:',sha(raw),flush=True)
