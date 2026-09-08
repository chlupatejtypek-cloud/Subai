> **LATEST MOTION FEEDBACK:** Liking-gap preview approved. Future UI text/panels must animate smoothly (reveal, slide, fade, state transition), never suddenly spawn. Occasional selective blur remains welcome, never constant; use an animated circle only when useful, optional not mandatory. Remember prior constraints:40–60s,10illustrations, meaningful backgrounds, balanced Stiles, real hook + separate zoom.

# `start` — one next video, step by step

Latest owner contract,2026-09-08. When the owner writes `start` (case-insensitive), the receiving agent executes this workflow immediately. Do not ask for a topic, repeated keys or routine permission. This is an agent instruction plus executable state helpers, NOT a deployed chat listener or an unattended generative service. Merely discussing the word `start` does not trigger paid generation.

## Operational preflight (not the creative research step)
Read current main and START_HERE; restore supplied local credentials if needed. Fetch before changes; preserve unrelated work. Run `python tools/youtube-sync.py --apply`, then `python tools/start-next.py --apply`. Commit/push the calendar reservation before spending on generation. If push conflicts, re-fetch and resolve selection before proceeding; never force-push or run concurrent productions. `--commit-state` can commit/push when working-tree/auth conditions are safe. Run only one production agent at a time; shared Actions lock protects publisher/handoff jobs, not arbitrary local agents.

Sync requires verified YouTube identity and successful API reads; failure leaves the calendar unchanged. Selector requires sync under10minutes old. It resumes a single unfinished researching/scripted/producing item, otherwise reserves earliest future planned item with no existing production directory/final asset or YouTube ID (a planned path alone is only a placeholder). Completed ready, scheduled, public, private-uploaded, held and reconciliation items are NOT new work. Multiple unfinished items require reconciliation, not a duplicate. Semantic topic checks include all productions, including unslotted previews. A proposed topic may be improved before script; preserve slot ID and record any changed topic/angle. Do not move existing uploaded media or fill missed slots by bursting uploads.

**Do not stop after the helper prints an ID. Begin step1 and continue through the steps in the same agent session as capabilities permit.** Record a real blocker or checkpoint if interrupted; do not claim production completed from reservation alone.

## 1. Research — before writing the script
Read RETENTION-RESEARCH.md. Consider3 genuinely different angles for the selected subject, comparing all calendar/production topics semantically. For each, note: relatable situation, surprising but supported finding, specific unanswered question, practical payoff, potential visual demonstration, evidence strength. An internal0–2 score on each dimension helps choose; it is an editorial rubric, not a validated virality predictor. Reject unsupported/generic/repeated angles even if the hook sounds good.

Read at least one primary study and corroborating material (prefer independent research/review). Record exact claim, measured outcome, population, design, limitations, source URL and what the video may NOT claim. Distinguish a press release about the same study from independent replication. If only an abstract is accessible, label it, narrow claims or choose better-supported evidence. Investigate counterevidence; never invent statistics. Deliver `research.md` with angle comparison, claim-evidence table, practical advice vs tested result, and one-sentence viewer promise. Exit: credible, useful, non-obvious angle with enough substance for40–60s; otherwise research a better angle.

## 2. Story architecture and script
Write3 opening candidates internally; select the clearest specific puzzle whose answer is actually delivered. No greeting, channel introduction or generic “Did you know?” padding. Write a beat table: time target / viewer question / new information / visual / source or illustration label / payoff. Each beat must move understanding forward, not merely repeat a tease.

A flexible50s scaffold (editorial hypothesis, not a scientifically optimal formula):0–3s concrete hook;3–10s relatable stakes and first answer;10–20s evidence/demo with useful animated UI;20–30s explanation and optional brief joke;30–42s practical example/contrast;42–50s useful closure. Adjust within40–60s, use at least10illustrations, aim2.5–5s holds, never pad a still. Include meaningful scene backgrounds and explanatory UI, not headings alone. Close the central question and avoid unrelated simultaneous events.

