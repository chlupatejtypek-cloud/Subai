"""Observe the single dispatched publisher, then verify returned YouTube state."""
from pathlib import Path
import os,time,json,requests,base64,importlib.util,datetime
p=Path(__file__).resolve().parent;root=p.parents[1];v=os.getenv('GITHUB_TOKEN') or os.getenv('GITHUB_PAT') or os.getenv('GH_TOKEN');headers={'Authorization':'Bearer '+v,'Accept':'application/vnd.github+json'};base='https://api.github.com/repos/chlupatejtypek-cloud/Subai';deadline=time.time()+600
while time.time()<deadline:
 r=requests.get(base+'/actions/workflows/publish-calendar.yml/runs',headers=headers,params={'per_page':15},timeout=30);r.raise_for_status();runs=[x for x in r.json()['workflow_runs'] if x['event']=='workflow_dispatch' and x['head_sha'].startswith('edb203c')]
 if runs:
  run=runs[0];print('Publisher',run['id'],run['status'],run['conclusion'],flush=True)
  if run['status']=='completed':assert run['conclusion']=='success';break
 time.sleep(12)
else:raise TimeoutError('Publisher not confirmed complete; do not retry upload')
r=requests.get(base+'/contents/calendar/2026-09-07_2026-10-06.json',headers=headers,params={'ref':'main'},timeout=30);r.raise_for_status();cal=json.loads(base64.b64decode(r.json()['content']));item=next(x for x in cal['items'] if x['id']=='SP-20260908-2');assert item['status']=='scheduled',item['status'];print('Calendar',item['status'],item.get('youtube_video_id'),flush=True)
spec=importlib.util.spec_from_file_location('publisher',root/'tools/youtube-publish.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);channel,_=m.config('stiles-psychology');token=m.access_token(channel)
vid=item.get('youtube_video_id') or item.get('youtube',{}).get('video_id');assert vid,item.keys()
for _ in range(15):
 r=requests.get('https://www.googleapis.com/youtube/v3/videos',params={'id':vid,'part':'status,processingDetails'},headers={'Authorization':'Bearer '+token},timeout=30);r.raise_for_status();video=r.json()['items'][0];print('YouTube',video,flush=True)
 if video.get('processingDetails',{}).get('processingStatus')=='succeeded':break
 time.sleep(10)
assert video['status']['privacyStatus']=='private';assert video['status']['publishAt']=='2026-09-08T17:00:00Z';assert video['processingDetails']['processingStatus']=='succeeded'
(p/'publication-verified.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'workflow_id':run['id'],'workflow_conclusion':run['conclusion'],'item_id':item['id'],'youtube':video},indent=2))
# Explicit refresh also captures the publisher's new calendar state.
started=datetime.datetime.now(datetime.timezone.utc).isoformat();r=requests.post(base+'/actions/workflows/refresh-handoff.yml/dispatches',headers=headers,json={'ref':'main'},timeout=30);r.raise_for_status();print('Refresh handoff dispatched',r.status_code,flush=True)
for _ in range(40):
 r=requests.get(base+'/actions/workflows/refresh-handoff.yml/runs',headers=headers,params={'per_page':10},timeout=30);r.raise_for_status();runs=[x for x in r.json()['workflow_runs'] if x['event']=='workflow_dispatch' and x['created_at']>=started[:19]+'Z']
 if runs and runs[0]['status']=='completed':
  assert runs[0]['conclusion']=='success';(p/'handoff-verified.json').write_text(json.dumps({'run_id':runs[0]['id'],'conclusion':runs[0]['conclusion'],'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2));print('Handoff success',flush=True);break
 time.sleep(10)
else:raise TimeoutError('Handoff refresh not yet confirmed')
