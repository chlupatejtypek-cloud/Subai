#!/usr/bin/env python3
"""Assemble SP-20260910-3.

Layer order:
  1. base.mp4      animated Agnes opening (0-4s) + separate slow zoom push-in
                   on the same still (4-5.6s), then the remaining shots with
                   extremely subtle drift, plus two bounded blur windows.
  2. ui.mov        animated cards (render-ui.py)
  3. captions      canonical stationary word captions
  4. narration.wav one continuous Fish take
"""
import json
import subprocess
import sys
from pathlib import Path

P = Path(__file__).resolve().parent
W, H, FPS = 1080, 1920, 30
SB = json.loads((P / 'storyboard.json').read_text())
DUR = SB['duration_seconds']
OUT = P / 'output'
OUT.mkdir(exist_ok=True)


def run(cmd):
    r = subprocess.run(cmd)
    if r.returncode:
        sys.exit(f'FAILED: {" ".join(str(c) for c in cmd)}')


def seg_path(n):
    return OUT / f'seg{n:02d}.mp4'


def build_segments():
    """One clip per shot. Shot 1 is opening video + a distinct zoom move."""
    shots = SB['shots']
    blur = SB['blur_windows']
    for s in shots:
        n, a, b = s['n'], s['start'], s['end']
        img = P / 'images' / s['image']
        length = round(b - a, 3)

        if n == 1:
            # 1a: real generated motion, scaled to frame, no camera move.
            op = OUT / 'seg01a.mp4'
            run(['ffmpeg', '-y', '-v', 'error', '-i', str(OUT / 'opening-raw.mp4'),
                 '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,'
                        f'crop={W}:{H},fps={FPS},setsar=1',
                 '-an', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p',
                 '-t', '4.0', str(op)])
            # 1b: SEPARATE effect - a slow zoom push-in on the still.
            zl = round(length - 4.0, 3)
            zf = round(zl * FPS)
            zp = OUT / 'seg01b.mp4'
            run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', str(img),
                 '-vf', f"scale=4320:-1,zoompan=z='1.02+0.06*on/{zf}':"
                        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={zf}:s={W}x{H}:fps={FPS},"
                        f'setsar=1',
                 '-t', str(zl), '-an', '-c:v', 'libx264', '-crf', '17',
                 '-pix_fmt', 'yuv420p', str(zp)])
            lst = OUT / 'seg01.txt'
            lst.write_text(f"file '{op.name}'\nfile '{zp.name}'\n")
            run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
                 '-i', str(lst), '-c', 'copy', str(seg_path(1))])
            continue

        # Extremely subtle drift on illustrated holds.
        frames = round(length * FPS)
        vf = (f"scale=4320:-1,zoompan=z='1.015+0.012*on/{frames}':"
              f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},"
              f'setsar=1')

        # Bounded blur: a blurred copy overlaid with an alpha fade in/out.
        # boxblur radius cannot take a time expression, but fade=alpha can.
        win = next((bw for bw in blur if bw['start'] < b and bw['end'] > a), None)
        if win:
            ls = round(max(win['start'], a) - a, 3)
            le = round(min(win['end'], b) - a, 3)
            fc = (f'[0:v]{vf},split=2[clean][toblur];'
                  f'[toblur]gblur=sigma=18,format=yuva420p,'
                  f'fade=t=in:st={ls}:d=0.4:alpha=1,'
                  f'fade=t=out:st={round(le - 0.4, 3)}:d=0.4:alpha=1[blurred];'
                  f"[clean][blurred]overlay=0:0:enable='between(t,{ls},{le})'[v]")
            run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', str(img),
                 '-filter_complex', fc, '-map', '[v]', '-t', str(length),
                 '-an', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p',
                 str(seg_path(n))])
        else:
            run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', str(img),
                 '-vf', vf, '-t', str(length), '-an', '-c:v', 'libx264',
                 '-crf', '17', '-pix_fmt', 'yuv420p', str(seg_path(n))])


def concat_base():
    lst = OUT / 'segments.txt'
    lst.write_text(''.join(f"file '{seg_path(s['n']).name}'\n" for s in SB['shots']))
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
         '-i', str(lst), '-c', 'copy', str(OUT / 'base.mp4')])


def overlay_ui():
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(OUT / 'base.mp4'),
         '-i', str(OUT / 'ui.mov'),
         '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto[v]',
         '-map', '[v]', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p',
         '-an', str(OUT / 'with-ui.mp4')])


def captions_and_audio():
    import os
    os.chdir(OUT)
    ass = OUT / 'captions.ass'
    run([sys.executable, str(P.parent.parent / 'tools/render-word-captions.py'),
         '--timestamps', str(P / 'audio/words.json'), '--output', str(ass)])
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(OUT / 'with-ui.mp4'),
         '-vf', f"ass={ass.name}", '-c:v', 'libx264', '-crf', '17',
         '-pix_fmt', 'yuv420p', '-an', str(OUT / 'with-captions.mp4')])
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(OUT / 'with-captions.mp4'),
         '-i', str(P / 'audio/final-mix.wav'),
         '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
         '-af', 'apad', '-t', str(DUR),
         '-movflags', '+faststart', str(OUT / 'final.mp4')])


if __name__ == '__main__':
    build_segments()
    concat_base()
    overlay_ui()
    captions_and_audio()
    d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'format=duration', '-of', 'csv=p=0',
                        str(OUT / 'final.mp4')], capture_output=True, text=True)
    print('final.mp4 duration =', d.stdout.strip(), 'target =', DUR)
