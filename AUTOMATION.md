# Subai automation — current operational contract

## Registry and calendar
`config/channels.json` is the public account registry. A channel links to a Cloudinary account by key, names the exact YouTube channel ID, and references secret NAMES only. The brand Stiles Psychology currently uses authenticated display name Chlupatej Typek; neither is silently renamed. Do not infer a Google email address from channel metadata.

Canonical live calendar: `calendar/2026-09-07_2026-10-06.json`. CSV and Markdown are initial editorial exports, not the live upload ledger. 90 English topics, three/day, September 7–October 6 inclusive. Slots in Europe/Prague; explicit UTC timestamps included. First-day late-evening exceptions reflect setup at ~22:00; they are targets, not promises. Research/action proposals must be validated before scripting. Normal times 15:00, 19:00, 23:00 are initial test slots, not evidence of optimal performance.

## What runs without the chat
1. `publish-calendar.yml` runs at minute 17 and 47 each hour (GitHub cron UTC). It validates config, reports unfinished overdue slots and uploads ONLY `ready`, QA-passed finals scheduled 30 minutes–48 hours ahead. GitHub can delay scheduled jobs; it is not an exact-minute scheduler. YouTube's future `publishAt` does the final timing.
2. The uploader refreshes OAuth, verifies the exact registered channel, downloads only a registered Cloudinary MP4, verifies SHA256 and probes actual dimensions, fps, duration and audio. It uploads privately with future publication time. It checks the returned schedule rather than assuming success.
3. A durable `upload_started` marker is pushed before upload. If response/state saving is ambiguous, automatic retries are blocked (`needs_reconciliation`) to prevent duplicates. Inspect YouTube Studio/API before clearing the marker. No public resumable-session URLs or OAuth values are stored.
4. `refresh-handoff.yml` refreshes the encrypted bootstrap on relevant main changes, by manual dispatch and daily at 04:13 UTC. Existing owner credentials are decrypted IN MEMORY, current runtime secrets are merged, current tracked docs/config/calendar are added, and only ciphertext is uploaded to Cloudinary. This preserves the original owner-supplied Git PAT without making a second separate broad PAT secret. Workflows with permission to decrypt the handoff must be treated as highly trusted.
5. Both workflows share a concurrency group to avoid racing main's state commits. No force pushes. A GitHub-token calendar commit does not itself trigger another workflow, so the daily handoff refresh captures scheduled state updates.

## What is NOT autonomous yet
**The 90 videos are not generated.** Current hosted image-generation tools require an agent session; GitHub Actions cannot call those chat tools. Research, script writing, image generation, assembly and semantic audiovisual review still require an agent production run. Merely running a cron cannot invent these capabilities. This release automates handoff/account configuration and publication of completed work, not unattended 90-video manufacturing. No paid Fish audio, images or Agnes jobs were generated during this configuration task.

To close this gap later, provision a trusted production runner with documented model endpoints, source/research access, cost limits and resumable job IDs; do not scrape browser sessions or silently reuse an old video's art for unrelated topics. Monthly credit consumption is unknown until actual production measurements exist. The owner authorized three productions per day, not unlimited failure retries.

## Production handoff and QA
Each calendar item progresses `planned -> researching -> scripted -> producing -> ready -> upload_started -> scheduled`. `published` requires a later actual API/Studio check; it is not inferred from the calendar clock. `blocked` and `needs_reconciliation` require investigation. JSON is the live state. Research/production stages are set by the producer, not the publisher.

Before `ready`, set:
- `research_status: verified`, at least two HTTPS `research_sources` (one primary/peer-reviewed, one corroborating).
- Accurate `description`, title ≤60 chars, `asset_url` on this channel's Cloudinary cloud, lowercase hex `asset_sha256`, measured `duration_seconds` ≤40.
- `qa` with true values for `research_verified`, `script_verified`, `voice_verified`, `character_verified`, `full_bleed`, `captions_aligned`, `captions_no_overlap`, `audio_verified`, `visual_review_passed`, `rights_verified`.
- `qa.reviewed_by`, ISO `qa.reviewed_at`, `qa.source_image_count` 1–10, `qa.voice_provider: fish_audio`, `qa.voice_reference_id: fb7ec16ca51a45a5a4db881244d7990a`.
- These are attested findings, not flags to auto-fill. Record supporting evidence in the production folder.

