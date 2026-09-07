#!/usr/bin/env python3
import json
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'calendar/2026-09-07_2026-10-06.json'
d=json.loads(p.read_text());now=datetime.now(timezone.utc)
print('# Stiles Psychology — calendar status\n')
print('Period:',d['start_date'],'through',d['end_date'],'| target:',len(d['items']),'videos\n')
for k,v in sorted(Counter(x['status'] for x in d['items']).items()):print(f'- **{k}**: {v}')
print('\n## Overdue unfinished slots\n')
late=[x for x in d['items'] if datetime.fromisoformat(x['publish_at_utc'].replace('Z','+00:00'))<now and x['status'] not in ('scheduled','published','cancelled')]
for x in late:print(f"- {x['id']}: {x['title']} — {x['status']}; manual rescheduling required")
if not late:print('None.')
print('\nA calendar entry is not a generated video. No asset is uploaded until it is ready and passes all quality gates. Exact YouTube public-upload eligibility and long-term OAuth validity still depend on Google project settings.')
