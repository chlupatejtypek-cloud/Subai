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
  provider: elevenlabs
  fish_audio: parked
  model: eleven_multilingual_v2
  voices:
    narrator: pNInz6obpgDQGcFmaJgB  # Adam — permanent main voice
    secondary: cgSgspJ2msm6clMCkdW9  # Jessica — optional, max 1–2 purposeful questions
    extras: []
  edit_speed: 1.05  # owner approved +5% pacing for future videos; preserve pitch
  background_music: false
  sfx: "intro whoosh plus 1–3 subtle motivated effects"
plan_version: "3.3"
production_mode: "vertical-test"
test_constraints:
  canvas: "1080x1920"
  max_duration_seconds: 40
  max_generated_images: 10
  elevenlabs_tts: true
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
- **Narration:** use ElevenLabs. One consistent male narrator carries nearly the entire Short. Jessica may ask **one or at most two purposeful questions** when that genuinely improves the explanation; do not alternate voices sentence by sentence. Conserve credits by approving the script and voice before synthesis, generating each final line once, and changing pacing in the edit rather than regenerating. Fish Audio is parked.
- **Story rhythm:** hook in the first 1–2 seconds, a visual/story change about every 4 seconds, payoff before second 36, short CTA/question only if time remains.
- **Sound design:** current owner choice is **SFX only, no continuous background music**. Keep dialogue dominant. Standard opening may use one subtle whoosh synchronized to the punch zoom; add only 1–3 further scene-motivated SFX in a ~40 s Short. Never add a sound to every caption/word. Record source URL, creator, download date and license proof for every stock audio asset.
- **Audio sourcing:** Pixabay's official public API covers images/videos, not its music/SFX catalog; a Pixabay API key does not automate audio. Pixabay audio may be downloaded manually, but retain its page URL and license certificate and prefer tracks without the Content ID shield. YouTube Audio Library is the preferred low-risk music source for YouTube; Freesound may be considered later for an automatable SFX API.
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

- `NARRATOR` (Stiles): ElevenLabs premade **Adam** (`pNInz6obpgDQGcFmaJgB`) is the permanent main voice. Reuse it in every Short unless the owner explicitly changes it.
- `JESSICA`: ElevenLabs premade Jessica (`cgSgspJ2msm6clMCkdW9`) is optional and used only for one or at most two concise viewer questions—not continuous dialogue and not necessarily every video.
- Start with `eleven_multilingual_v2`; record final settings after the narrator audition. Generate only from an approved script.
- Owner update after the spotlight-effect Short: future Adam narration uses a modest **1.05× pitch-preserving edit speed-up**. Divide provider timestamps by 1.05 before caption rendering and remap scene timings. Do not alter the already accepted spotlight-effect video. Never regenerate completed narration merely to make it faster.
- Chosen narrator ID and stable settings must remain in frontmatter so later videos sound the same.

## 11. Visual identity

- **Canvas (test mode):** 9:16 vertical, 1080×1920. Flat pastel/neutral backgrounds; thin black stick figures. Stiles must match [`characters/stiles.md`](characters/stiles.md); Jessie retains her ponytail and equally minimal proportions.
- **Composition and full bleed:** premium minimalism must not become emptiness. Fill scenes with relevant foreground, midground and background elements, closer framing, lighting depth, props and character interaction. Every generated source must be **edge-to-edge 9:16 full bleed**: no white/cream margins, matte, border, frame, lower panel or side strip. Never mention a “caption-safe area/lane” in an image prompt—the model repeatedly turned that instruction into a visible white panel. Place captions over the art during editing. Run `tools/full-bleed-check.py` before Cloudinary/Agnes; crop/fix or regenerate any failed source, then inspect the final rendered edges again.
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
- **2026-09-07** — v3.2: Fish voices parked; ElevenLabs restored as production TTS with one dominant male narrator and Jessica limited to 1–2 purposeful questions. Added mandatory full-bleed image validation, banned prompt language that creates caption panels, and defined restrained music/SFX sourcing and licensing rules.
- **2026-09-07** — v3.3: restored the owner's previously selected permanent narrator Adam (`pNInz6obpgDQGcFmaJgB`); Jessica remains optional. Background music is off for now; use only a restrained intro whoosh and 1–3 motivated SFX.
