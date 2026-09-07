---
id: "stiles"
status: "canonical-test-reference"
reference_version: "v1"
cloudinary_public_id: "subai/characters/stiles-tpose-front-back-v1"
cloudinary_url: "https://res.cloudinary.com/e5cjysjx/image/upload/v1788795048/subai/characters/stiles-tpose-front-back-v1.png"
format: "PNG 768x1376"
updated: "2026-09-07"
---

# Stiles — canonical test character reference

Use this model sheet as the strict character reference for every newly generated Stiles image during the test phase:

![Stiles front/back T-pose](https://res.cloudinary.com/e5cjysjx/image/upload/v1788795048/subai/characters/stiles-tpose-front-back-v1.png)

## Required visual traits

- Circular warm-beige head with a dark charcoal outline and a subtle shaded lower rim.
- Very thin charcoal/black stick torso and limbs.
- Long simple legs, small rounded feet, minimal mitten-like hands.
- Tiny readable facial features; expressions change but proportions do not.
- Premium muted 2D storybook/vector treatment on warm neutral or dusty-blue scenes.
- Never turn Stiles into a realistic human, 3D character, thick cartoon body, or generic black pictogram.

## Turnaround rules

- Front and back references define proportions, not a mandatory pose for story scenes.
- Keep head diameter, shoulder height, arm span, torso length and leg length stable.
- For another turnaround, generate one view at a time if the image model produces duplicate limbs.
- Inspect every generated image for extra limbs, mismatched hands, text artifacts and cropped feet before use.

## Cloudinary

- Cloud name and API key are available to GitHub Actions as repository variables.
- API secret is stored only as the encrypted Actions secret `CLOUDINARY_API_SECRET` and locally in gitignored `.env` when the owner provides it.
- Local upload command:

```bash
set -a; source .env; set +a
tools/upload-cloudinary.sh IMAGE PUBLIC_ID subai/characters
```
