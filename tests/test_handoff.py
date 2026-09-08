import importlib.util,unittest,tempfile,json,subprocess,hashlib,shlex
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def module(name,file):
 s=importlib.util.spec_from_file_location(name,ROOT/'tools'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
b=module('handoff_builder','build-handoff.py');i=module('handoff_installer','install-handoff.py')
class HandoffTests(unittest.TestCase):
 def test_shell_quote_roundtrip(self):
  value="synthetic'quote $literal and spaces#";raw=('FISH_API_KEY='+shlex.quote(value)+'\n').encode()
  self.assertEqual(b.parse_env(raw)['FISH_API_KEY'],value);self.assertEqual(i.parse_env(raw)['FISH_API_KEY'],value)
 def test_bad_duplicate_rejected(self):
  with self.assertRaises(ValueError):i.parse_env(b'FISH_API_KEY=a\nFISH_API_KEY=b\n')
 def test_fixed_salt_and_roundtrip(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'credentials').mkdir()
   with patch.object(b,'ROOT',root):
    enc=b.openssl(b'Synthetic test payload','TEST-password')
    self.assertEqual(enc[:8],b'Salted__');self.assertEqual(b.openssl(enc,'TEST-password',True),b'Synthetic test payload')
    key=hashlib.pbkdf2_hmac('sha256',b'TEST-password',enc[8:16],600000,48)
    p=subprocess.run(['openssl','enc','-d','-aes-256-cbc','-nosalt','-K',key[:32].hex(),'-iv',key[32:].hex()],input=enc[16:],capture_output=True)
    self.assertEqual(p.returncode,0);self.assertEqual(p.stdout,b'Synthetic test payload')
 def fixture(self,tmp):
  root=Path(tmp)/'repo';root.mkdir();subprocess.run(['git','init','-q',str(root)],check=True);(root/'.gitignore').write_text('.env\ncredentials/\n');(root/'config').mkdir();(root/'config/channels.json').write_text(json.dumps({'channels':[{'id':'stiles-psychology','youtube':{'channel_id':'TEST-channel'}}]}));bundle=Path(tmp)/'bundle';bundle.mkdir();env={'YOUTUBE_STILES_CLIENT_ID':'TEST-id','YOUTUBE_STILES_CLIENT_SECRET':'TEST-secret','YOUTUBE_STILES_REFRESH_TOKEN':'TEST-refresh'};(bundle/'credentials.env').write_text('\n'.join(k+'='+v for k,v in env.items()));(bundle/'youtube-client.json').write_text(json.dumps({'installed':{'client_id':'TEST-id','client_secret':'TEST-secret'}}));(bundle/'youtube-token.json').write_text(json.dumps({'channel':{'id':'TEST-channel'},'client_id':'TEST-id','token':{'refresh_token':'TEST-refresh'}}));return root,bundle
 def test_install_dryrun_permissions_merge(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,bundle=self.fixture(tmp);(root/'.env').write_text('EXISTING_SETTING=keep\n');i.install(bundle,root);self.assertFalse((root/'.git/credentials').exists());i.install(bundle,root,True);self.assertEqual(i.parse_env((root/'.env').read_bytes())['EXISTING_SETTING'],'keep');self.assertEqual((root/'.env').stat().st_mode&0o777,0o600);i.install(bundle,root,True)
 def test_conflict_refuses_all_writes(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,bundle=self.fixture(tmp);(root/'.env').write_text('YOUTUBE_STILES_REFRESH_TOKEN=DIFFERENT\n')
   with self.assertRaises(ValueError):i.install(bundle,root,True)
   self.assertFalse((root/'.git/credentials').exists())
 def test_symlink_refused(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,bundle=self.fixture(tmp);outside=Path(tmp)/'outside';outside.write_text('untouched');(root/'.env').symlink_to(outside)
   with self.assertRaises(ValueError):i.install(bundle,root,True)
   self.assertEqual(outside.read_text(),'untouched')
 def test_unignored_refused(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,bundle=self.fixture(tmp);(root/'.gitignore').write_text('')
   with self.assertRaises(ValueError):i.install(bundle,root,True)
 def test_start_document_is_current_source(self):
  code=(ROOT/'tools/build-handoff.py').read_text();self.assertIn("(ROOT/'START_HERE.md').read_text()",code);self.assertIn('Install the supplied secrets locally now',(ROOT/'START_HERE.md').read_text())
