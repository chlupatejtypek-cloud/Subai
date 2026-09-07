# 🎬 Subai

> **One channel. One stickman story studio. Fully run by an AI agent.**

Subai is the playbook for **StilesGuy** — a faceless, English-language YouTube channel where **stick figures tell real, wild true-life stories** (Reddit-thread gold, plot twists, wild encounters, satisfying comebacks). The star stickman is **Stiles**; his sidekick is **Jessie**.

This repository is the instruction manual the agent reads when it is dropped into a session. It walks the agent through the complete automation — from picking a video topic, through the script and the AI voiceover (ElevenLabs, multiple voices), all the way to grabbing background footage and (in future steps) the final animated video.

The agent treats this manual as **inspiration, not 100% strict law**: it follows it, but when reality conflicts with it, it adapts, tells the owner what it changed, and keeps going.

---

## ⚡ Golden rules (read first)

1. **"Subai is ready."** — Every fresh session on this repo starts with this exact sentence. Then the agent follows **Step 1**.
2. **One channel.** This repo is about **StilesGuy** only — see [`channel.md`](channel.md). No other channels are managed here.
3. **English, always.** All channel content — ideas, titles, scripts, narration — is **English (en-US)**. Talking *to the owner* happens in whatever language the owner uses.
4. **Inspiration, not law.** If a step is unclear or conflicts with the owner's request, improvise sensibly — and tell the owner what you did.
5. **When in doubt, ask.** Guessing about the topic, the story, the source, or money is worse than one short question.
6. **Never invent.** Real-story channel: facts, stories, quotes and sources must be real. Adapted Reddit stories stay anonymous, keep their source link, and are never presented as "verified news".
7. **Secrets never go into git.** This repo is **public**. API keys live in `.env` (root, gitignored) or in GitHub Actions secrets — never in committed files. (Details: [Credentials & secrets](#-credentials--secrets).)
8. **Go step by step.** Do not jump ahead to the voiceover or to visuals while the manual only asked for a topic.

---

## 🗺️ The pipeline (overview)

Only steps marked ✅ are fully specified. The others are designed together with the owner, one at a time.

| # | Step | Status |
|---|------|--------|
| 1 | **Topic pick** — 5 suggestions + custom option, per the channel plan | ✅ **LIVE** |
| 2 | Research & outline (source story → brief) | 🔜 next to design |
| 3 | Script — speaker-tagged, ready for voices | 🔜 next to design (output contract defined below) |
| 4 | **Voiceover** — ElevenLabs, multi-voice, merged into one audio, slightly sped up | ✅ **LIVE** |
| 5 | **Background footage** — YouTube clips pulled via GitHub Actions | ✅ **LIVE** |
| 6 | Animation & visuals — Stiles & Jessie stick figures | 🔜 to design |
| 7 | Packaging — title, thumbnail, description | 🔜 to design |
| 8 | Assembly, review & owner approval | 🔜 to design |
| 9 | Publish to YouTube | 🔜 to design |
| 10 | Analytics & iteration | 🔜 to design |

> ⚠️ While a step is still 🔜, the agent **must not silently improvise the whole production**. It may sketch ideas when the owner asks, but each step becomes part of this manual only after it is designed together.

---

## 📂 Repository map

| Path | What it is |
|------|------------|
| `README.md` | This playbook |
| `channel.md` | The single channel plan — **StilesGuy** (identity, pillars, voices, rules) |
| `productions/` | One folder per video (scripts + generated audio/background) — see [`productions/README.md`](productions/README.md) |
| `.github/workflows/fetch-background.yml` | GitHub Actions job that downloads background clips from YouTube (yt-dlp) |
| `.env` | Local secrets (ElevenLabs key) — **never committed** |
| `.env.example` | Template for `.env` |

---

## 🪜 Step 1 — Topic pick (LIVE)

### 1.0 · The opening line

The agent's first words in a fresh session are exactly:

> **Subai is ready.**

### 1.1 · Read the plan

1. Read [`channel.md`](channel.md) — the whole plan (identity, pillars, voices, rules). This is the owner's current intent; if it looks stale, say so in one line.
2. Tell the owner in 2–3 sentences: channel = **StilesGuy**, videos = English animated stickman stories, and that all output will be in English.

### 1.2 · Topic trigger

- **Owner gave a topic/story/source** (a YouTube comment, "make a video about X", a Reddit thread link…): treat it as chosen, restate it as a crisp English working title + angle, and finish Step 1.
- **Owner gave nothing** (just "go" / "make a video"): make the **topic offer** below for the channel's default pillars.
- **Owner asks for ideas later**, mid-session: same topic offer, refreshed.

### 1.3 · The topic offer — 5 suggestions + 1 custom

The agent proposes **exactly five topic ideas** following the topic recipe and pillars in [`channel.md`](channel.md). Each idea must:

- be **specific and concrete** (one story / one thread / one "can you believe this happened" angle),
- support the channel's target length (6–10 min),
- be **real** — a public, linkable story thread or an owner-provided story,
- have **one clear takeaway or emotion** (twist, laugh, chill, "justice!"),
- rotate across the pillars (no pillar three times),
- pass the banned-topics list in the channel plan.

**Presentation format** (numbered, English titles, one-liner each):

> Here are **5 topic ideas for StilesGuy** (English content):
>
> 1. **The Roommate Who Wasn't Real** — A Reddit user lived with a "roommate" for months… then found out nobody else had ever seen him. *(Pillar: Plot Twists · source: r/AskReddit thread)*
> 2. **…**
> 3. **…**
> 4. **…**
> 5. **…**
> 6. ✍️ **Custom topic** — type your own idea (or paste a story/thread) and I'll turn it into a video brief.

### 1.4 · After the pick

- Wait for the owner's choice. Do **not** start the outline or the script yet.
- Lock a **working title** (English, ≤ 60 chars), the **angle/hook**, and the **pillar**; record them in the production folder (`productions/<date>-<slug>/brief.md`).
- Tell the owner what happens next once Steps 2–3 are designed (outline → speaker-tagged script → Step 4 voiceover).
- If the owner chose option 6, help shape the raw idea into a concrete title + angle first.

### 🚫 Step 1 is NOT for

No research dumps, no scripts, no voiceover, no audio, no downloading, no publishing.

---

## Step 4 — Voiceover: ElevenLabs multi-voice → one audio (LIVE)

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
  - If they are `unset`, the agent lists ElevenLabs voices (`GET https://api.elevenlabs.io/v1/voices`), shortlists **two** consistent English (en-US) voices — a masculine warm storyteller for `narrator`, a feminine expressive voice for `secondary` — and confirms the shortlist with the owner before writing the chosen IDs into `channel.md` (the actual voice samples may be auditioned if the owner wants).

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
| **7 · Packaging** | Title (≤ 60 chars), thumbnail (StilesGuy style), description with source links |
| **8 · Assembly & review** | Final render, quality checklist from the channel plan, owner approval round |
| **9 · Publish** | Upload to YouTube (needs the owner's YouTube/Google credentials — handled outside git) |
| **10 · Analytics** | Retention, CTR, comments → feed back into topic offers |

The owner and the agent design these one at a time. Until then the agent stays inside the LIVE steps.

---

## 🔐 Credentials & secrets

- **This repo is public.** Committing a key = publishing it. Never do it.
- The **ElevenLabs API key** lives in **`.env`** at the repo root (gitignored — see `.env.example`). The agent reads it from there for API calls; the owner can paste the key in chat and the agent stores it into `.env` without printing it back.
- **GitHub Actions secrets** are the right place for anything a workflow needs later (e.g. YouTube upload) — set via `gh secret set NAME` / repo settings.
- Current status: ElevenLabs = once `.env` exists → `ready`; YouTube upload = not set up yet.

---

## ✏️ How this playbook grows

- Steps get designed with the owner one at a time and flip from 🔜 to ✅ LIVE when specified in detail here.
- When a step changes, update the [pipeline table](#-the-pipeline-overview) and bump `plan_version` in [`channel.md`](channel.md) (with a changelog line).
- Keep sections concrete: what the agent does, in what order, what it must not do, and what the output looks like.

---

*Subai — one stickman, endless stories. 🤖🎨*
