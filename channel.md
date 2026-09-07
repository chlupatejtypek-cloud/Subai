---
id: stiles-psychology
name: "Stiles Psychology"
status: active
content_language: en-US
plan_version: "4.0"
production_mode: "vertical-test"
registry: "config/channels.json"
calendar: "calendar/2026-09-07_2026-10-06.json"
tts:
  provider: fish_audio
  model: s2.1-pro-free
  reference_id: fb7ec16ca51a45a5a4db881244d7990a
  generation_speed: 1.0
  edit_speed: 1.06
  secondary_voice: null
updated: "2026-09-07"
---

# Stiles Psychology

**Tiny figures. Big psychology.** Research-led English Shorts using a consistent minimalist stick character. This brand currently posts through the authenticated YouTube channel **Chlupatej Typek**, ID `UCcWp-VFQ1zzI8Bl3n7krB6w`. Do not rename that channel or assume another account without owner authorization.

## Current sources of truth
- `config/channels.json`: every channel, connected Cloudinary account, public channel identity, voice, publication policy and names of secrets. Currently one channel.
- `calendar/2026-09-07_2026-10-06.json`: canonical machine-readable 30-day plan and live publication state.
- `AUTOMATION.md`: production handoff, QA gate and automatic publisher.
- `characters/stiles.md`: canonical character v2; `config/caption-style.json`: locked captions.
- Registry/this v4.0 policy supersede legacy Adam/Jessica or weekly-cadence rules in historical production files.

## Identity and audience
Global English-speaking viewers, primarily 16–34. Make one everyday behavior understandable through one evidence-informed mechanism and one modest useful action. Educate, never diagnose. All videos, titles, descriptions and scripts use en-US. Owner discussion can be Czech.

Stiles: circular warm-beige head, thin charcoal stick torso and limbs, tiny expressive features, mitten hands, long legs. Premium muted 2D storybook art. Jessie may appear visually; there is currently one narration voice. Neither character becomes realistic, 3D or a thick pictogram.

## Cadence and calendar
Owner selected 3 videos every day for 30 days, **7 September–6 October 2026**, 90 total. Regular publication slots: **15:00, 19:00, 23:00 Europe/Prague** (13:00, 17:00, 21:00 UTC during this period). These are initial testing choices, not analytics-proven optimal hours. Late first-day launch exception: 22:30 / 23:00 / 23:30 local.

The calendar is an editorial plan, not a claim that 90 videos have already been researched or made. Today's late slots may be missed if production cannot complete. Report missed slots; never quietly backdate, lower standards, or publish several overdue videos in a burst. Review retention and adjust future slots deliberately.

Rotate everyday attention/learning/habits, emotions/social psychology, and biases/decision-making daily. Avoid repeating the same mechanism with interchangeable wording. Proposed mechanisms/actions in the plan must be validated or revised during research.

## Evidence and editorial policy
Before scripting, record at least one primary/peer-reviewed source and one accessible corroborating source. Track which claim each supports, study limitations and whether the practical action is an extrapolation rather than a tested intervention. Prefer qualified statements over universal claims.

Inspect relevant Shorts for pacing where accessible; never fabricate performance data or copy scripts, distinctive creative assets or footage. Document inaccessible benchmarks. No invented statistics, pop-neuroscience certainty, deterministic body-language diagnosis, manipulative "dark psychology", mental-health labeling or treatment promises.

## Production specification
- 1080x1920, 9:16, 30fps, **no more than 40 seconds**; normally ~85–110 spoken words measured after synthesis. Do not pad a naturally shorter edit to 35 seconds.
- Target **10 distinct original source illustrations**, used once per scene where practical, with roughly 2–3 second visual changes. Additional Agnes stills are permitted when a beat genuinely needs them, but require an explicit recorded budget/QA adjustment; the default publisher budget remains ten. Rich foreground/midground/background; every edge full bleed. No white/cream matte, side strip, border or lower panel. Never prompt for a "caption-safe area/lane".
- Supply canonical Stiles reference for all generated scenes. Inspect anatomy, composition, objects, text artifacts and feet. Run `tools/full-bleed-check.py` before Cloudinary/Agnes.
- Agnes: only useful isolated environmental motion, fixed camera, 97 frames/~4s. Default 2.5; on insufficient quota one v2.0 fallback. At most two attempts per scene. Reject morphing/drift; never use a failed clip merely to hit a count. Other scenes use one gentle push, pull or lateral drift. First accepted Agnes hook gets the post-production 100%→105% punch and return; no extra motion on other accepted clips.
- Hook in 1–2s; meaningful change roughly every 4s; one mechanism, one concrete landing/action.

## Current narration — Fish Audio
**Default reference: `fb7ec16ca51a45a5a4db881244d7990a`**, provider metadata title "WNBA VOICEOVER". Voice metadata GET succeeded on 2026-09-07; this setup did not spend credits synthesizing a sample. Use `s2.1-pro-free` with provider-native timestamps and generate at native speed 1.0. Owner feedback on the first Fish video: remove long dead gaps and apply a **1.06× pitch-preserving edit**. First detect real silence; shorten pauses over roughly 0.42s toward 0.28s without clipping phonemes. Remap timestamps after silence removal AND tempo change. Keep short natural pauses; do not flatten all breaths. Normalize script line breaks to spaces before new synthesis.

`tools/fish-tts-with-timestamps.py` now reads the channel registry for its default reference. Do not silently change models/voices on an error; stop and report. Save alignment with the narration, then convert to flat word timing and use the central caption renderer. Generate each finalized script once; use existing audio for edit revisions.

Adam is parked, not deleted. The owner's preceding 1.05× pitch-preserving edit setting applies if Adam is explicitly restored. It does not automatically apply to the new Fish voice. Existing accepted videos are unchanged. No Jessica speech by default.

## Captions and audio
Render only with `tools/render-word-captions.py` and `config/caption-style.json` (`stiles-word-pop-v1`): DejaVu Sans Bold 60px, position (540,1230), white / selected warm-yellow, 3px outline, 1px shadow, no box, uppercase pop 78→108→100%, exactly one visible word, no overlaps. If editing audio speed, divide word timestamps by the same factor and remap scenes.

No continuous music. Restrained opening whoosh and 1–3 motivated quiet SFX; preserve dominant intelligible narration. Record license evidence for downloaded sound; original procedural effects are allowed and must be documented.

## Automatic publication policy
Owner authorized automatic publication after quality checks on 2026-09-07. Repeated manual topic/script/voice approval is not required for this calendar, but research, content, image, audio, rights and technical review are mandatory. This delegated approval does NOT authorize publishing incomplete drafts or changing channel/account identity.

Only mark `ready` after a verified final Cloudinary MP4, SHA256, sourced description and complete QA attestation exist. Publisher validates final file dimensions/duration/audio and refresh-token channel identity. Upload as private with future `publishAt`; missing scheduling confirmation is a reconciliation issue, not success. Public-upload audit restrictions and OAuth Testing-mode expiry remain external blockers until verified.

## QA gate
Evidence and script accurate; no diagnosis/clinical promises; English natural; correct Fish reference; Stiles consistent; full bleed; duration ≤40s; aligned one-word captions/no overlap; voice complete and intelligible; visual review; rights documentation; title/description honest. See exact required fields in AUTOMATION.md.

## History
v3.0 pivoted to research-led psychology; v3.1 locked captions; v3.2 restored ElevenLabs; v3.3 selected Adam and no music. v4.0 switches the default to the owner-provided Fish voice, introduces a channel registry, 90-item calendar and gated automatic publication. Historical production records remain accurate to their original settings.
