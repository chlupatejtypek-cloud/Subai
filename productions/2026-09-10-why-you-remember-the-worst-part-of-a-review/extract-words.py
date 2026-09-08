from pathlib import Path
import json,re
p=Path(__file__).resolve().parent;d=json.loads((p/'audio/source.opus.timestamps.json').read_text());chunks={}
for c in d['alignment_chunks']:
 key=c['chunk_seq']
 if key not in chunks or len(c['alignment']['segments'])>=len(chunks[key]['alignment']['segments']):chunks[key]=c
words=[{'text':w['text'],'start':w['start']+c['chunk_audio_offset_sec'],'end':w['end']+c['chunk_audio_offset_sec']} for c in sorted(chunks.values(),key=lambda c:c['chunk_seq']) for w in c['alignment']['segments']]
norm=lambda s:re.findall(r"[a-z]+(?:'[a-z]+)?",s.lower())
assert norm(' '.join(w['text'] for w in words))==norm((p/'narration.txt').read_text())
assert all(words[i]['start']<=words[i+1]['start'] for i in range(len(words)-1))
(p/'audio/words-original.json').write_text(json.dumps({'words':words,'note':'Retain most complete alignment per chunk_seq; streaming updates are not separate spoken segments.'},indent=2));print('Canonical words:',len(words))
