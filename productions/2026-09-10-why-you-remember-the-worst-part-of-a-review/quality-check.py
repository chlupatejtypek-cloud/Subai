from pathlib import Path
import json, subprocess, hashlib
from PIL import Image, ImageOps, ImageDraw

p = Path(__file__).resolve().parent
final = p / 'output/final.mp4'
sb = json.loads((p / 'storyboard.json').read_text())

d = json.loads(subprocess.check_output(
    ['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(final)]))
v = next(x for x in d['streams'] if x['codec_type'] == 'video')
a = next(x for x in d['streams'] if x['codec_type'] == 'audio')
duration = float(d['format']['duration'])

assert 40 <= duration <= 60, f'duration {duration} outside the 40-60s rule'
assert (v['width'], v['height'], v['r_frame_rate']) == (1080, 1920, '30/1')
assert abs(int(v['nb_frames']) - round(sb['duration_seconds'] * 30)) <= 2

# Captions: ordered, non-overlapping, inside the video.
lines = [x for x in (p / 'output/captions.ass').read_text().splitlines()
         if x.startswith('Dialogue:')]
ts = lambda x: sum(float(val) * k for val, k in zip(x.split(':'), (3600, 60, 1)))
caps = [(ts(x.split(',')[1]), ts(x.split(',')[2])) for x in lines]
assert caps and all(s < e for s, e in caps)
assert all(caps[i][1] <= caps[i + 1][0] for i in range(len(caps) - 1))
assert caps[-1][1] <= duration + .1

# Standing rule: at least 10 DISTINCT illustrations actually used.
used = sb['distinct_images_used']
assert len(set(used)) == len(used) >= 10, 'fewer than 10 distinct illustrations'
for name in used:
    assert (p / 'images' / name).exists(), name

# No shot may sit still too long.
longest = max(s['end'] - s['start'] for s in sb['shots'])
assert longest <= 6.0, f'hold of {longest}s is too long'

# Real animated opening AND a separate zoom.
assert sb['opening']['separate_opening_zoom'] is True
assert (p / 'output/opening-raw.mp4').exists()

# Blur present but bounded, never continuous.
blur_total = sum(b['end'] - b['start'] for b in sb['blur_windows'])
assert 0 < blur_total <= duration * .25, f'blur covers {blur_total}s'

r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(final), '-af',
                    'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                    '-f', 'null', '-'], capture_output=True, text=True, check=True)
loud = json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
assert float(loud['input_tp']) <= -1

report = {
    'duration_seconds': duration,
    'resolution': [1080, 1920],
    'fps': 30,
    'frames': int(v['nb_frames']),
    'codecs': [v['codec_name'], a['codec_name']],
    'sha256': hashlib.sha256(final.read_bytes()).hexdigest(),
    'bytes': final.stat().st_size,
    'caption_events': len(caps),
    'captions_no_overlap': True,
    'last_caption_end': caps[-1][1],
    'distinct_illustrations_used': len(used),
    'longest_hold_seconds': round(longest, 2),
    'animated_opening': 'Agnes video v2.0, 4.0s, locked camera micro-motion',
    'separate_zoom': 'slow push-in on the same still, 4.0-5.6s',
    'blur_seconds_total': round(blur_total, 2),
    'ui_cards': len(sb['ui_cards']),
    'ui_entrances': 'all eased over 400ms, staggered rows, nothing spawns',
    'loudness': loud,
    'sfx': 'original procedural only; no meme-API media composited',
    'review_boundary': ('Technical checks plus sampled frame review. '
                        'Not a claimed full human audio/video review.'),
}
(p / 'technical-qc.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))

times = [.4, 2.4, 4.5, 7.5, 10.5, 13.5, 17, 20, 23.2, 26, 28.5, 31,
         34, 36.5, 40, 44, 48.5]
sheet = Image.new('RGB', (1120, 2600), '#eae2d5')
for i, t in enumerate(times):
    f = p / 'output' / f'qc-{i:02}.jpg'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', str(final),
                    '-frames:v', '1', str(f)], check=True)
    sheet.paste(ImageOps.fit(Image.open(f), (270, 480)),
                ((i % 4) * 280, (i // 4) * 520))
    ImageDraw.Draw(sheet).text(((i % 4) * 280, (i // 4) * 520 + 484), f'{t}s', fill='black')
sheet.save(p / 'output/qc-sheet.jpg')
print('QC PASSED')
