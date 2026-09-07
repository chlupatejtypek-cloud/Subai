# Render report

## Result

- Status: **rendered — ready for owner review**
- Final video: `final/someone-broke-in-vertical.mp4`
- Voiceover: `audio/voiceover.mp3`
- Captions: `visuals/captions.srt` (also burned into final video)
- Contact sheet: `visuals/contact-sheet.jpg`
- QC sheet: `visuals/qc-sheet.jpg`

## Technical specification

| Property | Result |
|---|---|
| Canvas | 1080×1920 (9:16 vertical) |
| Frame rate | 30 fps |
| Duration | 158.467 s (2:38.47) |
| Video | H.264, yuv420p |
| Audio | AAC, 44.1 kHz, mono |
| File size | 12,030,662 bytes |
| Narrator | ElevenLabs Adam (`pNInz6obpgDQGcFmaJgB`) |
| TTS model | `eleven_multilingual_v2` |
| Spoken lines | 39/39 |
| Spoken words | 452 |
| TTS pacing | 1.07×, pitch preserved |
| Captions | 77 timed phrase cards, burned in |
| Generated images | 10/10, 768×1376 source frames |

## QC

- [x] Every tagged script line has a generated TTS segment.
- [x] All 39 source MP3 segments decode; timing recalculated from decoded PCM to remove MP3 padding drift.
- [x] Final audio normalized toward −16 LUFS (`volumedetect`: mean −17.2 dB, peak −1.6 dB).
- [x] Full final MP4 decodes with no reported errors.
- [x] No black frame lasting longer than one second.
- [x] Video and audio durations match (difference under 0.01 s).
- [x] Captions end at 2:38.401, before the media endpoint.
- [x] Four spot-check frames confirm scene order and caption rendering.
- [x] No gore, visible weapon, invented suspect identity, or invented resolution.

## Deliberate deviations from the old channel plan

The owner selected a 2:30–3:00 vertical video rather than the older 6–10 minute 16:9 format. This production therefore uses ten generated story frames with camera motion instead of YouTube background footage. YouTube upload was not attempted because Step 9 credentials are not configured.
