# 🎬 Subai

> **One channel. One research-led stickman psychology studio. Fully run by an AI agent.**

Subai is the playbook for **Stiles Psychology** — a faceless English-language YouTube channel where premium minimalist stick figures explain evidence-informed everyday psychology. **Stiles** visualizes one relatable mechanism per Short and ends with one realistic action viewers can try.

This repository is the instruction manual the agent reads when it is dropped into a session. It covers topic research, benchmark analysis, an English script, Fish Audio narration with native timestamps, generated Stiles scenes, a fixed-camera Agnes hook, moving stills, one-word captions, quality control and durable Cloudinary delivery.

The agent treats this manual as **inspiration, not 100% strict law**: it follows it, but when reality conflicts with it, it adapts, tells the owner what it changed, and keeps going.

---

## ⚡ Golden rules (read first)

1. **"Subai is ready."** — Every fresh session on this repo starts with this exact sentence. Then the agent follows **Step 1**.
2. **One channel.** This repo is about **Stiles Psychology** only — see [`channel.md`](channel.md). No other channels are managed here.
3. **English, always.** All channel content — ideas, titles, scripts, narration — is **English (en-US)**. Talking *to the owner* happens in whatever language the owner uses.
4. **Inspiration, not law.** If a step is unclear or conflicts with the owner's request, improvise sensibly — and tell the owner what you did.
5. **When in doubt, ask.** Guessing about the topic, the story, the source, or money is worse than one short question.
6. **Research before scripting.** Every psychological mechanism needs a recorded credible source. Never invent statistics, diagnoses, clinical promises or dopamine/neuroscience certainty.
7. **Secrets never go into git.** This repo is **public**. API keys live in `.env` (root, gitignored) or in GitHub Actions secrets — never in committed files. (Details: [Credentials & secrets](#-credentials--secrets).)
8. **Go step by step.** Do not jump ahead to the voiceover or to visuals while the manual only asked for a topic.

> **🤖 Agents:** before you assume you can push to this repo, read [`AGENT.md`](AGENT.md).
> It explains how write access actually works here (credentials are handed over per session —
> there is deliberately no token stored in the repo), how to configure `git push` with a PAT
> without hitting the usual auth error, and how the ElevenLabs key is handled.

---

## 🗺️ The pipeline (overview)

> **🧪 Current vertical psychology test mode (v3.0):** until the owner explicitly ends testing, each video is
> 9:16, no longer than 40 seconds, uses at most 10 generated images, uses Fish Audio rather than
> ElevenLabs for test narration after voice approval, and shows exactly one word of captions at a time below frame center with no
> background box. The precise settings and canonical Stiles reference are in
> [`channel.md`](channel.md) and [`characters/stiles.md`](characters/stiles.md). These rules
> override older long-form examples elsewhere in this playbook.

Only steps marked ✅ are fully specified. The others are designed together with the owner, one at a time.

| # | Step | Status |
|---|------|--------|
| 1 | **Topic pick** — 5 suggestions + custom option, per the channel plan | ✅ **LIVE** |
| 2 | **Research & benchmark** — primary evidence plus comparable successful Shorts | ✅ **LIVE** |
| 3 | **Script** — one mechanism, ≤40 seconds, evidence-informed action | ✅ **LIVE** |
| 4 | **Voiceover** — Fish Audio Slax with native word timestamps; ElevenLabs parked | ✅ **LIVE** |
| 5 | **Visual plan** — ≤10 generated Stiles scenes mapped to narration beats | ✅ **LIVE** |
| 6 | **Animation & assembly** — fixed-camera 4 s Agnes hook, moving stills, one-word captions | ✅ **LIVE** |
| 7 | Packaging — research-honest title, thumbnail and sourced description | 🔜 to design |
| 8 | Review, Cloudinary delivery & owner approval | ✅ **LIVE** |
| 9 | Publish to YouTube | 🔜 to design |
| 10 | Analytics & iteration | 🔜 to design |

> ⚠️ While a step is still 🔜, the agent **must not silently improvise the whole production**. It may sketch ideas when the owner asks, but each step becomes part of this manual only after it is designed together.

---

## 📂 Repository map

| Path | What it is |
|------|------------|
| `README.md` | This playbook |
| `channel.md` | The single channel plan — **Stiles Psychology** (identity, research rules, pillars, voice, visual rules) |
| `productions/` | One folder per video (scripts + generated audio/background) — see [`productions/README.md`](productions/README.md) |
| `.github/workflows/fetch-background.yml` | GitHub Actions job that downloads background clips from YouTube (yt-dlp) |
| `.github/workflows/test-elevenlabs.yml` | One-click key check + test TTS (key passed as a run input, never stored) |
| `.env` | Local secrets (ElevenLabs key) — **never committed** |
| `.env.example` | Template for `.env` |

---

## 🪜 Step 1 — Topic pick (LIVE)

### 1.0 · The opening line

The agent's first words in a fresh session are exactly:

> **Subai is ready.**

### 1.1 · Read the plan

1. Read [`channel.md`](channel.md) — the whole plan (identity, pillars, voices, rules). This is the owner's current intent; if it looks stale, say so in one line.
2. Tell the owner in 2–3 sentences: channel = **Stiles Psychology**, videos = English research-led animated psychology Shorts, and that all channel output will be in English.

### 1.2 · Topic trigger

- **Owner gave a psychology topic or question**: treat it as chosen, restate it as a crisp English working title + mechanism angle, then research before scripting.
- **Owner gave nothing** (just "go" / "make a video"): make the **topic offer** below for the channel's default pillars.
- **Owner asks for ideas later**, mid-session: same topic offer, refreshed.

### 1.3 · The topic offer — 5 suggestions + 1 custom

The agent proposes **exactly five psychology topic ideas** following the research recipe and pillars in [`channel.md`](channel.md). Each idea must:

- ask one specific everyday question,
- fit a ≤40-second explanation with one mechanism,
- have credible research likely available,
- offer one useful but non-clinical action,
- rotate across at least three pillars,
- pass the banned-pop-psychology list.

**Presentation format**:

> Here are **5 topic ideas for Stiles Psychology**:
>
> 1. **Why Procrastination Feels Like Relief** — Avoidance can briefly repair mood, teaching the loop to repeat. *(Pillar: Everyday Mind)*
> 2. **…**
> 3. **…**
> 4. **…**
> 5. **…**
> 6. ✍️ **Custom topic** — type a psychology question and I'll research its strongest defensible angle.

### 1.4 · After the pick

- Wait for the owner's choice. Do **not** start the outline or the script yet.
- Lock a **working title** (English, ≤ 60 chars), the **angle/hook**, and the **pillar**; record them in the production folder (`productions/<date>-<slug>/brief.md`).
- Tell the owner what happens next once Steps 2–3 are designed (outline → speaker-tagged script → Step 4 voiceover).
- If the owner chose option 6, help shape the raw idea into a concrete title + angle first.

### 🚫 Step 1 is NOT for

No research dumps, no scripts, no voiceover, no audio, no downloading, no publishing.

---

## Current test-production contract (v3.0)

For psychology Shorts, research and benchmark notes live in `research.md`; plain narration lives in `narration.txt`; Fish Audio Slax generates Opus plus native timestamps; the first source image is animated by Agnes for 97 frames with a fixed camera; all subsequent images receive a composition-aware push, pull or lateral pan; captions use one Fish-aligned word at a time; and the 1080×1920 result is uploaded to Cloudinary before disposable media cleanup. See the latest production folder for a working render implementation.

## Legacy Step 4 — ElevenLabs multi-voice (parked during testing)

> Trigger: this step starts when the owner approves the **script** (`productions/<folder>/script.md`, speaker-tagged as defined in Step 3's contract below) and says "make the audio" (or the equivalent). It does **not** start from a bare topic.

### 4.1 · Input contract — the speaker-tagged script

The script is Markdown, one line per spoken line, each prefixed with a speaker tag. The agent parses **in order** and speaks only tagged lines; everything else in the file is direction/metadata for later steps.

```markdown
# The Roommate Who Wasn't Real   (working title)

NARRATOR: I moved into a new apartment in August. Cheap rent, weird vibes, whatever.
JESSIE: So you never met the landlord?
NARRATOR: Not once. And that should've been my first red flag.
EXTRA-MOM: (a 50-something woman, warm but worried)
NARRATOR: "Mom," I said, "you worry too much."
```

- Tags allowed: `NARRATOR` (Stiles — always), `JESSIE` (always available), `EXTRA-*` (only if the script header declares them and the owner approved extra voices).
- One paragraph per line to speak. Sound-effect placeholders `[SFX …]` are ignored by Step 4 (used by visuals later).
- Step 4 output: one audio file, no silence gaps beyond short natural pauses.

### 4.2 · Prerequisites

- `.env` at repo root contains `ELEVENLABS_API_KEY` (owner pastes the key; the agent writes it into `.env` and **never echoes it back in full**).
- Voice IDs live in the `tts.voices` frontmatter of [`channel.md`](channel.md).
  - If they are `unset`, the agent lists ElevenLabs voices via the **`Test ElevenLabs Key`** workflow (or directly if the sandbox can reach the API), shortlists **two** consistent English (en-US) voices — a masculine warm storyteller for `narrator`, a feminine expressive voice for `secondary` — and confirms the shortlist with the owner before writing the chosen IDs into `channel.md` (the actual voice samples may be auditioned if the owner wants).

### 4.3 · Generate per-line audio

1. For each tagged line in order, call ElevenLabs TTS:
   `POST https://api.elevenlabs.io/v1/text-to-speech/<voice_id>` with `model_id` (current default / fastest quality model), `text` = the line (strip the tag), and `voice_settings` in a sensible storytelling ballpark: `stability ≈ 0.35–0.5`, `similarity_boost ≈ 0.75–0.85`.
2. Save segments as `productions/<folder>/audio/segments/001-narrator.mp3`, `002-jessie.mp3`, … (3-digit order prefix).
3. Handle API limits politely: retry with backoff on 429/5xx; if a line fails repeatedly, stop and tell the owner.
4. **Never re-generate a finished line just to change pacing** — pacing is fixed in step 4.4; fix pacing at the script stage instead.

### 4.4 · Merge into one audio, then speed it up slightly

1. Concatenate segments in order with short **~150–250 ms pauses** between lines (natural rhythm) → `audio/voiceover_raw.mp3`. Example with ffmpeg (concat demuxer with silent gaps, or `apad`/silence insertion between segments).
2. Apply a **slight speed-up that keeps the pitch** (`atempo`), default **1.07**, allowed range **1.05–1.12** — TTS reads a touch slow; the tiny boost adds energy and shortens the video. → `audio/voiceover.mp3`.
3. Optional polish: loudness normalize toward ≈ −16 LUFS (`loudnorm`).
4. The owner may ask for a different tempo once; afterwards this number is reused for the whole video.

### 4.5 · Sanity checks (all must pass)

- [ ] Every tagged line has a segment, in the right order (compare count + speaker sequence vs script).
- [ ] No empty/broken segments (file size sane, `ffprobe` parses each).
- [ ] Final file exists; duration ≈ expected (words ÷ pace × 60, ± 10 %).
- [ ] `voiceover.mp3` plays start to end; no clipping, no robot artifacts on the audition spot-check.
- [ ] Report to the owner: file path, final duration, tempo used, per-voice line counts.

**Output:** `productions/<folder>/audio/voiceover.mp3` — the single narration track that Step 5's background and Step 6's animation will sit on.

---

## Step 5 — Background footage from YouTube via GitHub Actions (LIVE)

> Why GitHub Actions: the agent's sandbox cannot reliably download YouTube videos itself. So downloads run on a **GitHub Actions runner** (yt-dlp), and the agent pulls the finished clip back into the repo folder.

### 5.1 · What we download

Short **ambient / "satisfying" background clips** that sit *behind* the stickman scenes (subtle b-roll: rain on a window, night city timelapse, a cozy fireplace, a train at dusk…). The animation and the narration are the content — the background only sets the mood. One clip per scene mood is enough; keep them short (15–90 s).

Rules:
- Prefer **explicitly free-to-use** sources: add `no copyright` / `royalty-free` / `free to use` keywords to the search, or use a URL the owner provides.
- Never present the clip itself as the video's content; never keep talking/watermarked audio in it; keep a note of the clip's source link in the production folder for credit.
- If a clip is questionable, skip it and pick another — mood is replaceable, rights issues are not.

### 5.2 · The workflow

The repo ships `.github/workflows/fetch-background.yml` (manual trigger, inputs: `query` or `url`, `max_duration`, `height`, `artifact_name`).

The agent runs it like this (from the repo, on this working branch — pass `--ref` so the workflow exists on the ref being run):

```bash
# search-based
gh workflow run fetch-background.yml --ref arena/01a07a66-subai \
  -f query="rain on window background loop no copyright" \
  -f max_duration=45 -f height=720

# or a specific URL
gh workflow run fetch-background.yml --ref arena/01a07a66-subai \
  -f url="https://www.youtube.com/watch?v=..." -f max_duration=60

# watch until it finishes
gh run watch $(gh run list --workflow fetch-background.yml --limit 1 --json databaseId -q '.[0].databaseId') --exit-status

# pull the clip into the production folder
gh run download <run-id> -n background-clip -D productions/<folder>/background/
```

(The exact branch name comes from the current session; `--ref` must point at the branch that contains the workflow file.)

### 5.3 · Verify before use

- [ ] `background/clip.mp4` exists, > ~100 KB, duration ≥ the scene needs (`ffprobe`).
- [ ] No loud/talking audio or watermarks visible on a spot check.
- [ ] Source link recorded in the production folder.
- If the download fails twice with different queries, stop and tell the owner (runner network or YouTube blocking) — do not silently skip backgrounds or hotlink other videos.

---

## Steps 2–3 & 6–10 (🔜 to be designed)

| Step | What it will cover |
|---|---|
| **2 · Research & outline** | From chosen topic/source → verified story beats, structure, source links, ~30 % of the work done before writing |
| **3 · Script** | English master script per [`channel.md`](channel.md) §script rules, **speaker-tagged** exactly as Step 4.1 needs it |
| **6 · Animation & visuals** | Rendering Stiles & Jessie as stick figures, scene direction from the script, placing background clips, captions |
| **7 · Packaging** | Title (≤60 chars), Stiles Psychology thumbnail, sourced description |
| **8 · Assembly & review** | Final render, quality checklist from the channel plan, owner approval round |
| **9 · Publish** | Upload to YouTube (needs the owner's YouTube/Google credentials — handled outside git) |
| **10 · Analytics** | Retention, CTR, comments → feed back into topic offers |

The owner and the agent design these one at a time. Until then the agent stays inside the LIVE steps.

---

## 🔐 Credentials & secrets

- **This repo is public.** Committing a key = publishing it. Never do it.
- The **ElevenLabs API key** lives in **`.env`** at the repo root (gitignored — see `.env.example`). The agent reads it from there for API calls; the owner can paste the key in chat and the agent stores it into `.env` without printing it back.
- **GitHub Actions secrets** are the right place for anything a workflow needs later (e.g. YouTube upload) — set via `gh secret set NAME` / repo settings.
- Current status: ElevenLabs = `.env` exists → `ready`; YouTube upload = not set up yet.

### 🔑 Verifying the ElevenLabs key

The agent's sandbox may not reach `api.elevenlabs.io` directly (egress is restricted to GitHub in some environments). Whenever the key needs proofing — or a voice needs listing — run the **`Test ElevenLabs Key`** workflow from the Actions tab (or via `gh workflow run test-elevenlabs.yml`) and pass the key as the `api_key` input. The key travels only inside that run and is never written to the repo. Usage:

```bash
# from a session that has push access and egress to api.github.com:
gh workflow run test-elevenlabs.yml --ref <current-branch> \
  -f api_key="sk_..." -f text="Subai is ready. This is a voice test for Stiles." \
  -f voice_id="pNInz6obpgDQGcFmaJgB"
gh run watch $(gh run list --workflow test-elevenlabs.yml --limit 1 --json databaseId -q '.[0].databaseId') --exit-status
gh run download <run-id> -n elevenlabs-test-audio -D media/
```

The workflow reports the account tier + remaining characters, lists the first voices, and uploads a short synthesized sample as an artifact.

---

## ✏️ How this playbook grows

- Steps get designed with the owner one at a time and flip from 🔜 to ✅ LIVE when specified in detail here.
- When a step changes, update the [pipeline table](#-the-pipeline-overview) and bump `plan_version` in [`channel.md`](channel.md) (with a changelog line).
- Keep sections concrete: what the agent does, in what order, what it must not do, and what the output looks like.

---

*Subai — tiny figures, big psychology. 🤖🧠*
