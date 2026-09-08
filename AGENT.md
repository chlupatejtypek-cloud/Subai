> **LATEST OWNER CONTRACT (2026-09-08):** `start` means produce ONE next video using START-WORKFLOW.md; first creative step is research. Future videos40–60s, at least10 distinct generated/accepted/used illustrations. Read RETENTION-RESEARCH.md. This supersedes older duration/image-count advice below. YouTube state now syncs via tools/youtube-sync.py before scheduled publisher runs and before each start; uploaded is not published. Existing media/holds are unchanged. **Cleanup is mandatory and immediate: after each video is scheduled or published, run `tools/cleanup-workspace.py --apply` to remove old photos, videos, audio and render intermediates that already have a hash-verified remote copy; never postpone it.**

# Agent operating contract — current,2026-09-08

## Begin, do not repeatedly ask for setup
Read START_HERE.md and install the credentials deliberately supplied in the owner's encrypted handoff. This is authorized local setup, not a reason to request the same keys again. Existing valid private local credentials also count; credentials need not have been pasted into this particular chat turn. Never search unrelated accounts/files for credentials.

Then read PIPELINE.md, registry, channel specification, latest editorial corrections, automation, YouTube and active production records. Fetch current main and preserve unrelated local changes. Verify actual permissions before claiming access.

## Authority and sources of truth
1. Current system/platform constraints and the owner's latest explicit request.
2. Current operating docs and registry on main. Latest editorial corrections supersede older advice; historic render sources stay reproducible.
3. Live provider state for factual availability/publication; calendar is a ledger, not proof that a video still exists.
4. Decrypted repo snapshot is fallback context, not authority over newer main.

Routine research, topic choice, scripting, single Fish synthesis, visuals, rendering, QA and publication of genuinely ready calendar items were delegated. Ask only for unresolved material decisions, scope/cost expansion, conflicting secrets or required external consent. Do not improvise away hard creative requirements to hit a slot.

## Secrets and Git
`.env` and `credentials/` must be gitignored; use mode600, private directories, no plaintext logs. `.git/credentials` is this project's YouTube token JSON, NOT Git credential-store. Both it and `.git/config` may disappear across Arena snapshots; restore from the verified bundle rather than demanding new authorization automatically.

Non-secret origin: https://github.com/chlupatejtypek-cloud/Subai.git . Use the supplied PAT via a private credential helper or per-command header; never embed it in the remote URL. Verify the repository write permission, fetch before pushing and stage only intended changes. Do not force-push, sweep unrelated files into a commit, or expose short-lived auth codes/resumable-upload URLs.

Do not move secrets into a private Git repository either; GitHub Actions secrets and the owner's encrypted handoff are the designated durable stores. Do not print decrypted credentials in chat to prove they work.

## Critical creative gates
Actual animated hook AND separate100→105→100% opening zoom; no still-only provider-failure substitute. Canonical Stiles proportions, context-appropriate expressions, enough distinct relevant imagery and justified hold durations. Micro-drift supplements variety. Latest cleaner-style preview needs owner review before release. A successful render or ASR match does not prove creative quality.

## Honest reporting
Distinguish planned, generated, technically checked, creatively approved, uploaded, processed, scheduled and public. A local hold does not cancel an existing YouTube schedule. HTTP403 insufficient scopes requires consent or Studio action, not repeated requests with the same token. Never claim cancellation, restored credentials, uploaded files or autonomous generation without evidence.

## Current production constraints
Use channel.md and VISUAL-EDITORIAL.md; do not restore historical ElevenLabs/Jessica/40s/fixed10+5 defaults. Existing published or scheduled videos are not silently replaced. Owner-rejected media cannot be automatically republished, even if stale QA flags were accidentally set true.
