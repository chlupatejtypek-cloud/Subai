---
id: stilesguy
name: "Stiles Psychology"
status: active
content_language: en-US
credentials:
  elevenlabs: ready      # parked during vertical testing
  fish_audio: ready      # API key verified; encrypted Actions secret + local gitignored .env
  youtube: none          # none | pending | connected (future, Step 9)
tts:
  provider: elevenlabs   # parked production provider
  test_provider: fish_audio
  fish_model: s2.1-pro-free
  fish_reference_id: c5f56a6cc2ec4fa8920cb4c5889a3fb7  # Slax — calm measured male educational narrator
  fish_secondary_reference_id: c2623f0c075b4492ac367989aee1576f  # Paula — articulate professional female educator
  speed: 1.05
  model: unset           # ElevenLabs model used only after test mode ends
  voices:
    narrator: unset      # ElevenLabs voice_id — Stiles, masculine, warm storyteller (en-US)
    secondary: unset     # ElevenLabs voice_id — Jessie, feminine, expressive (en-US)
    extras: []           # optional extra voices, added per video only with owner approval
plan_version: "3.1"
production_mode: "vertical-test"
test_constraints:
  canvas: "1080x1920"
  max_duration_seconds: 40
  max_generated_images: 10
  elevenlabs_tts: false
  animation: "up to 10 Agnes attempts at 97 frames / ~4 seconds; fixed generated camera; retain passed clips only; post-production punch on hook"
  captions: "one word at a time; word-aligned; 60 px; no background box"
created: 2026-09-07
updated: 2026-09-07
---

# Stiles Psychology

> **Tagline:** *Tiny figures. Big psychology.*

Research-led English psychology channel using premium minimalist stick-figure stories to explain why everyday minds behave the way they do. Each short opens with a relatable psychological tension, visualizes the mechanism through **Stiles**, and lands on one evidence-informed action viewers can try. Reddit-story sourcing is retired as the channel's focus.

---

## 1. Characters

| Character | Who | Voice role |
|---|---|---|
| **Stiles** | Main stickman — male, round head, slightly crooked smile. Everyman narrator and default "hero" of the story. | `NARRATOR` (always present) |
| **Jessie** | Female stick figure — ponytail, a bit more expressive. Co-host, skeptic sidekick, and the voice that reads quotes / plays the other characters. | `JESSIE` (always available) |

- Other characters in a story are played by **Stiles/Jessie voices in character** or (rarely, with owner approval) short-lived `EXTRA-*` voices.
- Stick-figure design stays minimal and consistent: thin black strokes, flat pastel scene backgrounds, the two heroes always recognizable.

## 2. Purpose & promise

- Turn credible psychology research into memorable, visual explanations of everyday behavior.
- Start with a relatable surprise, explain one mechanism without jargon inflation, and give one realistic action.
- Build an evergreen library around attention, habits, emotions, relationships and cognitive biases.
- Educate rather than diagnose. Avoid fake neuroscience, deterministic body-language claims, mental-health labeling and individualized treatment advice.

## 3. Audience

| Dimension | Value |
|---|---|
| Geography | Global English-speaking (US/UK/CA/AU dominant) |
| Age | 16–34 core |
| Mindset | Curious viewers who want evidence-informed explanations of procrastination, attention, habits, emotions, relationships and thinking errors |
| Consumption | Mobile-heavy, suggested-feed heavy, often binged; sound on |

## 4. Format & length

### Current mode: vertical testing (owner decision, 2026-09-07)

These rules override the older long-form defaults until the owner explicitly ends testing:

- **Canvas:** vertical 9:16, final render 1080×1920 at 30 fps.
- **Hard duration cap:** **40 seconds**. Aim for 35–40 seconds, never silently exceed 40.
- **Word budget:** normally 85–110 spoken words; measure the actual narration before rendering.
- **Visual budget:** at most 10 generated images; usually 6–8 is enough for 40 seconds.
- **Agnes clips:** generate up to **10 story-specific source scenes** for a ≤40 s test and, when each frame offers a safely isolated environmental action, attempt a **97-frame / ~4 s** Agnes clip. Agnes camera must remain fixed: no generated zoom, pan, dolly or reframing. Preserve Stiles anatomy and scene composition. Inspect first/middle/last frames at minimum; any body morphing, disappearance, major re-composition or camera drift fails QC and that scene falls back to its rich still with controlled editorial motion. Never include a failed clip merely to reach a count.
- **Hook punch:** the only standard camera-motion exception is post-production, not Agnes generation: start at 100%, punch quickly to about 105% in ~0.23 s, then ease back to 100% by the end of the four-second opening clip.
- **Narration during tests:** **do not call ElevenLabs**. Use Fish Audio `s2.1-pro-free` at default speed **1.05** with provider timestamps. Default dialogue balance is roughly 65–70% Slax (male explainer) and 30–35% Paula (female viewer question, inner thought or concise counterpoint), avoiding long uninterrupted monologues. Use restrained S2.1 `[bracket]` expression cues—normally one clear cue per sentence and never conflicting stacks.
- **Story rhythm:** hook in the first 1–2 seconds, a visual/story change about every 4 seconds, payoff before second 36, short CTA/question only if time remains.
- **Sound design:** use Fish expression tags for vocal performance and at most 3–5 restrained scene-motivated SFX (e.g. intro whoosh, phone click, mechanism hit, completion chime). Keep them below dialogue; never add a sound to every word. Fish lists separate cinematic SFX generation as a platform capability, but the current repository client covers TTS only, so do not send SFX prompts to `/v1/tts`.
- **Character reference:** Stiles must match [`characters/stiles.md`](characters/stiles.md).

