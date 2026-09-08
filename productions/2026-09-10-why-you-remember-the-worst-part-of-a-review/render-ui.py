"""Animated UI overlay: every card and row eases into view, never spawns.

Card entrances are 400 ms; rows stagger in after their panel. Nothing appears
instantly, per the standing owner requirement.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json

p = Path(__file__).resolve().parent
W, H, fps, duration = 1080, 1920, 30, 49.6
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fonts = {n: ImageFont.truetype(F, n) for n in (30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 52, 58, 64)}
cream, ink, teal, gold = '#FFF8E9', '#173B3B', '#3B827D', '#C49138'


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def text(layer, s, x, y, size, age, at=0.0, col=ink):
    u = ease((age - at) / .4)
    if not u:
        return
    tmp = Image.new('RGBA', (W, H))
    ImageDraw.Draw(tmp).text((x + round(60 * (1 - u)), y), s, font=fonts[size], fill=col)
    tmp.putalpha(tmp.getchannel('A').point(lambda a: round(a * u)))
    layer.alpha_composite(tmp)


# (start, end, key) — must match storyboard.json ui_in timings
WINDOWS = [
    (6.4, 10.1, 'minute'),
    (10.6, 13.2, 'howlong'),
    (17.4, 22.5, 'nolink'),
    (23.0, 26.5, 'peakend'),
    (26.9, 29.5, 'twopoints'),
    (30.1, 34.2, 'trial'),
    (34.6, 37.4, 'result'),
    (39.7, 43.3, 'keeps'),
    (47.1, 49.6, 'read'),
]


def frame(t):
    im = Image.new('RGBA', (W, H))
    sel = next(((a, b, k) for a, b, k in WINDOWS if a <= t < b), None)
    if not sel:
        return im
    start, end, kind = sel
    age = t - start
    fade = min(ease(age / .4), ease((end - t) / .4))
    dy = round(50 * (1 - ease(age / .4)))
    layer = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(layer)

    def panel(y, h):
        d.rounded_rectangle((80, y, 1000, y + h), radius=30, fill=cream,
                            outline=ink, width=3)

    if kind == 'minute':
        panel(300, 330)
        text(layer, 'EVERY MINUTE', 125, 345, 52, age)
        text(layer, 'Pain rated 0 to 10', 130, 445, 40, age, .3, teal)
        text(layer, 'Throughout the procedure', 130, 515, 34, age, .6)
    elif kind == 'howlong':
        panel(300, 340)
        text(layer, 'HOW LONG?', 125, 345, 52, age)
        text(layer, 'Shortest      4 minutes', 130, 450, 40, age, .3)
        text(layer, 'Longest      69 minutes', 130, 530, 40, age, .6, gold)
    elif kind == 'nolink':
        panel(280, 400)
        text(layer, 'WHAT PREDICTED', 125, 325, 48, age)
        text(layer, 'THE MEMORY?', 125, 385, 48, age, .1)
        text(layer, 'How long it lasted', 130, 500, 40, age, .8)
        text(layer, 'Almost no relationship', 130, 570, 44, age, 1.2, gold)
    elif kind == 'peakend':
        panel(280, 430)
        text(layer, 'WHAT PREDICTED', 125, 325, 48, age)
        text(layer, 'THE MEMORY?', 125, 385, 48, age, .1)
        text(layer, 'The worst moment', 130, 500, 44, age, .5, teal)
        text(layer, 'The last few minutes', 130, 580, 44, age, 1.1, teal)
    elif kind == 'twopoints':
        panel(320, 300)
        text(layer, 'TWO POINTS', 125, 365, 52, age)
        text(layer, 'Everything else averaged away', 130, 470, 34, age, .4)
    elif kind == 'trial':
        panel(300, 330)
        text(layer, '682 PATIENTS', 125, 345, 52, age)
        text(layer, 'Half got an extra minute', 130, 445, 40, age, .4)
        text(layer, 'Uncomfortable, but gentler', 130, 515, 34, age, .9, teal)
    elif kind == 'result':
        panel(290, 400)
        text(layer, 'THE RESULT', 125, 335, 52, age)
        text(layer, 'Total discomfort      Higher', 130, 445, 38, age, .3)
        text(layer, 'Remembered as        Better', 130, 525, 38, age, .9, gold)
        u = ease((age - 1.5) / .6)
        if u:
            d.line((132, 590, 132 + round(560 * u), 590), fill=gold, width=6)
    elif kind == 'keeps':
        panel(300, 360)
        text(layer, 'YOUR MEMORY KEEPS', 125, 345, 48, age)
        text(layer, 'The peak', 130, 450, 44, age, .5, teal)
        text(layer, 'The ending', 130, 530, 44, age, 1.2, teal)
    else:  # read
        panel(320, 300)
        text(layer, 'BEFORE YOU DECIDE', 125, 365, 48, age)
        text(layer, 'Read the whole record', 130, 470, 42, age, .4, teal)

    layer.putalpha(layer.getchannel('A').point(lambda a: round(a * fade)))
    im.alpha_composite(layer, (0, dy))
    return im


if __name__ == '__main__':
    (p / 'output').mkdir(exist_ok=True)
    proc = subprocess.Popen(
        ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba',
         '-s', f'{W}x{H}', '-r', str(fps), '-i', '-', '-an', '-c:v', 'qtrle',
         str(p / 'output/ui.mov')], stdin=subprocess.PIPE)
    try:
        for i in range(round(duration * fps)):
            f = frame(i / fps)
            assert f is not None, f'frame {i} returned None'
            proc.stdin.write(f.tobytes())
    finally:
        proc.stdin.close()
    assert proc.wait() == 0

    (p / 'ui-qc.json').write_text(json.dumps({
        'segments': [[a, b, k] for a, b, k in WINDOWS],
        'component_transition_ms': 400,
        'panel_translation_px': 50,
        'text_translation_px': 60,
        'staggered_row_entrances': True,
        'entrances_and_exits_eased': True,
        'nothing_spawns_instantly': True,
        'underline_growth_ms': 600,
        'underline_count': 1,
        'blur_intervals': [[19.0, 22.6], [34.3, 37.5]],
        'blur_fade_seconds': .4,
        'claims': ('Qualitative only. Duration shown as "almost no relationship" '
                   'rather than r=.03; predictors shown as "the worst moment" and '
                   '"the last few minutes" rather than r=.67. 682 patients is exact '
                   'and sourced. No return-rate percentage.'),
    }, indent=2) + '\n')
    print('ui.mov written')
