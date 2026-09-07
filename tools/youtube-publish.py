#!/usr/bin/env python3
"""Fail-closed scheduled publisher. Does not research, generate media, or invent QA.
Public state is committed BEFORE upload, so an interrupted upload cannot silently
create a duplicate. Ambiguous uploads require reconciliation, not blind retries.
"""
import argparse,hashlib,json,os,subprocess,tempfile
from datetime import datetime,timedelta,timezone
from pathlib import Path
from urllib.parse import urlparse
import requests
ROOT=Path(__file__).resolve().parents[1]
REQUIRED_QA=('research_verified','script_verified','voice_verified','character_verified','full_bleed','captions_aligned','captions_no_overlap','audio_verified','visual_review_passed','rights_verified')
def now():return datetime.now(timezone.utc)
def dt(value):return datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(timezone.utc)
def read(path):return json.loads(Path(path).read_text())
def config(channel_id):
 registry=read(ROOT/'config/channels.json')
 for c in registry['channels']:
  if c['id']==channel_id:return c,registry['cloudinary_accounts'][c['cloudinary_account']]
 raise ValueError('Channel is not registered')
def eligible(item,c,t):
 p=c['publishing']
 return item['status']=='ready' and t+timedelta(minutes=p['minimum_lead_minutes'])<=dt(item['publish_at_utc'])<=t+timedelta(hours=p['schedule_lookahead_hours'])
def validate(item,c,cloud):
 if item['channel_id']!=c['id']:raise ValueError('Channel mismatch')
 if not c['active'] or not c['publishing']['enabled']:raise ValueError('Publishing disabled')
 if not (1<=len(item['title'])<=60):raise ValueError('Title must have 1–60 characters')
 if not item.get('description') or len(item['description'])>5000:raise ValueError('Missing/long description')
 sources=item.get('research_sources',[])
 if item.get('research_status')!='verified' or len(sources)<2:raise ValueError('Research not verified with primary and corroborating sources')
 if not all(isinstance(s,str) and s.startswith('https://') for s in sources):raise ValueError('Invalid research links')
 qa=item.get('qa') or {}
 if any(qa.get(k) is not True for k in REQUIRED_QA):raise ValueError('Incomplete quality gate')
 if not qa.get('reviewed_by') or not qa.get('reviewed_at'):raise ValueError('Missing review provenance')
 if qa.get('voice_provider')!=c['voice']['provider'] or qa.get('voice_reference_id')!=c['voice']['reference_id']:raise ValueError('Narration provider or voice does not match current channel')
 if not 1<=qa.get('source_image_count',0)<=c['format']['max_generated_images']:raise ValueError('Invalid source image count')
 u=urlparse(item.get('asset_url') or '')
 if u.scheme!='https' or u.netloc!='res.cloudinary.com' or not u.path.startswith('/'+cloud['cloud_name']+'/video/upload/') or not u.path.lower().endswith('.mp4') or u.query:raise ValueError('Final asset must be an approved Cloudinary MP4 URL')
 digest=item.get('asset_sha256') or ''
 if len(digest)!=64 or any(x not in '0123456789abcdef' for x in digest):raise ValueError('Missing SHA256')
 if not 0<float(item.get('duration_seconds') or 0)<=c['format']['max_seconds']:raise ValueError('Duration over limit or absent')
def access_token(c):
 y=c['youtube']
 cid=os.environ.get(y['oauth_client_id_secret']);secret=os.environ.get(y['oauth_client_secret_secret']);refresh=os.environ.get(y['oauth_refresh_token_secret'])
 if not (cid and secret and refresh):
  client=read(ROOT/'credentials/youtube-client.json')['installed'];local=read(ROOT/'.git/credentials')
  if local.get('channel',{}).get('id')!=y['channel_id']:raise ValueError('Local token does not match requested channel')
  cid,secret,refresh=client['client_id'],client['client_secret'],local['token']['refresh_token']
 r=requests.post('https://oauth2.googleapis.com/token',data={'client_id':cid,'client_secret':secret,'refresh_token':refresh,'grant_type':'refresh_token'},timeout=40)
 if r.status_code!=200:raise ValueError('OAuth refresh failed HTTP '+str(r.status_code)+'; reauthorization may be required')
 t=r.json()['access_token'];r=requests.get('https://www.googleapis.com/youtube/v3/channels',params={'part':'id','mine':'true'},headers={'Authorization':'Bearer '+t},timeout=30)
 if r.status_code!=200 or y['channel_id'] not in [x['id'] for x in r.json().get('items',[])]:raise ValueError('Authenticated YouTube channel ID mismatch')
 return t
def persist(path,data,message,commit):
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');tmp.replace(path)
 if commit:
  relative=str(path.relative_to(ROOT));subprocess.run(['git','add',relative],cwd=ROOT,check=True)
  subprocess.run(['git','-c','user.name=Subai Publisher','-c','user.email=subai-publisher@users.noreply.github.com','commit','-m',message],cwd=ROOT,check=True)
  # Checkout's temporary GITHUB_TOKEN credentials are used only by Git, never printed here.
  subprocess.run(['git','push','origin','HEAD:main'],cwd=ROOT,check=True)
