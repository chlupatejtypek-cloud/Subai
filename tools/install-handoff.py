#!/usr/bin/env python3
"""Install an owner-supplied, already-decrypted bundle. Dry run by default.
No network calls, no secret logging, no blind overwrite or shell evaluation.
"""
import argparse,json,os,re,shlex,subprocess,tempfile
from pathlib import Path

def parse_env(raw):
 result={}
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
  if '\n' in value or '\r' in value:raise ValueError('Multiline environment value')
  if k in result and result[k]!=value:raise ValueError('Conflicting duplicate environment key: '+k)
  result[k]=value
 return result

def check_path(path,root):
 if not path.is_relative_to(root):raise ValueError('Destination outside repository')
 for x in [path,*path.parents]:
  if x.is_symlink():raise ValueError('Symlink destination refused')
  if x==root:break
 if path.exists() and not path.is_file():raise ValueError('Destination is not a file')

def install(bundle,repo,apply=False):
 if bundle.is_symlink() or repo.is_symlink():raise ValueError('Symlink root refused')
 bundle=bundle.resolve();repo=repo.resolve()
 if not (repo/'.git').is_dir() or (repo/'.git').is_symlink():raise ValueError('Normal Git repository required')
 def read(name):
  f=bundle/name
  if f.is_symlink() or not f.is_file() or f.stat().st_size>1000000:raise ValueError('Invalid bundle file: '+name)
  return f.read_bytes()
 incoming=parse_env(read('credentials.env'));client=json.loads(read('youtube-client.json'));token=json.loads(read('youtube-token.json'))
 registry=json.loads((repo/'config/channels.json').read_text());channel=next(x for x in registry['channels'] if x['id']=='stiles-psychology')
 if token.get('channel',{}).get('id')!=channel['youtube']['channel_id']:raise ValueError('Bundle channel mismatch')
 if not client.get('installed',{}).get('client_id') or not client['installed'].get('client_secret') or not token.get('token',{}).get('refresh_token'):raise ValueError('Incomplete OAuth bundle')
 if token.get('client_id')!=client['installed']['client_id']:raise ValueError('OAuth client mismatch')
 checks={'YOUTUBE_STILES_CLIENT_ID':client['installed']['client_id'],'YOUTUBE_STILES_CLIENT_SECRET':client['installed']['client_secret'],'YOUTUBE_STILES_REFRESH_TOKEN':token['token']['refresh_token']}
 if any(incoming.get(k)!=v for k,v in checks.items()):raise ValueError('Environment and OAuth JSON disagree')
 envpath=repo/'.env';check_path(envpath,repo)
 current=parse_env(envpath.read_bytes()) if envpath.exists() else {}
 conflicts=[k for k in incoming if k in current and current[k] and current[k]!=incoming[k]]
 if conflicts:raise ValueError('Existing credential conflict; verify freshness: '+', '.join(sorted(conflicts)))
 merged={**current,**incoming};envbody=('\n'.join(k+'='+shlex.quote(v) for k,v in sorted(merged.items()))+'\n').encode()
 payloads={envpath:envbody,repo/'credentials/youtube-client.json':(json.dumps(client,indent=2)+'\n').encode(),repo/'.git/credentials':(json.dumps(token,indent=2)+'\n').encode()}
 # Validate EVERYTHING before writing the first file.
 for f,body in payloads.items():
  check_path(f,repo)
  if f!=envpath and f.exists():
   existing=json.loads(f.read_bytes());fresh=json.loads(body)
   if f.name=='youtube-client.json':
    equal=all(existing.get('installed',{}).get(k)==fresh['installed'].get(k) for k in ('client_id','client_secret'))
   else:
    equal=(existing.get('client_id')==fresh.get('client_id') and existing.get('channel',{}).get('id')==fresh.get('channel',{}).get('id') and existing.get('token',{}).get('refresh_token')==fresh.get('token',{}).get('refresh_token'))
   if not equal:raise ValueError('Existing JSON credential conflict: '+str(f.relative_to(repo)))
   payloads[f]=f.read_bytes() # Preserve richer existing metadata for the same credentials.
  if '.git' not in f.relative_to(repo).parts:
   rel=str(f.relative_to(repo));tracked=subprocess.run(['git','ls-files','--error-unmatch','--',rel],cwd=repo,capture_output=True).returncode==0
   ignored=subprocess.run(['git','check-ignore','-q','--',rel],cwd=repo,capture_output=True).returncode==0
   if tracked or not ignored:raise ValueError('Credential destination must be ignored and untracked: '+rel)
 if apply:
  os.umask(0o077)
  for f,body in payloads.items():
   f.parent.mkdir(parents=True,exist_ok=True)
   if f.parent==repo/'credentials':f.parent.chmod(0o700)
   fd,name=tempfile.mkstemp(prefix='.handoff-',dir=f.parent)
   try:
    with os.fdopen(fd,'wb') as h:h.write(body)
    os.chmod(name,0o600);os.replace(name,f)
   finally:
    if os.path.exists(name):os.unlink(name)
 return {'mode':'installed' if apply else 'dry_run','destinations':[str(x.relative_to(repo)) for x in payloads],'secret_values_logged':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--bundle',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--apply',action='store_true');a=ap.parse_args()
 try:print(json.dumps(install(a.bundle,a.repo,a.apply)))
 except Exception as e:print('ERROR:',str(e) if isinstance(e,ValueError) else type(e).__name__);raise SystemExit(1)
if __name__=='__main__':main()
