#!/usr/bin/env python3
"""Refresh the existing encrypted handoff in place, never upload plaintext.
Local: load .env into environment, set HANDOFF_PASSPHRASE, then run.
CI: download/decrypt existing ciphertext in memory to preserve owner credentials;
merge current CI secrets; package current tracked documentation; re-encrypt.
Uses the original compatible OpenSSL AES-256-CBC/PBKDF2-SHA256/600000 format.
"""
import argparse,hashlib,io,json,os,subprocess,tarfile,time
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://res.cloudinary.com/e5cjysjx/raw/upload/subai/private-transfer/subai-agent-bootstrap-v1.enc'
KEYS=['GITHUB_PAT','ELEVENLABS_API_KEY','CLOUDINARY_CLOUD_NAME','CLOUDINARY_API_KEY','CLOUDINARY_API_SECRET','FISH_API_KEY','FISH_API_BASE','FISH_REFERENCE_ID','AGNES_API_KEY','AGNES_API_BASE','YOUTUBE_STILES_CLIENT_ID','YOUTUBE_STILES_CLIENT_SECRET','YOUTUBE_STILES_REFRESH_TOKEN']
def parse_env(raw):
 import shlex,re
 out={}
 for line in raw.decode().splitlines():
  line=line.strip()
  if not line or line.startswith('#'):continue
  if line.startswith('export '):line=line[7:]
  if '=' not in line:raise ValueError('Invalid environment entry')
  k,v=line.split('=',1)
  if not re.fullmatch(r'[A-Z_][A-Z0-9_]*',k):raise ValueError('Invalid environment key')
  values=shlex.split(v,comments=True,posix=True)
  if len(values)>1:raise ValueError('Unquoted environment value')
  value=values[0] if values else ''
  if k in KEYS:
   if k in out and out[k]!=value:raise ValueError('Conflicting environment key')
   out[k]=value
 return out
