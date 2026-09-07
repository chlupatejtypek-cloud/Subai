---
id: stilesguy
name: "StilesGuy"
status: active
content_language: en-US
credentials:
  elevenlabs: ready      # none | pending | ready  (key stored in .env — verified via GH Actions test)
  youtube: none          # none | pending | connected (future, Step 9)
tts:
  provider: elevenlabs
  model: unset           # e.g. current default ElevenLabs quality model — agent picks & records
  voices:
    narrator: unset      # ElevenLabs voice_id — Stiles, masculine, warm storyteller (en-US)
    secondary: unset     # ElevenLabs voice_id — Jessie, feminine, expressive (en-US)
    extras: []           # optional extra voices, added per video only with owner approval
plan_version: "2.4"
production_mode: "vertical-test"
test_constraints:
  canvas: "1080x1920"
  max_duration_seconds: 40
  max_generated_images: 10
  elevenlabs_tts: false
  first_frame_animation: "Agnes image-to-video, prefer 49 frames / about 2 seconds for stickman stability"
  captions: "one word at a time; word-aligned; 60 px; no background box"
created: 2026-09-07
updated: 2026-09-07
---

# StilesGuy

> **Tagline:** *Stick figures. True stories. Plot twists.*

Animated-stickman storytelling channel in English. Simple stick figures act out **real, wild true-life stories** — the kind people tell on Reddit and never shut up about. One main story (or a short themed set) per video, told by **Stiles** with his sidekick **Jessie**.

---

## 1. Characters

| Character | Who | Voice role |
|---|---|---|
| **Stiles** | Main stickman — male, round head, slightly crooked smile. Everyman narrator and default "hero" of the story. | `NARRATOR` (always present) |
| **Jessie** | Female stick figure — ponytail, a bit more expressive. Co-host, skeptic sidekick, and the voice that reads quotes / plays the other characters. | `JESSIE` (always available) |

- Other characters in a story are played by **Stiles/Jessie voices in character** or (rarely, with owner approval) short-lived `EXTRA-*` voices.
- Stick-figure design stays minimal and consistent: thin black strokes, flat pastel scene backgrounds, the two heroes always recognizable.

## 2. Purpose & promise

- Retell real, fascinating stories so a viewer **feels the twist** ("no way", "deserved", "oh no") instead of just hearing it.
- Make "boring" true stories cinematic: setup → doubt → twist → payoff.
- Build a library of evergreen story videos that compound on browse and suggested feeds.

## 3. Audience

| Dimension | Value |
|---|---|
| Geography | Global English-speaking (US/UK/CA/AU dominant) |
| Age | 16–34 core (plus anyone who loves Reddit storytime) |
| Mindset | Browsers who love storytime channels, "plot twist" compilations, AskReddit videos, satisfying justice content |
| Consumption | Mobile-heavy, suggested-feed heavy, often binged; sound on |

## 4. Format & length

### Current mode: vertical testing (owner decision, 2026-09-07)

These rules override the older long-form defaults until the owner explicitly ends testing:

- **Canvas:** vertical 9:16, final render 1080×1920 at 30 fps.
- **Hard duration cap:** **40 seconds**. Aim for 35–40 seconds, never silently exceed 40.
- **Word budget:** normally 85–110 spoken words; measure the actual narration before rendering.
- **Visual budget:** at most 10 generated images; usually 6–8 is enough for 40 seconds.
- **Animated hook:** the first generated story image is uploaded to Cloudinary, then animated with Agnes image-to-video. For stickman stability, prefer a short 49-frame (~2 s at 24 fps) locked-storyboard clip. Preserve Stiles, composition and line style; freeze character anatomy and request environmental motion plus a controlled camera push. Replace the first static edit segment with the returned clip. If Agnes fails twice, fall back to the static image rather than blocking the full production.
- **Narration during tests:** **do not call ElevenLabs**. Use a non-ElevenLabs test voice approved for that test, or stop and ask what narration source to use.
- **Story rhythm:** hook in the first 1–2 seconds, a visual/story change every 3–6 seconds, payoff before second 35, short CTA/question only if time remains.
- **Character reference:** Stiles must match [`characters/stiles.md`](characters/stiles.md).

The former 6–10 minute 16:9 format is parked for later; do not use it during vertical testing.

