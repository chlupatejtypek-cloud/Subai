import os,json,base64,requests,re
from pathlib import Path
p=Path(__file__).parent
text=(p/'narration.txt').read_text().strip()
r=requests.post('https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB/with-timestamps',headers={'xi-api-key':os.environ['ELEVENLABS_API_KEY']},json={'text':text,'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.5,'similarity_boost':0.75,'style':0.15,'use_speaker_boost':True}},timeout=120)
if r.status_code!=200:raise SystemExit('ElevenLabs HTTP '+str(r.status_code)+' '+r.text[:350])
d=r.json();(p/'audio/adam.mp3').write_bytes(base64.b64decode(d.pop('audio_base64')));(p/'audio/alignment.json').write_text(json.dumps(d))
a=d.get('normalized_alignment') or d['alignment'];chars=a['characters'];ss=a['character_start_times_seconds'];ee=a['character_end_times_seconds'];words=[]
for m in re.finditer(r'\S+',''.join(chars)):
 words.append({'text':m.group(),'start':ss[m.start()],'end':ee[m.end()-1]})
(p/'audio/words-original.json').write_text(json.dumps({'words':words},indent=2));print('Generated Adam:',len(words),'words, alignment end',ee[-1])
