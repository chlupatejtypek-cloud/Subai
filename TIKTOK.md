# TikTok publishing and covers

Second distribution channel for Stiles Psychology. The videos are already
1080x1920 / 30fps with burned-in word captions, so the master needs no re-render
for TikTok — but **every TikTok post must ship with a purpose-built cover**, and
the cover has to be designed against constraints that are different from
YouTube's.

---

## 1. Why the cover matters here, and where it is actually seen

TikTok is not YouTube. In the For You feed the video autoplays, so the cover is
not the click trigger there. The cover decides taps in the three places that
build a channel rather than a single view:

- the **profile grid** — the deciding surface for "should I follow this account",
  where nine covers are judged at once;
- **search results** — increasingly how evergreen explainer content is found;
- **external embeds and shares**.

So the cover is a *catalogue* asset. Consistency across covers matters as much
as any single cover's cleverness.

## 2. The hard layout constraints

| Zone | Size | Rule |
| --- | --- | --- |
| Canvas | 1080 x 1920, 9:16, sRGB | Match the video exactly. |
| Grid-safe square | centre 1080 x 1080 | Only region visible in **both** the full cover and the grid crop. Focal point and headline go here. |
| Auto-title gutter | bottom ~270 px | TikTok overprints the first caption line in white. Anything here is destroyed. |
| Status gutter | top ~220 px | Status bar and account chrome. Keep clear. |
| Legibility target | 200 x 350 px | The profile-grid render size. If it fails here, it fails. |
| Format | PNG for text-heavy covers, JPG for photographic | PNG keeps our type crisp. Under 5 MB. |

Sources: TikTok cover-spec guides on the grid crop and auto-title overlay
(socialrails.com/sizes/tiktok/thumbnail, moda.app/resources/sizes/tiktok-thumbnail),
plus adcreate.com's cross-platform thumbnail breakdown on text placement.
These are industry guides, not TikTok's own published spec — treat the pixel
numbers as well-corroborated conventions, and the CTR percentages that float
around such articles as unverified marketing claims we do not repeat.

## 3. What makes a cover interesting rather than merely correct

Four traits recur across every serious source, and all four are things we can
control:

1. **One focal point**, recognisable at 200 x 350. For us that is Stiles with a
   scene-appropriate expression, or the single prop the video is about.
2. **A short headline, 3-5 words**, set very large. It states the *promise*, not
   the topic. "Say it out loud" beats "Affect labeling research".
3. **Strong contrast.** Cream type on a dark bed, ochre accent. Never light type
   floating on a light illustration.
4. **A human face or character with clear emotion.** We have this built in;
   choose the frame where Stiles is actually reacting, not standing neutrally.

House rules on top of that, specific to this channel:

- **Curiosity gap, honestly.** The cover may withhold the answer; it must never
  imply a claim the video does not support. No invented numbers on covers ever.
- **The kicker carries the setup, the headline carries the payoff-tease.**
  Example: kicker "The spider test, one week later" / headline "SAY IT OUT LOUD".
- **Same type, same palette, same wordmark position on every cover.** The grid
  should read as one publication. Anton for the headline, DejaVu Bold for the
  kicker, warm green/ochre/cream Stiles palette.
- **No clutter.** One rule, one kicker, one headline, one wordmark. Nothing else.
- Do not reuse a blurry mid-motion frame. Pick a still, well-composed beat.

## 4. Making a cover

```
python tools/make-cover.py PRODUCTION_DIR \
    --from-video final.mp4 --ss 18 \
    --headline "Say it out loud" \
    --sub "The spider test, one week later"
```

`--image path.png` uses a production illustration instead of a video frame.
Without `--apply` the tool writes `cover-preview.png` only; with `--apply` it
writes `cover.png`, `cover-proof.png` and `cover.json`.

The tool enforces the constraints above and **exits non-zero on failure**:

