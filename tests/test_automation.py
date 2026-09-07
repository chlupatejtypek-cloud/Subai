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
  items=self.data['items'];self.assertEqual(len(items),90);self.assertEqual(len({x['id'] for x in items}),90);self.assertEqual(len({x['title'] for x in items}),90)
  days=Counter(x['scheduled_at'][:10] for x in items);self.assertEqual(len(days),30);self.assertTrue(all(v==3 for v in days.values()))
  for x in items:self.assertEqual(p.dt(x['scheduled_at']),p.dt(x['publish_at_utc']));self.assertLessEqual(len(x['title']),60)
 def test_planned_cannot_upload(self):
  item=dict(self.data['items'][0]);item['status']='planned';item['publish_at_utc']=(p.now()+timedelta(hours=2)).isoformat();self.assertFalse(p.eligible(item,self.c,p.now()))
 def test_overdue_cannot_upload(self):
  item=dict(self.data['items'][0]);item['status']='ready';item['publish_at_utc']=(p.now()-timedelta(minutes=1)).isoformat();self.assertFalse(p.eligible(item,self.c,p.now()))
 def test_ambiguous_cannot_retry(self):
  item=dict(self.data['items'][0]);item['status']='needs_reconciliation';item['publish_at_utc']=(p.now()+timedelta(hours=2)).isoformat();self.assertFalse(p.eligible(item,self.c,p.now()))
 def test_unverified_content_blocked(self):
  with self.assertRaises(ValueError):p.validate(self.data['items'][0],self.c,self.cloud)
 def test_new_voice(self):
  self.assertEqual(self.c['voice']['provider'],'fish_audio');self.assertEqual(self.c['voice']['reference_id'],'fb7ec16ca51a45a5a4db881244d7990a')
 def test_no_plaintext_secret_fields(self):
  d=p.read(ROOT/'config/channels.json');text=json.dumps(d)
  for prefix in ('ghp_','ya29.','-----BEGIN PRIVATE KEY-----'):self.assertNotIn(prefix,text)
if __name__=='__main__':unittest.main()
