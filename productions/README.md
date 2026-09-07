# 📁 productions/ — one folder per video

Every video gets one folder: `productions/<YYYY-MM-DD>-<slug>/` (e.g. `productions/2026-09-07-the-roommate-who-wasnt-real/`).

| Path | What lives there | When |
|---|---|---|
| `brief.md` | Working title, angle, pillar, source link(s) | Step 1 |
| `script.md` | The speaker-tagged master script (input for Step 4) | Step 3 |
| `audio/segments/` | Per-line TTS mp3s (`001-narrator.mp3`, …) | Step 4 |
| `audio/voiceover_raw.mp3` | Merged segments before tempo | Step 4 |
| `audio/voiceover.mp3` | **Final single narration track** (slightly sped up) | Step 4 |
| `background/` | YouTube clips pulled from the GitHub Actions artifact (`clip.mp4`) + a `sources.txt` with each clip's link | Step 5 |
| `visuals/` | Scene boards, captions, animation inputs | Step 6 (future) |
| `final/` | The finished video | Step 8 (future) |

## Notes

- Only `*.md` and small text files are committed to git. All audio/video under `productions/` is gitignored (the repo stays light; media can be regenerated).
- Keep `sources.txt` up to date — every Reddit thread and every background clip gets its link recorded for the description and for rights-safety.
- When a video is published (Step 9, future), the folder stays as the archive for that video.
