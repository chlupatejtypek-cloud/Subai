> **LATEST OWNER CONTRACT (2026-09-08):** `start` means produce ONE next video using START-WORKFLOW.md; first creative step is research. Future videos40–60s, at least10 distinct generated/accepted/used illustrations. Read RETENTION-RESEARCH.md. This supersedes older duration/image-count advice below. YouTube state now syncs via tools/youtube-sync.py before scheduled publisher runs and before each start; uploaded is not published. Existing media/holds are unchanged. **Cleanup is mandatory and immediate: after each video is scheduled or published, run `tools/cleanup-workspace.py --apply` to remove old photos, videos, audio and render intermediates that already have a hash-verified remote copy; never postpone it.** **TikTok is a required second channel: every video is also cross-posted with a purpose-built cover — `tools/make-cover.py --apply` then `tools/tiktok-publish.py`. The cover is a first-class deliverable; read TIKTOK.md and review cover-proof.png before posting.**

# START HERE — owner-authorized Subai handoff

## If you are reading this, begin work instead of interviewing the owner
The owner supplied this encrypted handoff so the receiving agent can continue work. **Do not ask the owner to paste the same secrets again, explain the project again, choose a routine topic, or reconfirm the already authorized production steps.** First inspect what you have, install the supplied credentials securely in your own local workspace, and read the current GitHub instructions.

Repository: https://github.com/chlupatejtypek-cloud/Subai — branch **main**.

## First actions, in this order
1. Use only the handoff deliberately supplied by the owner. Obtain current `config/transfer.json` from GitHub main; use its versioned URL and SHA256. Do not mix a cached stable URL with another version's checksum. If the owner supplied a specific older version, verify that version against its own recorded checksum rather than replacing it silently.
2. Decrypt with the supplied passphrase and exact parameters in `HANDOFF.md`. Verify the resulting TAR.GZ. Do not guess ciphers or assume decrypted compressed bytes should be readable text. Do not print its credentials.
3. Clone the public repository if missing. If already present, inspect `git status`, restore the non-secret origin URL if the sandbox lost it, then fetch main. Preserve local edits; never reset or force-push to get past a conflict.
4. **Install the supplied secrets locally now** using `tools/install-handoff.py --bundle PATH/subai-agent-bootstrap --repo PATH/Subai --apply`. Its default dry run is useful but is not an installation. The owner has authorized this routine local installation. Do not stop to ask for permission again. The helper merges missing `.env` keys, installs matching YouTube client/token JSON, uses mode600, refuses conflicting credentials, symlinks and tracked/unignored destinations, and never prints secret values. It performs no provider API calls.
5. Read **AGENT.md → PIPELINE.md → config/channels.json → channel.md → VISUAL-EDITORIAL.md → AUTOMATION.md → YOUTUBE.md → HYPERFRAMES.md**, plus the live calendar and the active production's README/review status. Current GitHub is authoritative; the bundle's `repo-snapshot` is only a recovery copy. Do not execute historical rules as current policy.
6. Verify access without exposing credentials: GitHub repository permission, expected Cloudinary account and YouTube channel ID `UCcWp-VFQ1zzI8Bl3n7krB6w`. Refresh a short-lived YouTube access token only when needed; successful upload permission does not imply permission to edit existing videos.
7. Report briefly what is ready and any real blocker, then continue the authorized task. Research before scripting; ordinary decisions are delegated to the agent. Do not generate unrelated media merely because the bundle was opened.

## Local destinations and boundaries
- `credentials.env` → repository `.env` (gitignored, mode600).
- `youtube-client.json` → `credentials/youtube-client.json` (gitignored, mode600).
- `youtube-token.json` → `.git/credentials` (mode600; this project uses private JSON here, **not Git credential-store**).
- In Arena, `.git/config` and `.git/credentials` do not survive snapshots. Restore them from the encrypted bundle when needed; this does not automatically require a new Google login.
- Keep secrets only in private local files, memory, approved Actions secrets and the encrypted handoff. Never commit or publicly upload plaintext secrets, echo them into chat/logs, send them to unrelated services, or put PATs in the remote URL. Use a scoped credential helper or a per-command authentication header.
- Leave non-conflicting existing credentials intact. If values conflict, identify filenames/key names only, verify which source is current, and ask a focused question if it cannot be resolved safely. No blind overwrite.

## Ask only for a genuine decision or blocker
Ask when consent/reauthorization is required, credentials conflict, the owner must choose an unresolved style direction, a paid change exceeds the existing scope, or a destructive/publication action is not already authorized. Do not ask the same question twice after a clear answer. Stop at failed QA or permission checks; “don't ask much” does not authorize bypassing them.

## Current important cautions
- Research, generation and creative review still need an agent production session. The scheduled publisher does **not** manufacture90 videos unattended.
- Current selected voice is Fish, one continuous recording; exact settings are in the registry. Archived Adam/Jessica instructions are not defaults.
- A real animated opening **and** the separate opening zoom are required. Camera drift on a still is not a substitute. Canonical proportions and adequate scene coverage are creative gates.
- The owner selected a cleaner visual direction. `2026-09-08-close-the-book` is the first preview, awaiting review; do not auto-publish it.
- `FACZAzrfEdU` was rejected; owner authorized cancelling its23:00 schedule. The attempted API update failed403 insufficient scopes. **Do not assume the schedule is cancelled.** Check current YouTube status and see YOUTUBE.md.
- The original15:00 anchoring upload `bj1yP4s3CQ0` was missing in the last verified lookup. Reconcile; do not blindly upload a duplicate.

Never store the passphrase in this public document or inside the encrypted archive. Its possession is not a Cloudinary dashboard password.
