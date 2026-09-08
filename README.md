> **LATEST OWNER CONTRACT (2026-09-08):** `start` means produce ONE next video using START-WORKFLOW.md; first creative step is research. Future videos40–60s, at least10 distinct generated/accepted/used illustrations. Read RETENTION-RESEARCH.md. This supersedes older duration/image-count advice below. YouTube state now syncs via tools/youtube-sync.py before scheduled publisher runs and before each start; uploaded is not published. Existing media/holds are unchanged.

# Subai — Stiles Psychology

Research-led English psychology Shorts with a consistent stickman character. Owner conversation may be Czech. This repository contains the current production and publication instructions; older contradictory versions are preserved in Git history, not active policy.

## Start here
**Receiving an encrypted handoff? Read [START_HERE.md](START_HERE.md).** Install its supplied secrets securely in your local workspace, read current main, and continue the authorized task without asking the owner to supply everything again.

- [AGENT.md](AGENT.md): authority, credentials and decision rules.
- [PIPELINE.md](PIPELINE.md): end-to-end sequence, stage exits and remaining blockers.
- [HANDOFF.md](HANDOFF.md): exact decryption and installation instructions.
- [channel.md](channel.md), [VISUAL-EDITORIAL.md](VISUAL-EDITORIAL.md): production specification and latest owner feedback.
- [AUTOMATION.md](AUTOMATION.md), [YOUTUBE.md](YOUTUBE.md): what runs unattended and what the account permits.
- [HYPERFRAMES.md](HYPERFRAMES.md): rendering/reproduction details.
- [config/channels.json](config/channels.json): machine-readable channel/settings.
- [calendar](calendar/2026-09-07_2026-10-06.json):90 editorial slots, not90 completed videos.

## Actual automation boundary
Research, writing, visual generation and creative review require an agent session. GitHub Actions automatically publishes only completed, checked `ready` items and refreshes the encrypted handoff. Normal target slots are15:00/19:00/23:00 Europe/Prague. No burst backfill or blind duplicate uploads.

No plaintext secrets belong in this public repository. The encrypted handoff is delivered from Cloudinary; its versioned URL, exact crypto parameters and checksum are in `config/transfer.json`.
