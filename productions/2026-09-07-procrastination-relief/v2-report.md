# V2 report — richer dual-voice psychology cut

## Owner feedback addressed

- Locked the liked subtitle design centrally as `stiles-word-pop-v1` rather than redefining it in each production.
- Rebuilt the visual plan around 10 richer, denser scenes instead of sparse infographic-like frames.
- Added a post-production opening punch: 100%→105% in ~0.23 s, then eased back to 100% across the four-second hook.
- Added female Fish voice Paula alongside male Slax.
- Fish speed set to 1.05 with restrained S2.1 bracket expression tags.
- Added low-level intro whoosh, phone click, mechanism hit and completion chime.

## Fish Audio

- Male: Slax, `c5f56a6cc2ec4fa8920cb4c5889a3fb7`
- Female: Paula, `c2623f0c075b4492ac367989aee1576f`
- Model: `s2.1-pro-free`
- Prosody speed: 1.05
- 11 short dialogue turns; 84 provider-aligned caption words
- Dialogue duration: 37.98 s; final timeline: 39.98 s
- Tags included `[curious]`, `[emphasis]`, `[surprised]`, `[low voice]`, `[concerned]`, `[realizing]`, `[sigh]`, `[encouraging]` and `[confident]`; tags did not become caption words.

## Visuals and Agnes

- 10 final source scenes, each mapped to a four-second beat.
- All 10 were uploaded and attempted as 97-frame Agnes V2.0 clips.
- Concurrent task creation caused HTTP 429; sequential generation with cooldown succeeded for all 10.
- Sampled first/middle/last frame QC rejected scenes 2, 3, 4, 5, 8 and 10 for camera changes, character/body changes, disappearance or major recomposition.
- Retained scenes 1, 6, 7 and 9 as meaningful-action Agnes footage.
- Rejected clips were replaced by their richer source stills with controlled push, pull or lateral pan. They were not treated as successful merely to reach a count.

## Captions

- Central config: `config/caption-style.json`
- Renderer: `tools/render-word-captions.py`
- Style ID: `stiles-word-pop-v1`
- 60 px DejaVu Sans Bold; `(540,1230)`; white plus warm-yellow highlights; 3 px outline; 1 px shadow; no box; `78%→108%→100%` pop
- Exactly one visible word; 84 events; overlap check 0

## Final QC

- 1080×1920, 30 fps, H.264
- Mono AAC, 48 kHz
- 39.98 seconds
- Integrated loudness ~−16 LUFS, true peak ~−1.5 dBTP
- Durable Cloudinary URL in `cloudinary.md`, verified HTTP 200
