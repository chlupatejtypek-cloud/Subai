# Local Hyperframes integration

First actual project: `productions/2026-09-07-why-awkward-silence-feels-so-long/hyperframes-v2/`.
Hyperframes 0.8.31 + Node 22.23.2 + GSAP 3.15.0. Full 1080×1920, 30fps local HTML-to-video render, then FFmpeg overlays locked ASS captions and mixes the one continuous Fish narration. No hosted HeyGen render, account setup or cloud API charge. Anonymous CLI telemetry disabled.

## Bootstrap / reproduce
1. `bash tools/setup-hyperframes.sh` installs pinned runtime packages in /home/user/hyperframes-runtime (node_modules is disposable, package manifests persist).
2. Minimal Debian host needed `libnss3` and `libnspr4`; install only if renderer's dependency preflight reports them. FFmpeg and DejaVu Sans Bold must be available.
3. Restore missing project assets/narration with `python tools/restore-hyperframes-project.py --manifest PROJECT/assets.json --output PROJECT --apply`. First omit --apply for a verified dry run. The source archive is encoded as three JSON parts because direct archive delivery returned HTTP 401; all parts and the reconstructed archive were verified.
4. Run `python build-composition.py`, `bash render-picture.sh`, `python mix-audio.py`, then `python finish-video.py` in that project. Mix requires the documented Kenney CC0 assets, downloaded with provenance.
5. Validate render, ASR, timing, source data and final shot/transition samples. A successful process alone is not semantic QA.

## Authoring decisions / lessons
- A seekable, paused timeline registered in window.__timelines, explicit root duration and stable IDs. No Date.now/random wall-clock motion.
- Declare hidden scene states in CSS AND initialize outside the paused timeline. Zero-time timeline sets can expose the wrong first frame; lint found this and it was fixed.
- Reused stills as CSS backgrounds to avoid duplicate timed-media discovery. The exact same cafe art returns; no regenerated near-duplicate people.
- Render TMPDIR under /home/user/.cache/hyperframes-tmp rather than the small /tmp tmpfs; temporary outputs are excluded from workspace snapshots.
- Two software workers with --no-low-memory-mode completed on this specific ~2GB host; reduce to one if memory pressure appears elsewhere. Do not assume GPU availability.
- Browser QA must not return the GSAP timeline from page.evaluate: a timeline is thenable and a paused one may leave evaluation waiting forever. Seek inside a block returning undefined.
- Cards land once and remain readable. No constant per-word transitions. Data plot uses actual reported means over a complete 1–7 scale, with no invented errors/intervals.
- Preserve locked caption position. UI has intentional whitespace around it, but illustrations remain full bleed; no accidental white caption panel.

## Sound
Fish's official REST schema was inspected: no dedicated SFX generation/search endpoint found. Do not confuse voice model search or similarly named third-party sites with a sound library. Use Fish only for narration unless a real SFX endpoint is later documented/verified.
Kenney Interface Sounds provides CC0 UI assets. This project uses open_001, drop_001 and drop_002, mixed quietly, plus original procedural zoom-in/out whooshes. They are not Fish-generated. Discovery links and API/Agnes diagnostics are in the project's provider-findings.md.

## Next-template changes after anchoring owner review
Remove the persistent brand node in NEW compositions, not archived render sources. Replace dense all-at-once layouts with successive focal groups. Prototype a temporary GSAP blur/dimming treatment on nonessential layers, preserving captions and data context; use it only for important moments. Alternate UI with distinct narrative illustrations. UI direction is owner-praised, not a reason to fill the entire running time with UI.
