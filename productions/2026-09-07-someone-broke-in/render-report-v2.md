# Vertical test V2 — render report

## Result

- Final video: `final/someone-broke-in-test-v2.mp4`
- Duration: **39.333 s**
- Canvas: **1080×1920**, 30 fps
- Video: H.264
- Audio: AAC mono, based on an Arena non-ElevenLabs test voice
- File size: 4,700,956 bytes
- Script: `script-test-v2.md` — 102 words

## Caption implementation

- 102 timed caption events for 102 spoken words.
- Exactly one word visible at a time; automated overlap check returned **0 overlaps**.
- Actual speech recognition/forced mapping was used—timing was not estimated from text length.
- Lightweight Vosk ASR returned exactly 102 timestamps. Five recognition substitutions were corrected by mapping those timestamps one-to-one back to the approved 102-word script.
- First word begins at 0.270 s; final word ends at 39.090 s.
- Position: `(540, 1235)`, approximately 64% of frame height.
- Style: 60 px bold white, restrained outline/shadow, no background box.
- Hook/reveal words use warm yellow.
- Animation per word: 78% scale → 108% → 100%, with a soft 25/55 ms fade.

## Story-driven visual timing

Eleven edit segments reuse ten generated scene images. Cuts are attached to narration beats, not equal divisions:

| Time | Duration | Visual beat |
|---:|---:|---|
| 0.00–3.00 | 3.00 s | Closet opens beneath him |
| 3.00–5.16 | 2.16 s | Attic viewpoint |
| 5.16–6.84 | 1.68 s | Worn boots under hatch |
| 6.84–12.99 | 6.15 s | Three hours earlier: house and smoke |
| 12.99–18.12 | 5.13 s | Narrator wakes and calls out |
| 18.12–20.88 | 2.76 s | Footsteps charge upstairs |
| 20.88–25.44 | 4.56 s | Escape through closet hatch |
| 25.44–29.85 | 4.41 s | Intruder searches and wrecks rooms |
| 29.85–34.83 | 4.98 s | Police response |
| 34.83–37.74 | 2.91 s | Missing knife reveal |
| 37.74–39.34 | 1.60 s | Closing question |

## QC

- [x] Full final MP4 decodes without errors.
- [x] Duration remains below the 40-second hard cap.
- [x] Mean audio level −17.9 dB; peak −1.7 dB.
- [x] 102 caption events, no overlaps.
- [x] Seven spot checks confirm captions have no box and visuals match the spoken beat.
- [x] No new ElevenLabs generation was used.
