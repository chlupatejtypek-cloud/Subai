import unittest,importlib.util,copy
from pathlib import Path
from datetime import datetime,timezone,timedelta
ROOT=Path(__file__).resolve().parents[1]
def load(name,file):
 s=importlib.util.spec_from_file_location(name,ROOT/'tools'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sync=load('sync','youtube-sync.py');start=load('start','start-next.py');p=sync.p
class WorkflowTests(unittest.TestCase):
 def test_public_verified(self):
  x={'status':'scheduled','youtube_video_id':'test'};sync.reconcile(x,{'status':{'privacyStatus':'public','uploadStatus':'processed'}},'2026-09-08T10:00:00Z');self.assertEqual(x['status'],'published');self.assertIn('first_observed_public_at',x)
 def test_clock_not_publication(self):
  x={};sync.reconcile(x,{'status':{'privacyStatus':'private','publishAt':'2020-01-01T00:00:00Z'}},'now');self.assertEqual(x['status'],'scheduled')
 def test_missing_keeps_id(self):
  x={'youtube_video_id':'test'};sync.reconcile(x,None,'now');self.assertEqual(x['youtube_video_id'],'test');self.assertEqual(x['status'],'needs_reconciliation')
 def test_rejected_schedule_alert(self):
  x={'publication_hold':True};sync.reconcile(x,{'status':{'privacyStatus':'private','publishAt':'future'}},'now');self.assertTrue(x['release_alert']);self.assertTrue(x['publication_hold'])
 def test_private_not_cancel_claim(self):
  x={};sync.reconcile(x,{'status':{'privacyStatus':'private'}},'now');self.assertEqual(x['status'],'uploaded_private')
 def test_select_skips_existing(self):
  now=datetime.now(timezone.utc);base={'publish_at_utc':(now+timedelta(days=10)).isoformat()};data={'last_remote_sync_at':now.isoformat(),'items':[{**base,'id':'ready','status':'ready'},{**base,'id':'uploaded','status':'planned','youtube_video_id':'test'},{**base,'id':'next','status':'planned','production_path':'productions/nonexistent-planned-placeholder'}]};self.assertEqual(start.select(data,now)[0]['id'],'next')
 def test_stale_sync_blocks(self):
  with self.assertRaises(ValueError):start.select({'items':[]},datetime.now(timezone.utc))
 def test_resume(self):
  now=datetime.now(timezone.utc);data={'last_remote_sync_at':now.isoformat(),'items':[{'id':'a','status':'producing'}]};self.assertTrue(start.select(data,now)[1])
 def fixture(self):
  c,cloud=p.config('stiles-psychology');x=p.read(ROOT/c['publishing']['calendar'])['items'][0];x.pop('youtube_video_id',None);x['duration_seconds']=50;x['qa'].update(source_image_count=10,creative_contract_version=2,explanatory_ui_verified=True,opening_video_verified=True,opening_zoom_verified=True,character_proportions_verified=True,visual_coverage_verified=True,longest_illustration_hold_seconds=7);return x,c,cloud
 def test_new_format_valid(self):p.validate(*self.fixture())
 def test_short_rejected(self):
  x,c,cloud=self.fixture();x['duration_seconds']=39
  with self.assertRaises(ValueError):p.validate(x,c,cloud)
 def test_long_rejected(self):
  x,c,cloud=self.fixture();x['duration_seconds']=61
  with self.assertRaises(ValueError):p.validate(x,c,cloud)
 def test_nine_images_rejected(self):
  x,c,cloud=self.fixture();x['qa']['source_image_count']=9
  with self.assertRaises(ValueError):p.validate(x,c,cloud)
 def test_existing_id_blocks(self):
  x,c,cloud=self.fixture();x['youtube_video_id']='test'
  with self.assertRaises(ValueError):p.validate(x,c,cloud)

 def test_headings_not_enough(self):
  x,c,cloud=self.fixture();x['qa']['explanatory_ui_verified']=False
  with self.assertRaises(ValueError):p.validate(x,c,cloud)
