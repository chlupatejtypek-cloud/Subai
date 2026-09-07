#!/usr/bin/env python3
"""Verify/reconstruct the project's JSON-part backup. Dry run unless --apply.
Never overwrite local edits; only restore missing files. Archives aren't executed.
"""
import argparse,base64,hashlib,io,json,tarfile
from pathlib import Path,PurePosixPath
from urllib.parse import urlparse
import requests
ap=argparse.ArgumentParser();ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--apply',action='store_true');a=ap.parse_args()
parts=[]
for item in json.loads(a.manifest.read_text()):
 if not item['file'].startswith('project-part-'):continue
 u=urlparse(item['url'])
 if u.scheme!='https' or u.hostname!='res.cloudinary.com' or not u.path.startswith('/e5cjysjx/'):raise ValueError('Unexpected backup host/cloud')
 r=requests.get(item['url'],timeout=90);r.raise_for_status();assert hashlib.sha256(r.content).hexdigest()==item['sha256'];parts.append(r.json())
parts.sort(key=lambda x:x['part']);assert parts and len(parts)==parts[0]['parts'] and [x['part'] for x in parts]==list(range(1,len(parts)+1));assert len({x['archive_sha256'] for x in parts})==1
raw=b''.join(base64.b64decode(x['payload'],validate=True) for x in parts);assert hashlib.sha256(raw).hexdigest()==parts[0]['archive_sha256']
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tar:
 count=0
 for m in tar.getmembers():
  rel=PurePosixPath(m.name)
  if not m.isfile() or rel.is_absolute() or '..' in rel.parts:raise ValueError('Unsafe archive member')
  f=a.output.joinpath(*rel.parts)
  if not f.resolve().is_relative_to(a.output.resolve()):raise ValueError('Unsafe destination')
  data=tar.extractfile(m).read();count+=1
  if a.apply and not f.exists():f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
 print('Archive checksum verified; files:',count,'mode:', 'restore missing only' if a.apply else 'dry run')
