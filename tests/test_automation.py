import importlib.util,json,unittest
from pathlib import Path
from datetime import datetime,timedelta,timezone
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('publisher',ROOT/'tools/youtube-publish.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class AutomationTests(unittest.TestCase):
 def setUp(self):
  self.data=p.read(ROOT/'calendar/2026-09-07_2026-10-06.json');self.c,self.cloud=p.config('stiles-psychology')
 def test_calendar(self):
  items=self.data['items'];self.assertEqual(len(items),90);self.assertEqual(len({x['id'] for x in items}),90);active=[x for x in items if x['status'] not in {'missed','cancelled'}];self.assertEqual(len({x['title'] for x in active}),len(active))
  days=Counter(x['scheduled_at'][:10] for x in items);self.assertEqual(len(days),30);self.assertTrue(all(v==3 for v in days.values()))
  for x in items:self.assertEqual(p.dt(x['scheduled_at']),p.dt(x['publish_at_utc']));self.assertLessEqual(len(x['title']),60)
 def test_missed_cannot_upload(self):
  item=dict(self.data['items'][0]);item['status']='missed';item['publish_at_utc']=(p.now()+timedelta(hours=2)).isoformat();self.assertFalse(p.eligible(item,self.c,p.now()))
 def test_planned_cannot_upload(self):
  item=dict(self.data['items'][0]);item['status']='planned';item['publish_at_utc']=(p.now()+timedelta(hours=2)).isoformat();self.assertFalse(p.eligible(item,self.c,p.now()))
 def test_overdue_cannot_upload(self):
  item=dict(self.data['items'][0]);item['status']='ready';item['publish_at_utc']=(p.now()-timedelta(minutes=1)).isoformat();self.assertFalse(p.eligible(item,self.c,p.now()))
 def test_ambiguous_cannot_retry(self):
  item=dict(self.data['items'][0]);item['status']='needs_reconciliation';item['publish_at_utc']=(p.now()+timedelta(hours=2)).isoformat();self.assertFalse(p.eligible(item,self.c,p.now()))
 def test_unverified_content_blocked(self):
  item=dict(self.data['items'][0]);item['research_status']='pending'
  with self.assertRaises(ValueError):p.validate(item,self.c,self.cloud)
 def test_new_voice(self):
  self.assertEqual(self.c['voice']['provider'],'fish_audio');self.assertEqual(self.c['voice']['reference_id'],'fb7ec16ca51a45a5a4db881244d7990a')
 def test_no_plaintext_secret_fields(self):
  d=p.read(ROOT/'config/channels.json');text=json.dumps(d)
  for prefix in ('ghp_','ya29.','-----BEGIN PRIVATE KEY-----'):self.assertNotIn(prefix,text)
if __name__=='__main__':unittest.main()

class UploadModeTests(unittest.TestCase):
 def check_mode(self,immediate):
  from unittest.mock import patch,MagicMock
  import tempfile
  c,_=p.config('stiles-psychology')
  item={'title':'A Test Title','description':'Educational example.','publish_at_utc':'2026-10-01T12:00:00Z'}
  init=MagicMock(status_code=200,headers={'Location':'https://www.googleapis.com/upload/test-session'})
  done=MagicMock(status_code=200);done.json.return_value={'id':'test-id','status':{'privacyStatus':'public' if immediate else 'private'}}
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'v.mp4';path.write_bytes(b'x')
   with patch.object(p.requests,'post',return_value=init) as post,patch.object(p.requests,'put',return_value=done):
    result=p.upload(item,c,'TEST-NOT-A-TOKEN',path,1,immediate=immediate)
    sent=post.call_args.kwargs['json']['status']
    self.assertEqual(sent['privacyStatus'],'public' if immediate else 'private')
    self.assertEqual('publishAt' in sent,not immediate)
    self.assertEqual(result['id'],'test-id')
 def test_immediate_omits_schedule(self):self.check_mode(True)
 def test_default_keeps_private_schedule(self):self.check_mode(False)
