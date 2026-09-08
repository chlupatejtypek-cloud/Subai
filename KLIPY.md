# KLIPY — meme / GIF / clip API

Owner supplied a KLIPY API key on 2026-09-08 and asked for memes to be usable in
videos, as a **short humorous beat** — one meme as a release after a reveal, in
keeping with the existing humour rule (some videos should have no joke at all).

The key is stored in the gitignored root `.env` as `KLIPY_API_KEY`. It is never
committed, never printed, and never passed on a command line.

## What KLIPY is

An expression-media platform and API for GIFs, stickers, clips, memes and AI
emojis — the same product category as GIPHY and Tenor, and currently being adopted
as a Tenor replacement because Tenor's third-party API is being sunset. Base URL
`https://api.klipy.com`, key in the path:

```
GET https://api.klipy.com/api/v1/{APP_KEY}/{type}/search?q=&page=&per_page=&customer_id=
GET https://api.klipy.com/api/v1/{APP_KEY}/{type}/trending?...
```

Media URLs come back under `file`, in four sizes (`hd`, `md`, `sm`, `xs`), each with
`gif`, `webp`, `jpg`, `mp4` and `webm` variants.

## Verified against the live API on 2026-09-08

| Endpoint | Result |
| --- | --- |
| `gifs/search`, `gifs/trending` | **Works** |
| `stickers/search` | **Works** |
| `clips/search` | **Works** |
| `memes/search`, `memes/trending`, `meme/*` | **`{"result":false,"errors":{"message":["Route not found"]}}`** |

So the **meme endpoints specifically are not enabled for this key**, even though
KLIPY documents them. Everything else responds normally, which means the key itself
is valid and this is an entitlement/plan issue rather than a bad key. To fix it,
check the Partner Panel at https://partner.klipy.com — the app may need the Meme
product enabled, or production access requested.

Also note the key is presumably still in **Testing mode**, which KLIPY limits to
**100 API requests per hour** until production access is granted.

## The blocking problem: KLIPY's integration terms conflict with how we make videos

This is the important part, and it is why nothing has been wired into the render
pipeline yet. KLIPY's Integration Requirements state, in their own words:

1. **"Load KLIPY media directly"** — media must be loaded from the returned URLs.
   *"Do not store, mirror, re-host, rewrite, or retain copies of KLIPY media unless
   KLIPY has approved a different delivery method in writing."*
2. **"Send requests from the end-user client"** — requests and media loads must come
   from the user's app or browser. *"Do not route requests through partner-operated
   servers, proxies, CDNs, or other intermediaries without prior written approval."*
3. **Preserve KLIPY URLs and delivery data** — do not strip tracking/attribution
   parameters.
4. **Attribution** — KLIPY branding must appear in the interface.

Our pipeline does the opposite of 1 and 2 by design: an agent on a server downloads
media, **bakes it into an exported MP4**, uploads that MP4 to Cloudinary, and
publishes it to YouTube and TikTok. That is server-side fetching plus permanent
re-hosting of a derivative — precisely what requires prior written approval. The
attribution requirement is also awkward in a burned-in video, where there is no
interface to place branding in and the viewer cannot click through.

There is a further, independent problem: **licensing for commercial republication.**
Being able to fetch a meme through an API is not the same as holding the rights to
embed it in monetisable YouTube/TikTok content. Popular memes are typically
screenshots from films, TV and photographs owned by third parties. Our existing rule
is that every asset has a recorded provider, rights and source ID.

## Recommendation

Do not put KLIPY media into rendered videos until **both** of these are resolved:

1. Email developers@klipy.com describing the actual use — server-side fetch, media
   composited into an exported short-form video, redistributed on YouTube and TikTok
   — and get written approval plus the attribution format they want. Their terms
   explicitly invite this ("contact us for prior approval and implementation
   guidance"), so it is a normal request, not a loophole.
2. Confirm the rights position for commercial reuse of specific memes, or restrict
   usage to items KLIPY can confirm are cleared for that.

Meanwhile the API is genuinely useful for things that do **not** involve baking media
into a published video:

- **Research/inspiration only**, offline: browsing what visual joke format is current
  for a topic, then having our own Stiles illustration express the same idea. This
  keeps the channel's visual identity consistent, which the owner has repeatedly
  asked for, and sidesteps both problems entirely.
- A future interactive surface (a picker in a web tool) where the KLIPY terms are
  straightforwardly satisfiable, because media loads client-side from their URLs.

## Tool

`tools/klipy.py` is a thin, read-only client.

```
python tools/klipy.py search "nervous before a call" --type gifs --limit 5
python tools/klipy.py trending --type gifs
```

Deliberate design decisions:

- It **prints URLs and titles only. It does not download anything.** Downloading is
  the exact step the terms restrict, so the tool does not make it easy to do by
  accident.
- It refuses `--type memes` with a clear explanation that the endpoint is not
  enabled for this key, instead of surfacing a bare "Route not found".
- It requires `customer_id`, which KLIPY expects for personalisation and ad
  attribution, and never strips URL parameters.
- It prints the attribution reminder with every result set.