Narrate through `tools/fish-tts-with-timestamps.py --text-file ... --output ...`. Default reference comes from the registry. Preserve native alignment and use the locked caption renderer. Adam is parked; its approved +5% edit speed does not silently alter the new Fish voice. Existing accepted video is not remade or automatically inserted into the new Fish-only calendar.

## Commands
```bash
pip install -r automation/requirements.txt
python -m unittest discover -s tests -v
python tools/calendar-report.py
python tools/youtube-publish.py                     # safe dry run
python tools/youtube-publish.py --verify-auth        # no upload
# Runtime execution normally belongs to the serialized Actions workflow:
python tools/youtube-publish.py --execute --commit-state
```
Never run multiple local publishers simultaneously. Production workflow serializes all publication jobs; local `--execute` without durable committed state is for a controlled single operator only.

## Secret provisioning
Owner-run `tools/configure-automation-secrets.py` requires `.env` loaded into environment, PyNaCl, gitignored `credentials/youtube-client.json`, token JSON in `.git/credentials`, and `HANDOFF_PASSPHRASE` provided separately. It sets encrypted Actions secrets for Fish, Cloudinary, YouTube client/refresh token, handoff passphrase and other existing media providers. It never outputs secret values.

`tools/build-handoff.py --upload` refreshes the same raw Cloudinary public ID. `config/transfer.json` records the NEW versioned URL and SHA256. Use that version, not the old immutable link. Encryption remains compatible OpenSSL AES-256-CBC with PBKDF2-SHA256 / 600000 iterations. The owner expressly chose the original weak password; rotation remains recommended. A public SHA256 checks identity/corruption, not secrecy or strong password entropy.

## External blockers and recovery
- Successful refresh and channels.list were verified, but OAuth consent Testing/Production status cannot be inferred. Testing-mode offline tokens can expire after seven days. Reauthorization needs the owner; re-encrypting a token does not extend its validity.
- Project upload-audit status is unknown. Unverified YouTube API projects can restrict API uploads to private. A scheduled metadata response is not proof a public audit restriction has been lifted. An actual future-public test/audit check is still needed; this task made no test upload.
- No new Google consent for unrelated scopes, automatic account renaming, deletions, comments or channel changes.
- On error: fail closed, report in Actions, preserve ledger. Do not lower QA, switch voices, backdate dates or upload duplicates.
- Revoke/rotate compromised credentials at their provider, then reprovision Actions and rebuild handoff. Old publicly accessible ciphertext versions may remain cached; replacing the latest file does not revoke old tokens.

## Owner-authorized immediate release
For an explicit owner request to publish a specific video now, record the item's `publication_override` (`mode: immediate_public`, `authorized_by: owner`, date/reason) without rewriting its historical planned slot. With all normal content/technical QA passed and status `ready`, use `tools/youtube-publish.py --execute --commit-state --publish-now-id ITEM_ID`. This uploads with public visibility and omits `publishAt`. The default scheduled workflow remains unchanged. The immediate response is recorded as `uploaded_public_pending_processing` or `uploaded_private`; only a subsequent videos.list status/processing verification can mark it `published`. Never treat a private/API-restricted upload as a public success, or upload it again as a workaround.

## Owner pacing feedback — phone-checking V2
Default future Fish post-edit is now 1.06× without pitch shift, after measured long-pause trimming. Preserve short breaths and never cut inferred word gaps unless actual waveform silence confirms them. Remap captions through every cut and speed change, then verify all words by ASR. New production targets ten unique scene images rather than repeatedly revisiting seven. This does not authorize re-uploading revisions to an already public video: keep the published ledger intact and store alternate renders under revision records pending owner review. The existing TTS helper now collapses script layout whitespace to avoid extra paragraph pauses.
