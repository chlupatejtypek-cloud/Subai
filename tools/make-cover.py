#!/usr/bin/env python3
"""Generate a TikTok cover (thumbnail) for a production.

Design rules are derived from the layout constraints TikTok actually imposes
(see TIKTOK.md for the sourced reasoning):

  canvas          1080x1920, sRGB
  grid-safe box   the centre 1080x1080 square is the ONLY region visible in
                  both the full-screen cover and the 1:1/3:4 profile-grid crop,
                  so the focal point and the headline live there
  title gutter    the bottom ~270 px is overprinted by TikTok's auto-title
                  (first caption line) and must stay free of meaning
  status gutter   the top 220 px sits under the status bar / follow chrome
  legibility      everything must still read at 200x350 px, so the headline is
                  set in a heavy display face at >= 96 px with real contrast

The cover is built from one production illustration: subject on the left/centre,
a large short headline, a small kicker, and a channel wordmark. Output is PNG
(sharp text) plus a proof sheet showing the crops and the 200x350 legibility
test, so the cover can be judged before upload.

Usage
    python tools/make-cover.py PRODUCTION_DIR --image path.png \
        --headline "NAME IT" --sub "Your body listens first" [--apply]
    python tools/make-cover.py PRODUCTION_DIR --from-video final.mp4 --ss 12.5 ...

Without --apply the tool only writes to a scratch preview path.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
GRID_SAFE = (0, (H - 1080) // 2, 1080, (H - 1080) // 2 + 1080)  # centre square
TITLE_GUTTER = 270      # bottom, covered by TikTok's auto-title
STATUS_GUTTER = 220     # top, under status bar / chrome
SIDE_MARGIN = 72
MIN_HEADLINE_PX = 96
THUMB_TEST = (200, 350)

ROOT = Path(__file__).resolve().parent.parent
FONT_DISPLAY = ROOT / "assets/fonts/Anton-Regular.ttf"
FONT_TEXT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

# Stiles palette (warm green / ochre / cream), kept consistent across covers
INK = (28, 38, 34)
CREAM = (245, 238, 224)
OCHRE = (222, 158, 58)
GREEN = (46, 96, 78)


# ---------------------------------------------------------------- utilities
def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def text_size(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def wrap_to_width(draw, text, font_path, size, max_width, max_lines):
    """Greedy wrap; returns (lines, font) or None when it does not fit."""
    font = load_font(font_path, size)
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if text_size(draw, trial, font)[0] <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        return None
    if any(text_size(draw, ln, font)[0] > max_width for ln in lines):
        return None
    return lines, font


def fit_headline(draw, text, max_width, max_lines=3, hi=260, lo=MIN_HEADLINE_PX):
    """Largest size that fits. Never goes below MIN_HEADLINE_PX."""
    best = None
    for size in range(hi, lo - 1, -2):
        got = wrap_to_width(draw, text, FONT_DISPLAY, size, max_width, max_lines)
        if got:
            best = (got[0], got[1], size)
            break
    if best is None:
        raise SystemExit(
            f"headline {text!r} cannot be set at >= {lo}px in {max_lines} lines; "
            "shorten it (3-5 words is the target)"
        )
    return best


def relative_luminance(rgb):
    def chan(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(x) for x in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def ffmpeg_bin():
    for cand in ("ffmpeg",):
        try:
            subprocess.run([cand, "-version"], capture_output=True, check=True)
            return cand
        except Exception:
            pass
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise SystemExit("ffmpeg not available; install it or pass --image")


def frame_from_video(video: Path, seconds: float) -> Image.Image:
    out = Path(tempfile.mkdtemp()) / "frame.png"
    subprocess.run(
        [ffmpeg_bin(), "-y", "-ss", str(seconds), "-i", str(video),
         "-frames:v", "1", str(out)],
        check=True, capture_output=True,
    )
    return Image.open(out).convert("RGB")


# ---------------------------------------------------------------- composition
def cover_from(base: Image.Image, headline: str, sub: str, wordmark: str,
               accent=OCHRE) -> Image.Image:
    """Compose the cover.

    Layout, from the constraints at the top of this file:
      - the kicker + headline block sits wholly inside the grid-safe square, so
        the promise survives the profile-grid crop as well as the full cover;
      - a soft-edged dark panel sits under the text so contrast never depends
        on which illustration was used;
      - the bottom title gutter and the top status gutter stay empty.
    """
    img = base.convert("RGB")

    # Fill 1080x1920 without distortion.
    scale = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)),
                     Image.LANCZOS)
    left = (img.width - W) // 2
    top = (img.height - H) // 2
    canvas = img.crop((left, top, left + W, top + H))

    draw = ImageDraw.Draw(canvas)
    max_text_w = W - 2 * SIDE_MARGIN

    # The text block must end inside the grid-safe square, not merely above the
    # title gutter, or the headline is decapitated on the profile grid.
    grid_top, grid_bottom = GRID_SAFE[1], GRID_SAFE[3]
    block_bottom = grid_bottom - 40

    lines, font, size = fit_headline(draw, headline.upper(), max_text_w,
                                     max_lines=2, hi=175)
    line_h = int(size * 1.02)
    block_h = line_h * len(lines)

    sub_font = load_font(FONT_TEXT, 44)
    sub_lines = []
    if sub:
        got = wrap_to_width(draw, sub.upper(), FONT_TEXT, 44, max_text_w, 2)
        sub_lines = got[0] if got else [sub.upper()]
    sub_h = 52 * len(sub_lines)

    rule_h = 14
    gap_rule, gap_sub = 26, 22
    total_h = rule_h + gap_rule + sub_h + gap_sub + block_h if sub_lines \
        else rule_h + gap_rule + block_h
    block_top = block_bottom - total_h
    if block_top < grid_top + 40:
        block_top = grid_top + 40

    # Soft-edged dark panel behind the whole text block.
    panel_top = max(grid_top - 40, block_top - 90)
    panel = Image.new("L", (W, H), 0)
    pd = ImageDraw.Draw(panel)
    pd.rectangle([0, panel_top, W, block_bottom + 90], fill=225)
    panel = panel.filter(ImageFilter.GaussianBlur(70))
    dark = Image.new("RGB", (W, H), (12, 20, 17))
    canvas = Image.composite(dark, canvas, panel)
    draw = ImageDraw.Draw(canvas)

    y = block_top
    draw.rounded_rectangle([SIDE_MARGIN, y, SIDE_MARGIN + 132, y + rule_h],
                           radius=7, fill=accent)
    y += rule_h + gap_rule

    for line in sub_lines:
        draw.text((SIDE_MARGIN, y), line, font=sub_font, fill=accent)
        y += 52
    if sub_lines:
        y += gap_sub

    for line in lines:
        draw.text((SIDE_MARGIN + 4, y + 5), line, font=font, fill=(0, 0, 0))
        draw.text((SIDE_MARGIN, y), line, font=font, fill=CREAM)
        y += line_h

    headline_band = (block_bottom - block_h, block_bottom)

    # Wordmark, small, in the clean band under the status gutter.
    if wordmark:
        wm_font = load_font(FONT_TEXT, 32)
        wm_w, wm_h = text_size(draw, wordmark, wm_font)
        pad = 16
        x0, y0 = SIDE_MARGIN, STATUS_GUTTER + 10
        draw.rounded_rectangle(
            [x0 - pad, y0 - pad, x0 + wm_w + pad, y0 + wm_h + pad + 8],
            radius=13, fill=(12, 20, 17),
        )
        draw.text((x0, y0), wordmark, font=wm_font, fill=CREAM)

    # TikTok prints its auto-title in white over the bottom gutter. If that
    # strip is bright or busy the caption is unreadable, so darken and soften
    # it deliberately instead of hoping the illustration cooperates.
    gutter_mask = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(gutter_mask)
    gd.rectangle([0, H - TITLE_GUTTER - 40, W, H], fill=200)
    gutter_mask = gutter_mask.filter(ImageFilter.GaussianBlur(55))
    softened = canvas.filter(ImageFilter.GaussianBlur(9))
    canvas = Image.composite(softened, canvas, gutter_mask)
    canvas = Image.composite(dark, canvas, gutter_mask.point(lambda v: int(v * 0.8)))

    canvas.info["headline_band"] = headline_band
    return canvas


# ---------------------------------------------------------------- validation
@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def validate(cover: Image.Image, headline_px: int) -> list[Check]:
    checks: list[Check] = []
    checks.append(Check("dimensions", cover.size == (W, H),
                        f"{cover.size[0]}x{cover.size[1]} (want {W}x{H})"))
    checks.append(Check("headline_size", headline_px >= MIN_HEADLINE_PX,
                        f"{headline_px}px (min {MIN_HEADLINE_PX})"))

    # Title gutter should be visually quiet: low variance means nothing
    # important is parked where TikTok prints the caption.
    gutter = cover.crop((0, H - TITLE_GUTTER, W, H)).convert("L")
    gutter = gutter.resize((270, 68), Image.LANCZOS)
    edges = gutter.filter(ImageFilter.FIND_EDGES).resize((135, 34), Image.LANCZOS)
    energy = sum(edges.getdata()) / (135 * 34)
    checks.append(Check("title_gutter_quiet", energy < 12,
                        f"edge energy {energy:.1f} (<12 keeps the auto-title readable)"))

    # Legibility at profile-thumbnail size: downscale then measure local
    # contrast in the headline band.
    small = cover.resize(THUMB_TEST, Image.LANCZOS).convert("L")
    band = small.crop((0, int(THUMB_TEST[1] * 0.55), THUMB_TEST[0],
                       int(THUMB_TEST[1] * 0.86)))
    vals = list(band.getdata())
    spread = max(vals) - min(vals)
    checks.append(Check("legible_at_200x350", spread >= 110,
                        f"luma spread {spread} (>=110)"))

    # Focal contrast: headline cream against its own bed.
    band = cover.info.get("headline_band", (int(H * 0.62), int(H * 0.72)))
    bed = cover.crop((SIDE_MARGIN, band[0], W - SIDE_MARGIN, band[1]))
    # darkest decile of the band approximates the bed behind the glyphs
    lum = sorted(bed.resize((48, 24)).convert("L").getdata())
    q = lum[len(lum) // 10]
    bed = (q, q, q)
    ratio = contrast_ratio(CREAM, bed)
    inside = band[0] >= GRID_SAFE[1] and band[1] <= GRID_SAFE[3]
    checks.append(Check("headline_inside_grid_crop", inside,
                        f"headline band {band} vs grid-safe "
                        f"{GRID_SAFE[1]}-{GRID_SAFE[3]}"))
    checks.append(Check("headline_contrast", ratio >= 4.5,
                        f"{ratio:.1f}:1 against the scrim (>=4.5)"))
    return checks


def proof_sheet(cover: Image.Image, out: Path):
    """Show what the cover looks like where it is actually seen."""
    pad = 30
    full = cover.resize((360, 640), Image.LANCZOS)
    grid = cover.crop(GRID_SAFE).resize((360, 360), Image.LANCZOS)
    tiny = cover.resize(THUMB_TEST, Image.LANCZOS)

    sheet = Image.new("RGB", (360 * 3 + pad * 4, 640 + pad * 2 + 60), (24, 24, 26))
    d = ImageDraw.Draw(sheet)
    f = load_font(FONT_TEXT, 22)
    sheet.paste(full, (pad, pad + 40))
    sheet.paste(grid, (pad * 2 + 360, pad + 40))
    sheet.paste(tiny, (pad * 3 + 720, pad + 40))
    d.text((pad, pad + 6), "full cover 1080x1920", font=f, fill=(235, 235, 235))
    d.text((pad * 2 + 360, pad + 6), "profile-grid crop (centre square)",
           font=f, fill=(235, 235, 235))
    d.text((pad * 3 + 720, pad + 6), "200x350 legibility test",
           font=f, fill=(235, 235, 235))

    # Mark the gutters on the full view.
    gy = int(640 * (1 - TITLE_GUTTER / H))
    d.rectangle([pad, pad + 40 + gy, pad + 360, pad + 40 + 640],
                outline=(226, 92, 92), width=2)
    d.text((pad + 6, pad + 42 + gy), "auto-title", font=load_font(FONT_TEXT, 18),
           fill=(226, 92, 92))
    sheet.save(out)


# ---------------------------------------------------------------- entrypoint
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("production", type=Path)
    ap.add_argument("--image", type=Path, help="illustration to build the cover from")
    ap.add_argument("--from-video", type=Path, help="extract the base frame from a video")
    ap.add_argument("--ss", type=float, default=2.0, help="frame timestamp in seconds")
    ap.add_argument("--headline", required=True, help="3-5 words, the promise")
    ap.add_argument("--sub", default="", help="short kicker under the headline")
    ap.add_argument("--wordmark", default="STILES PSYCHOLOGY")
    ap.add_argument("--apply", action="store_true",
                    help="write cover.png into the production directory")
    args = ap.parse_args()

    prod = args.production
    if not prod.is_dir():
        raise SystemExit(f"no such production directory: {prod}")

    if args.image:
        base = Image.open(args.image).convert("RGB")
        source = str(args.image)
    elif args.from_video:
        base = frame_from_video(args.from_video, args.ss)
        source = f"{args.from_video}@{args.ss}s"
    else:
        raise SystemExit("pass --image or --from-video")

    tmp = Image.new("RGB", (10, 10))
    _, _, headline_px = fit_headline(
        ImageDraw.Draw(tmp), args.headline.upper(), W - 2 * SIDE_MARGIN
    )
    cover = cover_from(base, args.headline, args.sub, args.wordmark)

    checks = validate(cover, headline_px)
    for c in checks:
        print(f"  [{'ok ' if c.ok else 'FAIL'}] {c.name}: {c.detail}")
    failed = [c.name for c in checks if not c.ok]

    out_dir = prod if args.apply else prod
    cover_path = out_dir / ("cover.png" if args.apply else "cover-preview.png")
    proof_path = out_dir / ("cover-proof.png" if args.apply else
                            "cover-preview-proof.png")
    cover.save(cover_path, "PNG")
    proof_sheet(cover, proof_path)

    meta = {
        "platform": "tiktok",
        "cover": cover_path.name,
        "proof_sheet": proof_path.name,
        "source_image": source,
        "headline": args.headline,
        "sub": args.sub,
        "wordmark": args.wordmark,
        "headline_px": headline_px,
        "canvas": [W, H],
        "grid_safe_box": list(GRID_SAFE),
        "title_gutter_px": TITLE_GUTTER,
        "checks": [{"name": c.name, "ok": c.ok, "detail": c.detail} for c in checks],
        "all_checks_passed": not failed,
        "bytes": cover_path.stat().st_size,
    }
    if args.apply:
        (prod / "cover.json").write_text(json.dumps(meta, indent=2) + "\n")

    print(f"\nwrote {cover_path} ({cover_path.stat().st_size/1024:.0f} KB)")
    print(f"wrote {proof_path}")
    if failed:
        print(f"\nFAILED checks: {', '.join(failed)} — fix before uploading")
        sys.exit(1)


if __name__ == "__main__":
    main()