## 5. Cadence

- **Ideal:** 2 videos/week. **Minimum:** 1/week. Consistency beats volume.

## 6. Content pillars

| Pillar | What it covers | Share |
|---|---|---|
| **Reddit Gold** | The best true-life threads (AskReddit "what's the most insane thing…", r/oddlyspecific stories) — one great thread retold, or a themed set | ~35 % |
| **Plot Twists** | Stories with a reveal that flips everything (owner stories or public threads) | ~30 % |
| **Wild Encounters** | Chance meetings, strangers, "only in real life" moments, mildly creepy-but-true | ~20 % |
| **Karma & Comebacks** | Satisfying justice / instant-comeback stories | ~15 % |

## 7. Topic recipe (how the 5 ideas are generated)

- **Mix pillars** — five offers never come from one pillar (e.g. 2× Reddit Gold, 1× Plot Twists, 1× Wild Encounters, 1× Karma).
- **Concrete beats vague** — *"The roommate who wasn't real"* yes · *"Creepy stories"* no.
- **Real & linkable** — the story must trace to a public thread or the owner; the offer names the source type.
- **One emotion per idea** — name it in the one-liner (twist / chill / justice / laughter).
- **Evergreen default**; trends only if the story itself is timeless.
- **Banned:** clearly fabricated "and everyone clapped" tier stories, doxxing or identifying details, stories about real minors in sensitive contexts, hateful or graphic content, anything needing gore to tell.
- **Honesty rule:** real Reddit stories are retold as *"shared by a Reddit user"*, never as verified news or the agent's own experience.

## 8. Script rules (feeds Step 4 voiceover)

- English (en-US), conversational, present/past mix like spoken storytelling.
- Speaker tags from the contract in README Step 4.1: `NARRATOR:`, `JESSIE:`, `EXTRA-*:` only when declared and approved.
- **Dialogue in short lines** (≤ ~25 words); narration lines ≤ ~45 words — better TTS prosody and easier scene mapping.
- Mark scene/mood breaks with `## Scene:` headings (used by Step 6 animation, ignored by Step 4 audio).
- No filler ("um", "in this video we will…"), no false drama, no emoji in speech.
- Every story beat earns its place: setup → doubt → twist → payoff.

## 9. Story structure template (one main story)

| Beat | Approx. | What happens |
|---|---|---|
| **Cold open** | 0:00–0:35 | Start at the twist/teaser ("The apartment had one rule: never open the closet."). |
| **Meet the cast** | ~0:35–1:30 | Set the scene; Stiles introduces the ordinary situation. |
| **Rising weirdness** | middle | Small strange things; Jessie's asides raise the doubt ("So… you're sure about that?"). |
| **The turn** | ~last third | The reveal — payoff of the title's promise. |
| **Landing** | last 30 s | Quick recap, one comment question, subscribe CTA. |

## 10. Voice direction

> **Vertical test override:** do not generate new ElevenLabs audio during testing. The voice qualities below remain the creative target, but use a non-ElevenLabs test voice selected for the run. Save ElevenLabs credits until the owner ends test mode.

- `NARRATOR` (Stiles): masculine, warm, curious storyteller; slightly amused; never shouty; en-US.
- `JESSIE`: feminine, expressive, quicker; can do deadpan, skeptic, and "oh no" energy; en-US.
- Settings ballpark: `stability 0.35–0.5`, `similarity_boost 0.75–0.85` (fine-tuned once per voice, then reused).
- Chosen voice IDs are recorded in the frontmatter above; extras per video are recorded in the script header.
- Final pacing: merged audio at `atempo ≈ 1.07` (see README Step 4.4) — scripts must already read at that pace.

## 11. Visual identity