- `dimensions` — exactly 1080 x 1920.
- `headline_size` — at least 96 px; the layout starts at 175 px and shrinks only
  as far as it must. If a headline cannot be set at 96 px in two lines, the tool
  refuses: the headline is too long, shorten it.
- `headline_inside_grid_crop` — the headline band lies inside the centre square,
  so it is not decapitated on the profile grid.
- `title_gutter_quiet` — the bottom 270 px carry no busy detail.
- `legible_at_200x350` — luma spread measured after downscaling to grid size.
- `headline_contrast` — at least 4.5:1 between the type and the darkest decile
  of its own bed.

**Always look at `cover-proof.png` before approving.** It renders the full cover,
the profile-grid crop and the 200 x 350 test side by side, with the auto-title
gutter outlined. Automated checks catch geometry and contrast; only the proof
sheet catches "the headline sits on top of Stiles' face".

## 5. Publishing

```
set -a; source .env; set +a
python tools/tiktok-publish.py --production DIR            # dry run
python tools/tiktok-publish.py --production DIR --execute
```

The publisher uses TikTok's Content Posting API v2 at `open.tiktokapis.com`:

1. `POST /v2/post/publish/creator_info/query/` — required first. It returns the
   privacy levels this creator actually allows; sending a level not in that list
   fails the post.
2. `POST /v2/post/publish/video/init/` with `PULL_FROM_URL` pointing at the
   Cloudinary master, plus `post_info`.
3. Poll `POST /v2/post/publish/status/fetch/` until `PUBLISH_COMPLETE`.

### The cover caveat — read this before assuming covers are automatic

The v2 Direct Post API **does not accept a custom cover image**. It exposes only
`video_cover_timestamp_ms`, a frame offset. Posting an external cover URL to it
returns a 400 invalid-cover-asset error; the `video_cover_image_url` field seen
in some third-party docs belongs to those *aggregators*, not to TikTok's own API.

Two consequences, and we use both:

- **Automated path.** The publisher renders the designed cover, then requires
  that the same designed frame exists inside the video, and points
  `video_cover_timestamp_ms` at it. The build must therefore hold a clean,
  cover-worthy beat; `--cover-ms` records which one.
- **Best-reach path (preferred while the account is small).** Post with
  `post_mode = MEDIA_UPLOAD` so the video lands in the TikTok inbox as a draft,
  then finish it in the app: attach the designed `cover.png` as the custom cover
  and add trending audio. Drafts finished natively generally reach further than
  fully automated direct posts. This is a manual step and the workflow says so
  rather than pretending it is automated.

### Other API facts that bite

- Scope `video.publish` is needed for direct posting; `video.upload` only
  produces drafts.
- The app must pass TikTok's audit before posts can be public. Before audit,
  posts are forced to `SELF_ONLY`.
- Third-party API posting has its own daily rate limit, separate from the app.
- `is_aigc` must be set true. Our illustrations and narration are AI-generated,
  so the disclosure is not optional.
- Caption max 2,200 characters. TikTok ignores line breaks.
- The **first line of the caption is what gets printed over the cover's bottom
  gutter** — write it as a real line, not a hashtag dump.

## 6. Credentials

Not yet configured. Required, as GitHub Actions secrets and in the encrypted
handoff bundle, same pattern as YouTube:

```
TIKTOK_CLIENT_KEY
TIKTOK_CLIENT_SECRET
TIKTOK_REFRESH_TOKEN
```

Until these exist, `tools/tiktok-publish.py` runs in dry-run only and prints the
exact payload it would send. Nothing is posted.

## 7. Cross-posting policy

- The YouTube upload remains the primary. TikTok posts the same master.
- Never delete or alter an existing YouTube video to accommodate TikTok.
- Cleanup rules are unchanged: `cover.png` is a media file and is removed by
  `tools/cleanup-workspace.py` once it is backed up and hash-verified, exactly
  like every other rendered asset. `cover.json` stays, so the cover is
  reproducible.
