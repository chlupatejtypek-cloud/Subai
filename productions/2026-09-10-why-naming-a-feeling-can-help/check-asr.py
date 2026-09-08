from pathlib import Path
import json,re,difflib
from faster_whisper import WhisperModel
p=Path(__file__).resolve().parent;m=WhisperModel('base.en',device='cpu',compute_type='int8');segs,info=m.transcribe(str(p/'audio/narration.wav'),beam_size=5,language='en');s=' '.join(x.text.strip() for x in segs);norm=lambda x:re.findall(r"[a-z]+(?:'[a-z]+)?",x.lower());a=norm((p/'narration.txt').read_text());b=norm(s);d={'transcript':s,'expected_words':len(a),'actual_words':len(b),'exact_match':a==b,'similarity':difflib.SequenceMatcher(None,a,b).ratio(),'diff':list(difflib.unified_diff(a,b))};(p/'asr-qc.json').write_text(json.dumps(d,indent=2));print(json.dumps(d))