- **Canvas (test mode):** 9:16 vertical, 1080×1920. Flat pastel/neutral backgrounds; thin black stick figures. Stiles must match [`characters/stiles.md`](characters/stiles.md); Jessie retains her ponytail and equally minimal proportions.
- **Motion and editing:** every otherwise-static image receives a clearly perceptible but gentle **3–5% zoom** over its full screen time, alternating between push-in and pull-out where composition allows. Never leave a still perfectly static. Images must depict what the narration is discussing at that moment. Never divide the duration into equal image intervals; cut on meaningful words, reveals and action beats. Short high-impact shots may last ~1.5–3 s, while context shots may hold ~4–7 s when the audio supports them.
- **Background:** clean generated scene art is preferred during testing. Ambient third-party footage is optional and must never distract from the figures.
- **Captions:** exactly **one word visible at a time**, synchronized to measured word-level timestamps from the final audio. Center horizontally around **64% of frame height** (slightly below center), default **60 px** at 1080×1920. Use bold white type, with selected hook/reveal words in warm yellow, and only a restrained dark outline/shadow—**no black rectangle/background box**. Each word should pop smoothly (`~78% → 108% → 100%`) with a very short soft fade. Never estimate timing from character count; run speech alignment against the actual final audio, then map recognized timestamps back to the approved script.
- **Thumbnails:** bold stickman moment from the video + ≤ 5 words; consistent palette; honest to the content.
- **Intro/outro:** no separate 4-second sting during ≤40 s tests; the hook starts immediately.

## 12. Packaging (used from Step 7 onward)

- Titles English, ≤ 60 chars, twist-led but not lying ("The Roommate Who Wasn't Real" ✓, "He Ruined My Life (GONE WRONG)" ✗).
- Description: 1–2 line hook → chapters → source link(s) → one comment question.
- No keyword stuffing; honest thumbnail.

## 13. Quality checklist (every video before approval)

- [ ] Story is real + linkable or owner-provided; anonymity kept; source recorded.
- [ ] Speaker tags parse cleanly; dialogue lines short enough for good TTS.
- [ ] No banned topics; nothing presented as verified when it isn't.
- [ ] English correct (US spelling); script reads aloud naturally at final tempo.
- [ ] Voiceover: all lines present, ordered, one merged file, tempo 1.05–1.12, duration in target range.
- [ ] Background clips rights-safe, subtle, source noted (when used).
- [ ] Thumbnail/title/description consistent and honest; YouTube policy safe for general audience.

## 14. Rules: do / don't

| ✅ Do | ❌ Don't |
|---|---|
| Tell the story with a clear twist/payoff | Drone, pad runtime, or add fake drama |
| Keep real stories real + anonymous + sourced | Present unverified posts as news/facts |
| Short spoken lines, natural dialogue | Run-on 60-word TTS paragraphs |
| Keep the same two voices + stickman look | Change narrator/design every video |
| Use backgrounds subtly (Step 5) | Copy a clip as the video's main content |
| Stay in English (en-US) | Mix languages in titles/scripts |

## 15. KPIs & iteration (used from Step 10 onward)

- Retention curve per beat (where do viewers leave at the "doubt" stage? → tighten setup).
- CTR (is the twist-titled thumbnail honest and clickable?).
- Comments on the closing question → next topic batch.
- Pillar performance → rebalance §6 shares every ~10 videos.

---

*Plan v2.0 — single-channel stickman story studio. Changes bump `plan_version`.*

## Changelog

- **2026-09-07** — v2.0: rebuilt around one channel, **StilesGuy** (stickman true-story channel; Stiles + Jessie); two default ElevenLabs voices; steps 4 (voiceover) and 5 (YouTube background via GitHub Actions) added to the pipeline.
- **2026-09-07** — v2.1: ElevenLabs API key stored in local `.env` (gitignored — repo is public); `elevenlabs: ready`. On-sandbox verification blocked by egress restrictions → confirm via `Test ElevenLabs Key` workflow once it runs on the default branch.
- **2026-09-07** — v2.2: vertical test mode enabled: ≤40 seconds, ≤10 generated images, no new ElevenLabs TTS during tests, and word-level captions (one word at a time, below center, no background box). Canonical Stiles front/back T-pose stored on Cloudinary and documented in `characters/stiles.md`.
- **2026-09-07** — v2.3: captions increased from 54 px to 60 px. Future tests animate the first hook image with Agnes image-to-video, using a Cloudinary first-frame URL and falling back to the static frame after two failures.
- **2026-09-07** — v2.4: Agnes prompt lessons from live tests: prefer a 49-frame (~2 s) locked-storyboard hook for stickman art; freeze characters and animate environment/camera only. Static images now receive a clearly visible but gentle 3–5% push-in or pull-out instead of appearing perfectly still.