The former 6–10 minute 16:9 format is parked for later; do not use it during vertical testing.

## 5. Cadence

- **Ideal:** 2 videos/week. **Minimum:** 1/week. Consistency beats volume.

## 6. Content pillars

| Pillar | What it covers | Share |
|---|---|---|
| **Everyday Mind** | Procrastination, motivation, attention, memory and decision-making | ~35 % |
| **Emotions & Self-Regulation** | Avoidance, anxiety mechanisms, rumination, self-compassion and coping | ~25 % |
| **Social Psychology** | Attachment, boundaries, persuasion, conformity and relationship patterns | ~25 % |
| **Biases & Experiments** | Cognitive biases and classic findings, with limitations and replication context | ~15 % |

## 7. Topic and research recipe

- **Mix pillars** — five offers span at least three psychology pillars.
- **Concrete beats vague** — *"Why procrastination feels like relief"* yes · *"Psychology facts"* no.
- **Research before scripting** — use at least one primary or peer-reviewed source plus an accessible corroborating source. Record links and the claim each supports.
- **Benchmark responsibly** — inspect current successful Shorts on the same question; borrow pacing principles and audience framing, never wording, footage or distinctive creative expression.
- **One mechanism per short** — do not compress multiple theories into a false universal explanation.
- **Useful ending** — offer one small evidence-informed action, with appropriate uncertainty.
- **Banned:** fake dopamine claims, diagnosis-by-listicle, manipulative “dark psychology tricks,” deterministic body-language claims, stigma, individualized medical advice and sensationalized experiments stripped of limitations.

## 8. Script rules (feeds Step 4 voiceover)

- English (en-US), conversational and precise.
- Default to one calm narrator. Add dialogue or a second voice only when it materially improves the explanation.
- Keep narration lines short enough for natural TTS and clear scene mapping.
- Open with a surprising but defensible reframe in the first sentence; explain the causal chain visually; end with one concrete action.
- No filler, false certainty, invented statistics, fake clinical authority, jargon dumps or emoji in speech.
- Qualify claims when evidence is correlational, mixed, population-specific or preliminary.

## 9. Vertical psychology structure

| Beat | Approx. | What happens |
|---|---|---|
| **Hook** | 0–4 s | Relatable contradiction or surprising reframe, carried by the Agnes action shot. |
| **Experience** | 4–12 s | Show the familiar situation and emotion without diagnosing the viewer. |
| **Mechanism** | 12–24 s | Explain one research-grounded psychological loop in plain language. |
| **Cost/reframe** | 24–29 s | Show why the short-term response persists or what it costs. |
| **Action** | 29–38 s | Give one specific, small step tied directly to the mechanism. |
| **Landing** | optional final 2 s | Memorable final line; CTA only when it does not crowd the lesson. |

## 10. Voice direction

> **Vertical test override:** do not generate new ElevenLabs audio during testing. Use Fish Audio voice **Slax** (`c5f56a6cc2ec4fa8920cb4c5889a3fb7`) with provider-native timestamps unless the owner approves another voice.

- `NARRATOR` (Stiles): masculine, calm, measured educational explainer; warm and curious; never shouty; en-US.
- `JESSIE`: feminine, expressive, quicker; can do deadpan, skeptic, and "oh no" energy; en-US.
- Settings ballpark: `stability 0.35–0.5`, `similarity_boost 0.75–0.85` (fine-tuned once per voice, then reused).
- Chosen voice IDs are recorded in the frontmatter above; extras per video are recorded in the script header.
- Final pacing: merged audio at `atempo ≈ 1.07` (see README Step 4.4) — scripts must already read at that pace.

## 11. Visual identity

