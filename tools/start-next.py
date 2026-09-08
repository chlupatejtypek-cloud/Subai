#!/usr/bin/env python3
"""Agent workflow reservation, not a hosted media generation engine. Sync first."""
import importlib.util,json,argparse
from pathlib import Path
s=importlib.util.spec_from_file_location('publisher',Path(__file__).with_name('youtube-publish.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def select(data,t):
 synced=data.get('last_remote_sync_at')
 if not synced or not 0<=(t-p.dt(synced)).total_seconds()<=600:raise ValueError('Run youtube-sync.py --apply successfully first; sync must be under10minutes old')
 active=[x for x in data['items'] if x['status'] in ('researching','scripted','producing') and not x.get('youtube_video_id') and not x.get('publication_hold')]
 if len(active)>1:raise ValueError('Multiple unfinished productions; reconcile active reservation before starting another')
 if active:return active[0],True
 candidates=[x for x in data['items'] if x['status']=='planned' and not x.get('asset_url') and not (x.get('production_path') and (p.ROOT/x['production_path']).exists()) and not x.get('youtube_video_id') and not x.get('publication_hold') and p.dt(x['publish_at_utc'])>t]
 if not candidates:raise ValueError('No future unproduced calendar slot; extend/replan calendar without backdating')
 return min(candidates,key=lambda x:p.dt(x['publish_at_utc'])),False
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');ap.add_argument('--commit-state',action='store_true');a=ap.parse_args()
 if a.commit_state and not a.apply:raise ValueError('--commit-state requires --apply')
 c,_=p.config('stiles-psychology');path=p.ROOT/c['publishing']['calendar'];data=p.read(path);item,resume=select(data,p.now())
 if a.apply and not resume:
  item['status']='researching';item['production_path']=item.get('production_path') or 'productions/'+item['id'].lower();item['workflow']={'stage':1,'stage_name':'research','started_at':p.now().isoformat(),'contract':'40–60 seconds;10–15 distinct used illustrations','next_action':'Read RETENTION-RESEARCH.md; compare3 angles; verify primary evidence before scripting'}
  p.persist(path,data,'production: reserve '+item['id']+' for research',a.commit_state)
 print(json.dumps({'mode':'applied' if a.apply else 'dry_run','resume':resume,'item':item['id'],'topic_proposal':item['title'],'instructions':'START-WORKFLOW.md','action':'Continue agent production now; do not stop at reservation or ask routine topic approval'}))
if __name__=='__main__':
 try:main()
 except Exception as e:print('ERROR:',str(e) if isinstance(e,ValueError) else type(e).__name__);raise SystemExit(1)
