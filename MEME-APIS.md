# Meme / GIF APIs — KLIPY and GIPHY

The owner wants memes usable in videos as a **short humorous beat** — one meme as a
release after a reveal, consistent with the existing humour rule (some videos should
have no joke at all). Two API keys have been supplied:

| Provider | Key in `.env` | Status |
| --- | --- | --- |
| KLIPY | `KLIPY_API_KEY` | Works for gifs/stickers/clips; **meme endpoints not enabled** |
| GIPHY | `GIPHY_API_KEY` | Works for gifs/stickers |

Both keys live only in the gitignored root `.env`. They are never committed, never
printed, and never passed on a command line.

## The bottom line

**Neither provider currently permits what our pipeline would do with the media**, and
GIPHY is the stricter of the two. This is a licensing problem, not a technical one —
both APIs work fine. Details below, then what to do about it.

---

## GIPHY

Verified live on 2026-09-08: `gifs/search`, `gifs/trending` and the sticker
equivalents all return HTTP 200 with this key.

### Why it cannot go into a rendered video

Quoting GIPHY's own terms:

- **User ToS §5 (Proprietary Rights):** *"you shall not copy, modify, publish,
  transmit, distribute, perform, or display any content, nor shall you sell,
  license, rent, or otherwise use or exploit any content for commercial use"*.
  GIPHY's own plain-English summary of that clause: content may be used *"solely for
  personal and non-commercial purposes."*
- **API Terms §1 (License; Restrictions):** the API is licensed *"solely to allow
  for the creation of software applications that interface with Giphy's products and
  services"*. An exported MP4, re-hosted on Cloudinary and published to YouTube and
  TikTok, is not an application interfacing with GIPHY.
- **API Terms §4 (Trademarks):** any application must be *"conspicuously label[led]
  … with the words 'Powered by Giphy,' and the Giphy logo"*.
- **API Terms §5 (Attribution):** *"you won't display any content in your
  applications without Giphy user and/or source attribution where available."*

A monetisable psychology short is commercial use, so §5 of the User ToS rules it out
on its own — before we even reach the trademark and attribution obligations, which
are awkward to satisfy inside a burned-in video where nothing is clickable.

## KLIPY

Verified live on 2026-09-08:

| Endpoint | Result |
| --- | --- |
| `gifs/search`, `gifs/trending` | Works |
| `stickers/search` | Works |
| `clips/search` | Works |
| `memes/search`, `memes/trending`, `meme/*` | `{"result":false,...,"Route not found"}` |

The meme endpoints specifically are **not enabled for this key**, though KLIPY
documents them. The key is otherwise valid, so this is an entitlement issue: enable
the Meme product for the app in the Partner Panel (https://partner.klipy.com), or
request production access. The key is also presumably still in Testing mode, which
KLIPY caps at **100 requests per hour**.

Note: KLIPY rejects the default Python `urllib` User-Agent with HTTP 403. A
browser-like agent is required; `tools/klipy.py` sets one.

### Why it cannot go into a rendered video either

KLIPY's Integration Requirements:

1. **"Load KLIPY media directly"** — *"Do not store, mirror, re-host, rewrite, or
   retain copies of KLIPY media unless KLIPY has approved a different delivery
   method in writing."*
2. **"Send requests from the end-user client"** — *"Do not route requests through
   partner-operated servers, proxies, CDNs, or other intermediaries without prior
   written approval."*
3. Preserve KLIPY URLs and tracking/attribution parameters.
4. Display KLIPY branding in the interface.

Our pipeline downloads media server-side and bakes it into a redistributed MP4,
which is exactly what (1) and (2) reserve for written approval.

KLIPY is the more promising of the two, because its terms *invite* the conversation
("contact us for prior approval and implementation guidance") rather than flatly
restricting content to non-commercial use.

## The separate, provider-independent problem: rights

Being able to fetch a meme through an API is not the same as holding the rights to
embed it in monetisable content. Popular memes are overwhelmingly screenshots from
films, TV and photographs owned by third parties, uploaded to these platforms by
users who often did not own them. Our standing rule is that every asset has a
recorded provider, rights basis and source ID. A GIF of unclear provenance cannot
satisfy that, regardless of which API served it.

## Recommendation

**Do not composite KLIPY or GIPHY media into any published video** until both of
these are settled:

1. Written approval from the provider for the actual use — server-side fetch, media
   composited into an exported short-form video, redistributed on YouTube and
   TikTok — including the attribution format they require. Start with KLIPY
   (developers@klipy.com); GIPHY would additionally need a commercial-use
   arrangement that their standard terms do not grant.
2. A defensible rights basis for the specific items, or a restriction to items the
   provider confirms are cleared for commercial reuse.

Meanwhile both APIs are genuinely useful for something that avoids both problems
entirely, and that fits the channel better anyway:

> **Inspiration only.** Browse what visual joke format is current for a topic, then
> express the same idea as an original Stiles illustration.

This keeps the channel's visual identity consistent — which the owner has repeatedly
asked for — and means the humour beat can ship now, without a licensing dependency.

## Tools

Both clients are read-only and **neither downloads anything**. Downloading is the
precise step the terms restrict, so the tools do not make it easy to do by accident;
a unit test enforces this.

```
set -a; source .env; set +a

python tools/klipy.py search "nervous before a call" --type gifs --limit 5
python tools/klipy.py trending --type clips

python tools/giphy.py search "reading a bad review" --limit 5 --rating pg
python tools/giphy.py trending --rating g
```

- `tools/klipy.py` refuses `--type memes` with a clear explanation rather than
  surfacing a bare "Route not found".
- `tools/giphy.py` prints the per-item user/source attribution GIPHY requires, and
  defaults to the `pg` content rating.
- Both print the provider's attribution and usage warning with every result set.
