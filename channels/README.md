# 📁 Channels — how channels are stored

Subai can manage **multiple YouTube channels**. Every channel gets exactly **one Markdown file** in this folder. The file is both the channel's identity and its plan — the agent reads it whenever it works on that channel.

## File naming

- One file per channel: `channels/<id>.md` where `<id>` is a short kebab-case slug, e.g. `channels/default.md`, `channels/my-tech.md`.
- `channels/default.md` is special: it is the **fallback channel** used whenever the owner gives no channel and no other channel is active.

## Required fields (YAML frontmatter)

```yaml
---
id: default              # unique slug, matches the file name
name: "Curiosity Vault"  # display name of the YouTube channel
status: active           # active | paused | archived
content_language: en-US  # language of ALL channel output
credentials_status: none # none | pending | connected
plan_version: "1.0"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

The Markdown body then contains the full plan. Mirror the section structure of [`default.md`](default.md): Purpose, Audience, Format & length, Cadence, Content pillars, Topic recipe, Structure template, Voice, Visual identity, Packaging, Quality checklist, Rules, KPIs & iteration, Changelog. Not every channel needs every section in the same depth — but Purpose, Audience, Format, Pillars, Topic recipe and Rules should always exist.

## How the agent picks the working channel

Checked in **Step 1.1** of the README, in this order:

1. The owner names a channel (by `id` or `name`) → use it.
2. Exactly one profile is `status: active` → use it.
3. `channels/default.md` exists and is active → use it as the default.
4. Several profiles are active and none was named → ask the owner which one.
5. No channel exists → tell the owner and offer to create one from the template below.

## Creating a new channel

The agent copies the template below, fills it in **together with the owner** (name, niche, plan), saves it as `channels/<id>.md`, and confirms the choice of `id` and `name`. The owner can also hand over a ready-made profile and the agent just files it and summarizes it.

```yaml
---
id: my-channel           # unique kebab-case slug
name: "My Channel Name"
status: active           # active | paused | archived
content_language: en-US
credentials_status: none # none | pending | connected
plan_version: "1.0"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

```markdown
# <Channel Name>

> **Tagline / one-line positioning.**

## 1. Purpose
Why the channel exists and what it promises viewers.

## 2. Audience
Who it is for (geography, age, mindset, how they watch).

## 3. Format & length
Video type, target duration, structure, captions, script word budget.

## 4. Cadence
How many videos per week / month; preferred schedule.

## 5. Content pillars
The 2–5 recurring topic families, with a suggested share of output each.

## 6. Topic recipe
How video ideas are generated for THIS channel (what is allowed/banned).

## 7. Structure template
The beat-by-beat skeleton every script follows.

## 8. Voice
Narrator style, accent, pace — or "no narration / text-based" if the channel is silent.

## 9. Visual identity
Colors, thumbnail style, footage rules, intro/outro.

## 10. Packaging
Title / description / tags style (used from Step 6 onward).

## 11. Quality checklist
The per-video gate before anything gets approved.

## 12. Rules: do / don't
Hard limits (language, honesty, copyright, YouTube policy).

## 13. KPIs & iteration
What gets measured and how the plan evolves.

## Changelog
Date-stamped changes; bump `plan_version` on every edit.
```

## 🔐 Credentials — what lives here and what does NOT

- **In this folder:** only the `credentials_status` field (`none | pending | connected`). That is enough for every step up to publishing.
- **Never in this folder or anywhere in git:** API keys, OAuth tokens, passwords, refresh tokens, or channel login data. Credentials handling is introduced with **Step 8 (Publish & schedule)** and lives outside the repository (see the [Credentials policy](../README.md#-credentials--secrets-policy)).
