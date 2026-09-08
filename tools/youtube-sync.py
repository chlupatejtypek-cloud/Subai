#!/usr/bin/env python3
"""Read-only YouTube reconciliation; only the local calendar/Git is mutated."""
import importlib.util,json,argparse
from pathlib import Path
import requests
s=importlib.util.spec_from_file_location('publisher',Path(__file__).with_name('youtube-publish.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def reconcile(item,video,checked):
 item['last_status_check_at']=checked
 if video is None:
  item['status']='needs_reconciliation';item['reconciliation_reason']='Known video ID absent from authenticated lookup; never retry upload automatically';return
 status=video.get('status',{});processing=video.get('processingDetails',{}).get('processingStatus');privacy=status.get('privacyStatus');schedule=status.get('publishAt')
 item['remote_status']={'privacy':privacy,'publish_at':schedule,'upload_status':status.get('uploadStatus'),'processing_status':processing}
 item['remote_schedule_still_active']=bool(schedule)
 if status.get('uploadStatus') in ('failed','rejected','deleted') or processing in ('failed','terminated'):
  item['status']='needs_reconciliation';item['reconciliation_reason']='Remote processing/upload failure';return
 if privacy=='public' and status.get('uploadStatus')=='processed':
  item['status']='published';item.setdefault('first_observed_public_at',checked)
 elif privacy=='private' and schedule:item['status']='scheduled'
 elif privacy=='private':item['status']='uploaded_private'
 elif privacy=='unlisted':item['status']='uploaded_unlisted'
 else:item['status']='needs_reconciliation'
 review=item.get('owner_review') or {}
 held=bool(item.get('publication_hold') or (isinstance(review,dict) and review.get('status')=='rejected'))
 item['release_alert']= 'Owner-held video is public or still scheduled; external action required' if held and (privacy=='public' or schedule) else None
 if item['status']!='needs_reconciliation':item.pop('reconciliation_reason',None)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');ap.add_argument('--commit-state',action='store_true');a=ap.parse_args()
 if a.commit_state and not a.apply:raise ValueError('--commit-state requires --apply')
 c,_=p.config('stiles-psychology');path=p.ROOT/c['publishing']['calendar'];data=p.read(path);token=p.access_token(c);ids=list(dict.fromkeys(x['youtube_video_id'] for x in data['items'] if x.get('youtube_video_id')));found={}
 for offset in range(0,len(ids),50):
  r=requests.get('https://www.googleapis.com/youtube/v3/videos',headers={'Authorization':'Bearer '+token},params={'id':','.join(ids[offset:offset+50]),'part':'status,processingDetails'},timeout=30)
  if r.status_code!=200:raise ValueError('YouTube read failed HTTP '+str(r.status_code)+'; calendar unchanged')
  found.update({v['id']:v for v in r.json()['items']})
 checked=p.now().isoformat()
 for item in data['items']:
  if item.get('youtube_video_id'):reconcile(item,found.get(item['youtube_video_id']),checked)
 data['last_remote_sync_at']=checked
 if a.apply:p.persist(path,data,'calendar: reconcile actual YouTube publication state',a.commit_state)
 print(json.dumps({'mode':'applied' if a.apply else 'dry_run','checked_at':checked,'items':[{'id':x['id'],'status':x['status'],'alert':x.get('release_alert')} for x in data['items'] if x.get('youtube_video_id')]}))
if __name__=='__main__':
 try:main()
 except Exception as e:print('ERROR:',str(e) if isinstance(e,ValueError) else type(e).__name__);raise SystemExit(1)
