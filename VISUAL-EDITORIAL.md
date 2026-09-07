# Editorial and visual contract — latest owner review, 2026-09-07
Supersedes fixed ten agent + five Agnes images and the 40s ceiling. Existing voice, single-recording delivery, restrained SFX, English language and canonical captions remain.

## Research before a script exists
1. Investigate primary evidence and an accessible explanation. Record what was actually measured, population, uncertainty and practical limits.
2. Pitch the useful angle internally: what will the viewer learn that is not obvious, why should they care, and what concrete decision/action changes? Reject a generic topic/angle rather than polish empty advice. The calendar is provisional, not permission to bypass research.
3. Build around a compelling question, a clear mechanism/example and an earned practical payoff. Never invent surprising facts or overstate weak evidence to create novelty.
4. Script one flowing paragraph. Keep the accepted Fish voice/tempo. Up to 60 seconds when warranted, no mandatory minimum or artificial padding.

## Calculate images from the storyboard, NOT seconds alone
After draft scripting, define semantic beats; after synthesis, assign their actual word-cue times. For each beat list: duration, new information, visual function, source asset ID, required UI/reveal and transition.

Unique image count = number of distinct required illustration assets after identical-scene reuse and UI-only beats are accounted for. Shot count and image count are DIFFERENT. A new sentence is not automatically a cut. No fixed 10+5 provider allocation. Generate only what the plan calls for; reject redundant pictures even if already paid for.

Use duration/typical hold as a rough planning check, never an automatic cutter: e.g. 48 seconds divided by 6 seconds suggests about 8 visual sections, NOT 8 mandatory new images. Some sections may be UI, some may share exactly the same source illustration. A short hook may need 2–3s; a demonstration may need 7–10s. These are starting examples, not enforced limits. Test comprehension and let complex content remain readable.

Never alternate nearly identical generated cafe scenes with shifting faces, hands, hair or furniture. For continuity, transform/reframe the SAME source asset. New art must add a materially different situation, view or explanation. Movement without information is not engagement.

## Smooth purposeful motion
Keep a stable visual anchor and limited motion hierarchy. Ease cards/labels into place, let them settle and stay long enough to read. A short 250–450ms transition is a starting point to test, not an obligation on every cut. No overlapping-face dissolves, slideshow spinning, random bounce, constant zooms or transition sound spam. Clean motivated cuts are allowed when smoother than an artificial effect.

UI matches Stiles palette/typography and scene depth; avoid an unrelated glossy dashboard pasted over storybook art. Reserve space without creating a blank caption panel. Do not collide with the locked captions or reveal a list too fast to read. Examples: an evidence-backed numerical comparison, a causal sequence, a cue/action plan, or two/three actionable cards arriving exactly with their spoken points. Use true sourced numbers, clear units/axes/baselines; label any illustrative rather than measured graph. Never draw a statistical effect the source did not establish.

## Hyperframes evaluation
Official documentation reviewed:
- https://hyperframes.app/docs/1-startup/1-introduction
- https://developers.heygen.com/hyperframes-overview
HTML/CSS/JS compositions with a seekable timeline can render to video. Candidate integration: isolated chart/card/diagram compositions, locally rendered then composited with the continuous narration and canonical captions. Next technical gate: build a small component, render locally, check deterministic frame timing, font/assets, alpha/compositing, motion easing and final MP4. Initial local integration now rendered in the silence hyperframes-v2 production using Hyperframes 0.8.31. See HYPERFRAMES.md for actual setup and QA lessons. Owner review of the treatment is pending; do not confuse render success with universal creative approval. No paid cloud subscription/API provisioning authorized or needed for the evaluation.

## Review and cleanup
Review the storyboard for semantic repetition BEFORE generation. Review the edit for continuity, useful visual change, readable UI, smooth transitions and sound restraint. Fifteen successful image requests do not constitute successful creative QA.

Before cleanup, enumerate originals/finals/pending revision assets, verify durable backups and populate .media-keep with actual paths (an empty file protects NOTHING). Run tools/cleanup-production.py dry-run, then --apply only on reviewed regenerable or durably backed disposable files. Never delete the sole copy of a final or pending revision source; do not remove remote backups or publishing records. Keep scripts/timelines/provenance and final user-facing downloads.
