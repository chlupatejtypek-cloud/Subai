# Stiles Psychology — current production specification

Machine-readable settings: config/channels.json. Latest owner corrections: VISUAL-EDITORIAL.md. These replace earlier experimental voice/image quotas; history remains in Git.

## Content
English en-US; psychology education, not diagnosis or exaggerated neuroscience. Investigate credible primary evidence before writing, record what was measured and what was not. Useful, non-obvious angle plus concrete practical takeaway. No repeated topic merely with a new title; the calendar's title-uniqueness test is not semantic deduplication.

## Character and visual direction
Owner rejected extreme empty minimalism: use meaningful cafe/street/home or topic-specific backgrounds in cream/teal/ochre, with readable illustrated detail and the same canonical Stiles. Inspect relative head/body size, dot eyes, limbs, proportions and scene relevance against reference. Expressions can change; identity must not. Revised-style work is preview-only until reviewed. The first-step preview was explicitly rejected; never publish it.

Future videos are40–60 seconds with at least10 distinct generated, accepted and actually used illustrations (up to existing15-image cap). Plan around meaningful script beats, not padding or drifting duplicates; aim2.5–5s illustration holds. Include useful animated comparison/state UI, not merely headings. Count used distinct sources separately from generation attempts. Flag holds over7s for justification. See START-WORKFLOW.md and RETENTION-RESEARCH.md.

Actual animated hook required, with separate100→105→100% punch zoom. Prefer Agnes v2.0;2.5 quota rejection is known, do not repeatedly retry it. At most one targeted corrective retry per shot. Provider failure/invalid footage is a blocker, not permission for a camera-only still substitute. Other illustrated holds: barely perceptible monotonic1–2% move, no oscillation, stationary captions and full bleed.

One focal thought at a time; concise UI only when useful. No persistent corner branding, tiny academic footers or “Example prices” opening label. Brief selective blur is optional and must preserve essential comparisons and captions. 40–60s,1080×1920,30fps. Do not stretch scenes to fill the limit.

## Voice, captions, sound
One continuous Fish call, reference fb7ec16ca51a45a5a4db881244d7990a, model/settings from registry, native synthesis speed1.0. Measured silence editing and pitch-preserving1.06× tempo; remap timestamps. Streaming alignment updates may repeat a chunk; retain its complete update rather than duplicate words. Preserve original recording and provider alignment. Adam is parked; no silent voice substitution.

Canonical captions: tools/render-word-captions.py with config/caption-style.json. One word at a time, no overlaps; no independent redesign of the caption style. Independent ASR and timing/level checks; disclose orthographic normalization and do not claim human listening when only automated checks were performed.

No music bed. A few quiet meaningful SFX, including the hook zoom; latest productions use about5, not a mandatory count. Original procedural or licensed/CC0 effects, retain provenance. Fish narration API is not an SFX catalogue.

## Release
Research/script, character/coverage/opening, narration/captions, rights, final-file and remote-checksum review precede ready. See PIPELINE.md and AUTOMATION.md for release-contract fields. New-style preview and rejected work must not be auto-published. Final source/MP4 backups verified before local cleanup; exact edit scripts/provenance stay in Git.
