# Agnes hook V4 — locked storyboard experiment

Status: **candidate for owner review**

## Result

- Model: `agnes-video-v2.0`
- Input: assistant-generated Cloudinary hook first frame
- Frames: 49 (`8n+1`), 24 fps
- Native duration: 2.041667 s
- Delivery: 1080×1920 H.264, no audio
- Cloudinary: https://res.cloudinary.com/e5cjysjx/video/upload/v1788799809/subai/productions/2026-09-07-someone-broke-in/agnes-hook-v4-locked.mp4
- Public ID: `subai/productions/2026-09-07-someone-broke-in/agnes-hook-v4-locked`
- HTTP verification: 200

## Prompt lesson

The previous prompt asked Stiles to breathe/tremble and the boots to shift weight. Agnes interpreted that as permission to rebuild anatomy and merge the two subjects. V4 instead described the input as a **locked storyboard frame**, explicitly identified Stiles and the boots as separate people on separate floors, froze every character limb, and allowed motion only in dust, lighting and camera.

## QC result

- [x] Stiles remains a crouched stickman.
- [x] Hand stays over mouth.
- [x] Two work boots remain below the hatch and separate from Stiles.
- [x] No added/missing limbs.
- [x] No transition into a realistic or thick-bodied human.
- [x] Full clip decodes without errors.
- [x] No loop or salvaged prefix was used; this is the original complete 49-frame generation.
- [!] Agnes ignored the requested one-percent camera move and generated a much stronger push. It is visually useful as a short hook, but camera magnitude remains a model-control limitation.

## Prompt pattern for future hooks

- Prefer 49 frames (~2 s) for stylized single-frame hooks; longer generations drift more.
- Begin with `LOCKED STORYBOARD FRAME`.
- Explicitly name each visible person/object and their spatial relationship.
- Freeze character position, limbs, face, anatomy and object silhouettes.
- Animate environment only: dust, rain, light flicker, fog, reflections.
- Avoid `breathing`, `trembling`, `weight shift`, `turning`, or other body-motion language unless deformation is acceptable.
- Always inspect a contact sheet spanning the entire clip before accepting it.
