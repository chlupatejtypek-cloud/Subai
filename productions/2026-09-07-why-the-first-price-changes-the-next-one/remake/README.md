# Anchoring: owner-requested focused remake

Preview only. Do not upload, replace, or reschedule the original YouTube `bj1yP4s3CQ0` without owner approval. Original source and publication records are unchanged.

## Changes
- Actual moving paper tag now bears struck-through $99 and $49, perspective-tracked in all 97 native frames. Fictional example prices. Original Agnes 2.0 motion reused; no new video generation.
- Three new distinct illustrations: physical experiment room, Stiles with globe, and shop. Existing home illustration reused. Five visual environments, seven editorial beats, not seven regenerated pictures.
- Authored SVG wheel spins and stops at 10. Same room/object reused for the explanation, not regenerated.
- Standalone comparison UI lasts ~8 seconds, rather than most of the film. Both medians remain sharp and visible together. No persistent corner brand, progress decoration, or academic footer.
- Temporary selective focus on the real price tag and later the starting-point takeaway. Captions stay sharp.
- One unchanged continuous approved narration, identical canonical 129-word captions. Five restrained sound cues repositioned to the new events.

## Reproduction
Node 22+, Hyperframes 0.8.31 and FFmpeg; Python numpy/scipy/OpenCV/Pillow/soundfile. Restore media with the repository JSON-part restorer and assets.json.

```sh
python track-price.py          # optional: rebuild printed-tag derivative
python build-remake.py
python mix-sfx.py
bash render-picture.sh
python finish-video.py
```

Research is reused from the verified 1974 primary paper; see research.md. The two results are group MEDIAN guesses, not correct answers or present-day UN statistics.