def openssl(data,password,decrypt=False):
 # stdin carries the passphrase, while data is a mode-600 temporary file.
 import tempfile
 with tempfile.TemporaryDirectory(dir=ROOT/'credentials') as d:
  source=Path(d)/'input';source.write_bytes(data);source.chmod(0o600)
  cmd=['openssl','enc','-aes-256-cbc','-pbkdf2','-iter','600000','-md','sha256','-in',str(source),'-pass','stdin']
  help_result=subprocess.run(['openssl','enc','-help'],capture_output=True)
  if b'-saltlen' in help_result.stdout+help_result.stderr:cmd.extend(['-saltlen','8'])
  if decrypt:cmd.insert(2,'-d')
  r=subprocess.run(cmd,input=(password+'\n').encode(),capture_output=True)
  if r.returncode:raise ValueError('Encryption/decryption failed; no plaintext output disclosed')
  return r.stdout
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--upload',action='store_true');ap.add_argument('--output',default='credentials/subai-agent-bootstrap-v1.enc');args=ap.parse_args()
 os.umask(0o077);(ROOT/'credentials').mkdir(exist_ok=True)
 password=os.environ.get('HANDOFF_PASSPHRASE','')
 if not password:raise ValueError('HANDOFF_PASSPHRASE is required')
 env={}
 if (ROOT/'.env').exists():env=parse_env((ROOT/'.env').read_bytes())
 else:
  # Preserve existing owner-supplied credentials, including local Git access, without a second PAT secret.
  recorded=ROOT/'config/transfer.json'
  source_url=json.loads(recorded.read_text()).get('versioned_url',SOURCE) if recorded.exists() else SOURCE
  if not source_url.startswith('https://res.cloudinary.com/e5cjysjx/raw/upload/'):raise ValueError('Unexpected handoff source host/path')
  r=requests.get(source_url,timeout=60);r.raise_for_status()
  if recorded.exists() and hashlib.sha256(r.content).hexdigest()!=json.loads(recorded.read_text())['sha256']:raise ValueError('Previous handoff ciphertext checksum mismatch')
  plain=openssl(r.content,password,True)
  with tarfile.open(fileobj=io.BytesIO(plain),mode='r:gz') as t:
   member=t.getmember('subai-agent-bootstrap/credentials.env')
   if member.size>64000:raise ValueError('Unexpected credential payload size')
   env=parse_env(t.extractfile(member).read())
 for k in KEYS:
  if os.environ.get(k):env[k]=os.environ[k]
 reg=json.loads((ROOT/'config/channels.json').read_text());c=reg['channels'][0];env['FISH_REFERENCE_ID']=c['voice']['reference_id']
 if (ROOT/'credentials/youtube-client.json').exists():
  client=json.loads((ROOT/'credentials/youtube-client.json').read_text());inside=client['installed'];env.setdefault('YOUTUBE_STILES_CLIENT_ID',inside['client_id']);env.setdefault('YOUTUBE_STILES_CLIENT_SECRET',inside['client_secret'])
 else:
  client={'installed':{'client_id':env['YOUTUBE_STILES_CLIENT_ID'],'client_secret':env['YOUTUBE_STILES_CLIENT_SECRET'],'auth_uri':'https://accounts.google.com/o/oauth2/auth','token_uri':'https://oauth2.googleapis.com/token','redirect_uris':['http://localhost']}}
 if (ROOT/'.git/credentials').exists():
  local=json.loads((ROOT/'.git/credentials').read_text());env.setdefault('YOUTUBE_STILES_REFRESH_TOKEN',local['token']['refresh_token'])
 required=['CLOUDINARY_CLOUD_NAME','CLOUDINARY_API_KEY','CLOUDINARY_API_SECRET','FISH_API_KEY','YOUTUBE_STILES_CLIENT_ID','YOUTUBE_STILES_CLIENT_SECRET','YOUTUBE_STILES_REFRESH_TOKEN']
 if any(not env.get(k) for k in required):raise ValueError('Required handoff credential missing')
 if client['installed']['client_id']!=env['YOUTUBE_STILES_CLIENT_ID'] or client['installed']['client_secret']!=env['YOUTUBE_STILES_CLIENT_SECRET']:raise ValueError('Client JSON conflicts with environment credentials')
 # Keep shell-compatible values without evaluating incoming .env. No newline-bearing secret values.
 import shlex
 if any('\n' in v or '\r' in v for v in env.values()):raise ValueError('Unexpected multiline credential')
 envbytes=('\n'.join(k+'='+shlex.quote(v) for k,v in sorted(env.items()))+'\n').encode()
 yt={'token':{'refresh_token':env['YOUTUBE_STILES_REFRESH_TOKEN'],'scope':' '.join(c['youtube']['scopes']),'token_type':'Bearer'},'channel':{'id':c['youtube']['channel_id'],'title':c['youtube']['authenticated_display_name']},'client_id':env['YOUTUBE_STILES_CLIENT_ID']}
 start=(ROOT/'START_HERE.md').read_text()
 files={'START_HERE.md':start.encode(),'HANDOFF.md':(ROOT/'HANDOFF.md').read_bytes(),'credentials.env':envbytes,'youtube-client.json':json.dumps(client).encode(),'youtube-token.json':json.dumps(yt).encode()}
 tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
 for name in tracked:
  path=ROOT/name
  if path.is_file() and (path.suffix in ('.md','.json','.csv','.py','.yml','.txt','.sh') or name == '.env.example') and name != 'config/transfer.json' and not name.startswith('productions/') and path.stat().st_size<1000000:
   files['repo-snapshot/'+name]=path.read_bytes()
 files['MANIFEST.txt']=('\n'.join(sorted(files))+'\n').encode()
 buffer=io.BytesIO()
 with tarfile.open(fileobj=buffer,mode='w:gz') as t:
  for name,body in files.items():
   info=tarfile.TarInfo('subai-agent-bootstrap/'+name);info.size=len(body);info.mode=0o600;info.mtime=int(time.time());t.addfile(info,io.BytesIO(body))
 plain=buffer.getvalue();encrypted=openssl(plain,password)
 if openssl(encrypted,password,True)!=plain:raise ValueError('Encrypted roundtrip verification failed')
 output=ROOT/args.output;output.parent.mkdir(exist_ok=True,parents=True);output.write_bytes(encrypted);output.chmod(0o600)
 info={'schema_version':2,'public_id':'subai/private-transfer/subai-agent-bootstrap-v1.enc','resource_type':'raw','stable_url':SOURCE,'sha256':hashlib.sha256(encrypted).hexdigest(),'bytes':len(encrypted),'encryption':'OpenSSL AES-256-CBC / PBKDF2-HMAC-SHA256 / 600000 iterations','encryption_parameters':{'cipher':'aes-256-cbc','kdf':'PBKDF2','digest':'sha256','iterations':600000,'salt_bytes':8,'envelope':'binary OpenSSL Salted__','plaintext':'tar.gz'},'repo_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'contains':'START_HERE.md, HANDOFF.md, encrypted credentials, YouTube client/token, current tracked repo snapshot; never plaintext','updated_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 if args.upload:
  timestamp=str(int(time.time()));public_id='subai-agent-bootstrap-v1.enc';folder='subai/private-transfer';params=f'folder={folder}&overwrite=true&public_id={public_id}&timestamp={timestamp}';sig=hashlib.sha1((params+env['CLOUDINARY_API_SECRET']).encode()).hexdigest()
  r=requests.post(f"https://api.cloudinary.com/v1_1/{env['CLOUDINARY_CLOUD_NAME']}/raw/upload",data={'folder':folder,'public_id':public_id,'overwrite':'true','timestamp':timestamp,'signature':sig,'api_key':env['CLOUDINARY_API_KEY']},files={'file':(public_id,encrypted,'application/octet-stream')},timeout=90)
  if r.status_code!=200:raise ValueError('Encrypted upload failed HTTP '+str(r.status_code))
  result=r.json();info['versioned_url']=result['secure_url'];info['cloudinary_version']=result['version']
  check=requests.get(info['versioned_url'],timeout=60)
  if check.status_code!=200 or hashlib.sha256(check.content).hexdigest()!=info['sha256']:raise ValueError('Uploaded ciphertext verification failed')
  info['verification']='HTTP 200 + SHA256 matches locally roundtrip-tested ciphertext'
  (ROOT/'config/transfer.json').write_text(json.dumps(info,indent=2)+'\n')
 print(json.dumps(info))
if __name__=='__main__':
 try:main()
 except Exception as e:
  print('ERROR:',str(e) if isinstance(e,ValueError) else type(e).__name__);raise SystemExit(1)
