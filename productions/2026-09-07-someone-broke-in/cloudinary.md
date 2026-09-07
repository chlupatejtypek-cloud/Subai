# Cloudinary assets

All URLs below were checked for HTTP 200 before local cleanup.

## Current production outputs

| Asset | Public ID | URL | Status |
|---|---|---|---|
| V3 Agnes first frame | `subai/productions/2026-09-07-someone-broke-in/hook-v3-first-frame` | https://res.cloudinary.com/e5cjysjx/image/upload/v1788797504/subai/productions/2026-09-07-someone-broke-in/hook-v3-first-frame.png | uploaded; waiting for Agnes API key |
| Latest completed test V2 | `subai/productions/2026-09-07-someone-broke-in/someone-broke-in-test-v2` | https://res.cloudinary.com/e5cjysjx/video/upload/v1788797505/subai/productions/2026-09-07-someone-broke-in/someone-broke-in-test-v2.mp4 | uploaded; HTTP 200 |

## Pending V3 flow

1. Use the V3 first-frame URL as `--image-url` for `tools/agnes-image-to-video.py`.
2. Generate a four-second 9:16 hook with `agnes-video-2.5`.
3. Inspect the Agnes result for Stiles consistency, extra limbs and text artifacts.
4. Replace the first static segment in the 39-second edit with the accepted Agnes clip.
5. Upload the final V3 video to this Cloudinary folder and record its versioned URL here.
6. Verify HTTP 200, update `.media-keep`, then run workspace cleanup.