Start around140–175 English words as a rough drafting budget; actual recorded/edited runtime controls. One continuous flowing Fish narration. Read aloud for breath, repetition and clunky transitions. Shorten confusing sentences; add useful examples rather than padding to40s. Exit: `narration.txt`, `story-beats.md`, claim audit and hook/payoff check.

## 3. Optional humor pass
Consider one short dry observation, situational irony or Stiles reaction that reinforces the explanation. Some videos should have no joke. No compulsory punchline, canned meme, laugh track, insulting the viewer or mocking mental illness. If removing the joke makes the explanation clearer or it needs explaining, cut it. Example of tone, not a reusable line: “Apparently my brain hired a lawyer, not a fact-checker.” Use only for a genuinely relevant, accurately explained mechanism. Humor should be a brief release after a useful reveal, not a detour before the opening promise.

## 4. Storyboard and visual plan
Plan10–15 distinct generated illustrations that are accepted AND used in the final video. Ten generation attempts, crops or near-identical drifted remakes do not satisfy the minimum. Keep cleaner cream/teal/ochre Stiles, canonical proportions and scene-specific expressions. Mix clear scenes with concise helpful UI. Time meaningful changes against narration; no mandatory frantic cut frequency. Actual animated opening plus separate opening zoom remains required. Record planned/generated/accepted/used counts and longest source hold, with justification above7s.

## 5. Voice and assets
Synthesize finalized script once as one continuous Fish recording; preserve native alignment. Existing restrained pause edits and1.06 pitch-preserving tempo remain; do not speed it twice. Generate/review illustrations and real opening motion with bounded corrective retries. No substitution of a static hook after provider failure. Record provider/rights/source IDs. If natural final duration falls outside40–60s, revise substantive script/timing rather than stretch silence or rush unintelligibly.

## 6. Assembly
1080×1920,30fps; actual hook motion AND opening zoom; minimal movement on stills; canonical stationary word captions; meaningful quiet SFX, no music bed. One focal idea at a time. Render the exact final and preserve timeline/edit sources.

## 7. QA and release decision
Check actual40–60s runtime, at least10 distinct used illustrations, voice identity, ASR/caption completeness and timing, audio levels, full bleed, real hook/zoom, proportions, visual coverage, rights and research claim fidelity. Watch/listen when available; report accurately which checks were automated vs human/agent review. Review every beat for “what new value arrives here?” and verify hook promise is paid off. Never manufacture QA attestations.

Populate creative contract v2 plus existing QA. `qa.source_image_count` means distinct accepted illustrations actually used. Record generated count separately. Existing-video ID always blocks another upload. Carry required owner review/rejection/holds into calendar, not only chat. Cleaner style preview still awaits approval; this workflow change does not approve it. For a completed but held new video, use status `preview_pending_owner_review`, publication_hold=true and owner_review_required=true. Routine approved-style work need not seek a new topic/script approval.

## 8. Backup and calendar handoff
Upload/verify final hash; backup editable sources and verify download/restore before cleanup. Store final URL, SHA256, duration, production path, QA and review status. Only fully cleared work becomes `ready`. Videos may be generated weeks ahead and remain `ready` until the publisher's30min–48h window. Do not regenerate them on the next `start`. Commit each major stage's artifact paths and `workflow.stage/next_action` so interruptions resume from real outputs.

## 8b. Mandatory cleanup after every finished video

**Standing owner instruction (2026-09-08): clean up immediately after a video is finished and scheduled/published — not "later", not "when the disk fills up".** Old photos, videos, audio and render intermediates must not accumulate in the workspace.

Run it as the step right after the publisher reports `scheduled` or `published`:

```
set -a; source .env; set +a
python tools/cleanup-workspace.py            # dry run, shows exactly what goes
python tools/cleanup-workspace.py --apply
```

