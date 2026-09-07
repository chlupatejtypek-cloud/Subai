# Vertical test V3 — Agnes hook render report

## Final result

- Final video: `final/someone-broke-in-test-v3-agnes.mp4`
- Cloudinary: https://res.cloudinary.com/e5cjysjx/video/upload/v1788798777/subai/productions/2026-09-07-someone-broke-in/someone-broke-in-test-v3-agnes.mp4
- Duration: **39.333 s**
- Canvas: **1080×1920**, 30 fps
- Size: **5,036,890 bytes**
- Captions: one word at a time, 60 px, smooth pop, actual word alignment, no box
- Narration: existing non-ElevenLabs test voice; no new TTS credits used

## Assistant-generated first frame

The assistant generated a new production-specific hook image before calling Agnes. It depicts Stiles hiding in the attic while the intruder's boots stand in the closet directly below.

- Cloudinary first frame: https://res.cloudinary.com/e5cjysjx/image/upload/v1788797504/subai/productions/2026-09-07-someone-broke-in/hook-v3-first-frame.png
- Public ID: `subai/productions/2026-09-07-someone-broke-in/hook-v3-first-frame`
- HTTP verification: 200

## Agnes attempts and honest QC

1. `agnes-video-2.5` rejected task creation with HTTP 403 `insufficient_user_quota` (remaining quota $0). No output and no charge.
2. `agnes-video-v2.0` accepted the frame-based image-to-video request and completed successfully.
3. Initial polling every three seconds hit HTTP 429 after progress reached 30%. The same video ID was resumed—no duplicate generation—and completed using a 15-second polling interval.
4. The full four-second Agnes output failed creative QC: after roughly 0.4 seconds it changed Stiles into a thicker human-like character and removed/reinterpreted the boots.
5. The first ~0.2 seconds retained the correct character and composition. That accepted micro-motion prefix was converted into a smooth forward/reverse loop with a controlled camera push. No additional Agnes task was created.

Accepted hook:

- Cloudinary: https://res.cloudinary.com/e5cjysjx/video/upload/v1788798775/subai/productions/2026-09-07-someone-broke-in/hook-v3-agnes-safe.mp4
- Public ID: `subai/productions/2026-09-07-someone-broke-in/hook-v3-agnes-safe`
- Duration: 4.000 s
- Resolution: 1080×1920
- HTTP verification: 200

## Final edit

- 0.00–4.00: accepted Agnes micro-motion hook.
- 4.00–6.84: static attic/boots continuation with Ken Burns movement.
- Remaining cuts follow narration beats from V2 (house/smoke, waking, stairs, attic escape, search, police, knife, closing question).
- Full final MP4 decoded without ffmpeg errors.

## Workspace lifecycle

Durable results were uploaded and HTTP-verified before cleanup. The V3 final remains local temporarily for owner preview; all other ignored production media can be removed after review using `.media-keep` and `tools/cleanup-production.py`.