def download(item,path,c):
 with requests.get(item['asset_url'],stream=True,timeout=60,allow_redirects=False) as r:
  if r.status_code!=200:raise ValueError('Asset fetch failed HTTP '+str(r.status_code))
  total=0;sha=hashlib.sha256()
  with path.open('wb') as f:
   for chunk in r.iter_content(1024*1024):
    total+=len(chunk)
    if total>150*1024*1024:raise ValueError('Short exceeds 150MB input limit')
    sha.update(chunk);f.write(chunk)
 if sha.hexdigest()!=item['asset_sha256']:raise ValueError('Final asset checksum mismatch')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 v=next(x for x in probe['streams'] if x['codec_type']=='video');audio=any(x['codec_type']=='audio' for x in probe['streams']);duration=float(probe['format']['duration']);num,den=map(float,v['r_frame_rate'].split('/'))
 if v['width']!=1080 or v['height']!=1920 or abs(num/den-30)>.01 or not audio or not 0<duration<=40.001:raise ValueError('Final file failed technical QC')
 if abs(duration-float(item['duration_seconds']))>.1:raise ValueError('Duration does not match signed-off final')
 return total
def upload(item,c,token,path,size):
 body={'snippet':{'title':item['title'],'description':item['description'],'categoryId':c['youtube']['category_id'],'defaultLanguage':c['language'],'defaultAudioLanguage':c['language']},'status':{'privacyStatus':'private','publishAt':item['publish_at_utc'],'selfDeclaredMadeForKids':c['youtube']['made_for_kids'],'containsSyntheticMedia':True}}
 headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','X-Upload-Content-Type':'video/mp4','X-Upload-Content-Length':str(size)}
 r=requests.post('https://www.googleapis.com/upload/youtube/v3/videos',params={'uploadType':'resumable','part':'snippet,status'},headers=headers,json=body,timeout=45)
 if r.status_code not in (200,201):raise ValueError('Upload initialization HTTP '+str(r.status_code))
 url=r.headers.get('Location','');parsed=urlparse(url)
 if parsed.scheme!='https' or not (parsed.hostname=='www.googleapis.com' or (parsed.hostname or '').endswith('.googleapis.com')):raise ValueError('Unexpected upload session host')
 # Session URL is sensitive and is never recorded in logs or public state.
 with path.open('rb') as f:r=requests.put(url,data=f,headers={'Authorization':'Bearer '+token,'Content-Type':'video/mp4','Content-Length':str(size)},timeout=240)
 if r.status_code not in (200,201):raise ValueError('Upload completion HTTP '+str(r.status_code)+'; reconcile before retrying')
 result=r.json()
 if not result.get('id'):raise ValueError('Upload completed without a video ID; reconcile')
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--calendar',default='calendar/2026-09-07_2026-10-06.json');ap.add_argument('--execute',action='store_true');ap.add_argument('--commit-state',action='store_true');ap.add_argument('--verify-auth',action='store_true');args=ap.parse_args()
 path=ROOT/args.calendar;data=read(path);c,cloud=config(data['channel_id']);t=now()
 if args.verify_auth:access_token(c);print('OAuth refresh + channel ID verification passed');return
 candidates=[x for x in data['items'] if eligible(x,c,t)];late=[x for x in data['items'] if x['status'] in ('planned','researching','scripted','producing','ready') and dt(x['publish_at_utc'])<t]
 print(json.dumps({'planned_items':len(data['items']),'ready_in_window':[x['id'] for x in candidates],'overdue':[x['id'] for x in late],'ambiguous_uploads':[x['id'] for x in data['items'] if x['status'] in ('upload_started','needs_reconciliation')],'mode':'execute' if args.execute else 'dry_run'}))
 for item in candidates:
  validate(item,c,cloud)
  if not args.execute:continue
  token=access_token(c)
  with tempfile.TemporaryDirectory() as tmp:
   video=Path(tmp)/'video.mp4';size=download(item,video,c)
   # Recheck timing after downloads; never silently publish an overdue video immediately.
   if not eligible(item,c,now()):raise ValueError('Scheduling window elapsed during preflight')
   item['status']='upload_started';item['upload_started_at']=now().isoformat()
   persist(path,data,'publish: reserve '+item['id']+' before upload',args.commit_state)
   try:
    result=upload(item,c,token,video,size);item['youtube_video_id']=result['id'];item['youtube_url']='https://www.youtube.com/watch?v='+result['id']
    status=result.get('status',{});item['api_returned_publish_at']=status.get('publishAt');item['api_returned_privacy']=status.get('privacyStatus');item['uploaded_at']=now().isoformat()
    item['status']='scheduled' if status.get('publishAt') and dt(status['publishAt'])==dt(item['publish_at_utc']) and status.get('privacyStatus')=='private' else 'needs_reconciliation'
    persist(path,data,'publish: record '+item['id']+' '+item['status'],args.commit_state)
   except Exception:
    item['status']='needs_reconciliation';item['error']='Upload was attempted but completion/scheduling is uncertain. Inspect the channel before any retry.'
    persist(path,data,'publish: reconcile '+item['id'],args.commit_state)
    raise ValueError('Upload outcome uncertain; automatic duplicate retry disabled') from None
if __name__=='__main__':
 try:main()
 except Exception as e:
  # Never print requests exception URLs, request bodies or tokens.
  if isinstance(e,ValueError):print('ERROR:',str(e))
  else:print('ERROR: operation failed; type='+type(e).__name__)
  raise SystemExit(1)