What the tool guarantees, and what you must not bypass:
- Deletes a media file only after re-downloading its recorded Cloudinary copy and matching SHA256 three ways (local, remote, manifest), or after matching its hash inside a cold archive whose `restore-verification.json` confirms every member was verified.
- Cleans only media: rendered masters, generated stills, source/derived audio, QC contact sheets and `output/` intermediates. Scripts, research, provenance JSON and QA records always stay, so any production remains reproducible.
- Skips a production entirely while its calendar item is still in progress, so the video being built now keeps its inputs.
- Prints `KEEP` for anything without a verified remote copy. That is a to-do, not a pass: upload it, record it in the production's `assets.json`, verify the hash, then clean.

Never delete media by hand instead of running this, and never weaken the hash checks to reclaim space faster. Restore anything later from the URLs in `assets.json`.

## 8c. TikTok cover and cross-post

**Standing owner instruction (2026-09-08): every video also goes to TikTok, and the cover is a first-class deliverable, not an afterthought.** Read TIKTOK.md before making one.

```
python tools/make-cover.py PRODUCTION_DIR --from-video FINAL.mp4 --ss 18 \
    --headline "Say it out loud" --sub "The spider test, one week later"   # preview
python tools/make-cover.py ... --apply                                     # cover.png + cover.json
python tools/tiktok-publish.py --production PRODUCTION_DIR                 # dry run
```

Non-negotiable design rules, all enforced by the tool, which exits non-zero on failure:
- 1080x1920 sRGB, everything meaningful inside the **centre 1080x1080 grid-safe square** — that is the only region visible in both the full cover and the profile-grid crop.
- The **bottom 270 px stays empty and quiet**: TikTok overprints the caption's first line there in white.
- Headline **3–5 words**, at least 96 px, stating the promise not the topic; kicker carries the setup. No numbers or claims the video does not support.
- Cream type on a dark bed, ochre accent, Stiles palette, wordmark in the same place every time. The profile grid must read as one publication.
- Pick a frame where Stiles is actually reacting, never a motion-blurred one.

**Always open `cover-proof.png` and look at it.** It shows the full cover, the grid crop and the 200x350 legibility test with the caption gutter marked. The automated checks catch geometry and contrast; only your eyes catch a headline sitting on Stiles' face.

The TikTok v2 API cannot accept a custom cover image — only a frame timestamp. So either point `--cover-ms` at a genuinely cover-worthy frame, or use `--draft` to send the video to the TikTok inbox and attach `cover.png` by hand in the app (preferred while the account is small; see TIKTOK.md section 5).

## 9. Upload and actual publication sync
Serialized Actions uploads only eligible ready items; state reservation before upload prevents blind retries. `scheduled` means private with future publishAt, NOT public. The same workflow now runs youtube-sync before publication on cron17/47 and execute; it updates known IDs from YouTube and commits the result. Each `start` also syncs. Public+processed becomes `published`; `first_observed_public_at` is observation time, not claimed exact release time. Missing/failed IDs become needs_reconciliation; retain IDs and never auto-reupload. Private without schedule becomes uploaded_private, not an assertion who cancelled it. Owner-held media still scheduled/public gets an alert, not a false cancellation.

## 10. Learn from results
At roughly24h,72h and7days after public release, review available engaged views, stayed-to-watch, average view duration/percentage, retention drops/replays, shares and meaningful comments. Compare similar-length/channel videos and sample sizes, not invented universal viral thresholds. Record one concrete hypothesis/change for the next production in `performance-notes.md`. Retention Analytics API integration is NOT implemented/authorized by readonly Data API credentials; use supplied Studio exports or request appropriate access only if necessary. Do not block ordinary production on unavailable analytics or invent metrics.

## Completion response
Briefly give: selected topic, completed stage, final preview link if available, duration/used-image count, QA/review state, calendar ID/slot, whether ready/scheduled/public, the TikTok cover headline plus whether all its checks passed and whether the TikTok post is direct/draft/pending credentials, and confirmation that cleanup-workspace.py was applied with how much space it reclaimed. State actual blockers. One `start` produces/resumes one video, never the whole90-slot calendar in one hidden batch.
