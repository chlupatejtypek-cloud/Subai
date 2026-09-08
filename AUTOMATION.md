# Automation — current,2026-09-08

## Runs without chat
- publish-calendar.yml: GitHub cron at minutes17/47 each hour, plus manual dispatch. GitHub may delay jobs. Only `ready` items30minutes–48hours ahead may upload; YouTube's future publishAt performs release timing.
- Before uploading: validate registry/channel, evidence/QA, approved Cloudinary URL, SHA256, actual dimensions/fps/audio/duration; refresh OAuth and verify channel identity.
- Commit/push `upload_started` BEFORE upload. Ambiguous completion becomes `needs_reconciliation`; no blind retry. Capture the returned video ID and verify schedule instead of assuming success.
- refresh-handoff.yml: relevant main changes, manual dispatch and daily04:13UTC. It preserves supplied credentials, merges runtime secrets, encrypts current instructions/config/calendar and uploads ciphertext only.
- Both workflows share one concurrency group. Fetch state commits before pushing; no force pushes. A workflow's GITHUB_TOKEN push does not trigger another workflow, so explicit/daily handoff refresh captures publisher state.

## Does NOT run autonomously
Research, scriptwriting, hosted image generation, assembly decisions and semantic/creative review still require an agent session. `unattended_generation=false`. The90-slot calendar is not90 completed videos. No scheduling analytics/viral guarantee or automatic semantic-topic deduplication is implemented.

## State and gates
Typical sequence: planned → researching → scripted → producing → ready → upload_started → scheduled. Public status requires an actual API check; clock passage alone is not proof. Blocked/missed/needs_reconciliation states require investigation. A scheduled item may additionally have owner rejection or a cancellation blocker; its remote publishAt is not removed by a local status change.

Before ready, provide title≤60chars, accurate description, at least2 recorded HTTPS sources including primary evidence, verified final URL/SHA256/duration and QA provenance. Existing REQUIRED_QA includes research/script, voice/character, fullbleed, caption alignment/no-overlap, audio/visual review and rights. Actual code is tools/youtube-publish.py.

**Release contract v2 for future ready items:** qa.creative_contract_version=2; true opening_video_verified, opening_zoom_verified, character_proportions_verified and visual_coverage_verified; record longest_illustration_hold_seconds and, if over7s, a content-specific long_hold_justification. These are review attestations supported by artifacts, not automatically inferred facts. Rejected or explicitly held items fail validation regardless of old flags. If owner_review_required=true, owner_review.status must be approved. Existing uploaded/published items are not retroactively reuploaded or certified against v2.

## Safe commands
```sh
python -m unittest discover -s tests -v
python tools/calendar-report.py
python tools/youtube-publish.py                 # dry run
python tools/youtube-publish.py --verify-auth   # identity check, no upload
```
Actual execution normally belongs to the serialized workflow. Do not run competing local publishers. Immediate publication needs a specific owner override; automatic calendar authorization is not permission to backdate or burst-fill missed slots.

## Known boundaries
YouTube upload+readonly scopes work for uploads/read checks, but existing-video status edits failed403 insufficient scopes. Owner-authorized cancellation therefore needs Studio or Google reauthorization; do not repeat the same failed update. Consent-screen Testing/Production mode and formal project audit status are not inferred. Public phone upload was verified, which supersedes older “no public test yet” notes, but does not prove indefinite token validity.

See PIPELINE.md for current unresolved releases and the full audit, YOUTUBE.md for account permissions, HANDOFF.md for restoring credentials. Secrets stay out of public Git, including upload session URLs and auth codes.
