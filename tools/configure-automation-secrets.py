#!/usr/bin/env python3
"""Owner-run provisioning only. Requires current-session GITHUB_PAT and PyNaCl.
Secret values are encrypted locally with GitHub's public key, never printed.
Do not execute this script with arbitrary third-party credential paths.
"""
import base64,json,os
from pathlib import Path
import requests
from nacl.public import PublicKey,SealedBox
ROOT=Path(__file__).resolve().parents[1]
repo='https://api.github.com/repos/chlupatejtypek-cloud/Subai'
headers={'Authorization':'Bearer '+os.environ['GITHUB_PAT'],'Accept':'application/vnd.github+json'}
r=requests.get(repo+'/actions/secrets/public-key',headers=headers,timeout=30)
if r.status_code!=200:raise SystemExit('Cannot read Actions public key: HTTP '+str(r.status_code))
pub=r.json();box=SealedBox(PublicKey(base64.b64decode(pub['key'])))
c=json.loads((ROOT/'credentials/youtube-client.json').read_text())['installed'];token=json.loads((ROOT/'.git/credentials').read_text())['token']
values={name:os.environ[name] for name in ['CLOUDINARY_CLOUD_NAME','CLOUDINARY_API_KEY','CLOUDINARY_API_SECRET','FISH_API_KEY','AGNES_API_KEY','ELEVENLABS_API_KEY','HANDOFF_PASSPHRASE'] if os.environ.get(name)}
values.update(YOUTUBE_STILES_CLIENT_ID=c['client_id'],YOUTUBE_STILES_CLIENT_SECRET=c['client_secret'],YOUTUBE_STILES_REFRESH_TOKEN=token['refresh_token'])
if not values.get('HANDOFF_PASSPHRASE'):raise SystemExit('Missing handoff passphrase')
for name,value in values.items():
 r=requests.put(repo+'/actions/secrets/'+name,headers=headers,json={'key_id':pub['key_id'],'encrypted_value':base64.b64encode(box.encrypt(value.encode())).decode()},timeout=30)
 print(name,'HTTP',r.status_code)
 if r.status_code not in (201,204):raise SystemExit('Secret provisioning failed; values suppressed')
# Never store the broad owner PAT as a separate Actions secret.