- **Canvas (test mode):** 9:16 vertical, 1080×1920. Flat pastel/neutral backgrounds; thin black stick figures. Stiles must match [`characters/stiles.md`](characters/stiles.md); Jessie retains her ponytail and equally minimal proportions.
- **Composition:** premium minimalism must not become emptiness. Fill scenes with relevant foreground, midground and background elements, closer framing, lighting depth, props and character interaction. Reserve only a narrow caption-safe lane; never ask the image model for a large empty caption area or panel.
- **Motion and editing:** apply the standardized intro punch to the first accepted Agnes clip. Other accepted Agnes clips receive no additional camera motion. Every fallback still gets exactly one composition-aware preset: **(A)** slow 3–5% push-in, **(B)** slow 3–5% pull-out, or **(C)** pre-scale to roughly 105–110% and drift gently left-to-right or right-to-left.
- **Background:** clean generated scene art is preferred during testing. Ambient third-party footage is optional and must never distract from the figures.
- **Captions:** the only approved style is central preset [`config/caption-style.json`](config/caption-style.json), currently `stiles-word-pop-v1`. Render through `tools/render-word-captions.py`; production scripts must not redefine appearance. It locks DejaVu Sans Bold 60 px, `(540,1230)`, white with selected warm-yellow words, 3 px dark outline, 1 px shadow, no box, uppercase, and pop `78% → 108% → 100%`. Use provider-native Fish timestamps and enforce zero overlaps / exactly one visible word.
- **Thumbnails:** bold stickman moment from the video + ≤ 5 words; consistent palette; honest to the content.
- **Intro/outro:** no separate 4-second sting during ≤40 s tests; the hook starts immediately.

## 12. Packaging (used from Step 7 onward)

- Titles English, ≤60 characters, curiosity-led but scientifically honest ("Why Procrastination Feels Like Relief" ✓, "This Brain Hack Cures Laziness" ✗).
- Description: one-line hook → concise educational context → research source links → general-education disclaimer when relevant.
- No keyword stuffing, clinical promises or misleading brain imagery; thumbnail must represent the actual mechanism.

## 13. Quality checklist (every video before approval)

- [ ] Every factual mechanism is supported by recorded research; no source says more than it actually found.
- [ ] Benchmark inspiration is documented without copying wording or creative assets.
- [ ] No diagnosis, fake neuroscience, invented statistic, clinical promise or individualized treatment advice.
- [ ] English correct (US spelling); script reads naturally and remains under 40 seconds.
- [ ] Fish voiceover contains all lines; native word timestamps are preserved and final loudness is suitable.
- [ ] Background clips rights-safe, subtle, source noted (when used).
- [ ] Thumbnail/title/description consistent and honest; YouTube policy safe for general audience.

## 14. Rules: do / don't

| ✅ Do | ❌ Don't |
|---|---|
| Explain one mechanism with a clear payoff | Cram in unrelated psychology facts |
| Research claims and preserve uncertainty | Present pop-psychology claims as settled science |
| Use short spoken lines and visual causal chains | Read an abstract or jargon list aloud |
| Keep the same narrator and Stiles look | Change voice/design every video |
| Learn pacing from benchmarks | Copy wording, footage, thumbnails or signature expression |
| Stay in English (en-US) | Mix languages in titles/scripts |

## 15. KPIs & iteration (used from Step 10 onward)

- Retention curve per beat (where do viewers leave at the "doubt" stage? → tighten setup).
- CTR (is the twist-titled thumbnail honest and clickable?).
- Comments on the closing question → next topic batch.
- Pillar performance → rebalance §6 shares every ~10 videos.

---

*Plan v3.0 — single-channel research-led stickman psychology studio. Changes bump `plan_version`.*

## Changelog

- **2026-09-07** — v2.0: rebuilt around one channel, **StilesGuy** (stickman true-story channel; Stiles + Jessie); two default ElevenLabs voices; steps 4 (voiceover) and 5 (YouTube background via GitHub Actions) added to the pipeline.
- **2026-09-07** — v2.1: ElevenLabs API key stored in local `.env` (gitignored — repo is public); `elevenlabs: ready`. On-sandbox verification blocked by egress restrictions → confirm via `Test ElevenLabs Key` workflow once it runs on the default branch.
- **2026-09-07** — v2.2: vertical test mode enabled: ≤40 seconds, ≤10 generated images, no new ElevenLabs TTS during tests, and word-level captions (one word at a time, below center, no background box). Canonical Stiles front/back T-pose stored on Cloudinary and documented in `characters/stiles.md`.
- **2026-09-07** — v2.3: captions increased from 54 px to 60 px. Future tests animate the first hook image with Agnes image-to-video, using a Cloudinary first-frame URL and falling back to the static frame after two failures.
- **2026-09-07** — v2.4: Agnes prompt experiment used a 49-frame locked-storyboard clip to reduce morphing; this was useful for diagnosis but is superseded by v2.5.
- **2026-09-07** — v2.5: clarified final motion language: Agnes hook is 97 frames / ~4 s with a fixed camera and meaningful scene action—no zoom. Editorial motion applies only to subsequent stills via push-in, pull-out, or gentle lateral pan. Fish Audio connected for non-ElevenLabs test narration and provider-native timestamp alignment.
- **2026-09-07** — v3.0: channel pivoted from Reddit/true-story retellings to research-led everyday psychology. Added evidence and benchmark rules, psychology pillars, an education-not-diagnosis boundary, and approved Fish voice Slax. First test: *Why Procrastination Feels Like Relief*.
- **2026-09-07** — v3.1: locked subtitle appearance in a central preset; added Paula as a second Fish voice, 1.05 speed and restrained expression tags/SFX. Raised visual target to 10 richer scenes, added a standardized post-production intro punch, and retained only Agnes clips that pass camera/anatomy QC.
