#!/usr/bin/env python3
"""Read-only KLIPY client for GIF / sticker / clip lookup.

This tool intentionally does NOT download media. KLIPY's Integration Requirements
say media must be loaded directly from the returned URLs and must not be stored,
mirrored or re-hosted without written approval, and that requests should originate
from the end-user client rather than a partner server. Baking KLIPY media into an
exported MP4 that we then re-host on Cloudinary/YouTube/TikTok would breach both.

So this is a discovery tool: it shows what exists so a human can decide, and it
keeps the pipeline honest by not offering a one-command path to a rights problem.
See KLIPY.md for the full reasoning and what to ask KLIPY for.

Reads KLIPY_API_KEY from the environment; the key is never printed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "https://api.klipy.com/api/v1"

# Verified live on 2026-09-08: these respond for our key.
WORKING_TYPES = ("gifs", "stickers", "clips")
# Documented by KLIPY but returns {"result":false,...,"Route not found"} for our
# key — the Meme product is not enabled on this app. See KLIPY.md.
DISABLED_TYPES = ("memes", "meme")

ATTRIBUTION = (
    "KLIPY requires visible attribution wherever this media is shown, media to be "
    "loaded directly from these URLs, and no re-hosting. Do NOT composite these "
    "into a rendered video without written approval from developers@klipy.com."
)


def api_key() -> str:
    key = os.environ.get("KLIPY_API_KEY")
    if not key:
        raise SystemExit(
            "KLIPY_API_KEY is not set. Run: set -a; source .env; set +a"
        )
    return key


# KLIPY rejects the default Python urllib User-Agent with HTTP 403; it expects a
# browser-like agent (their ads documentation says the same). Set one explicitly.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def request(path: str, params: dict) -> dict:
    url = f"{BASE}/{api_key()}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read())
    if not payload.get("result"):
        message = payload.get("errors", {}).get("message", ["unknown error"])
        raise SystemExit(f"KLIPY error: {'; '.join(message)}")
    return payload["data"]


def check_type(media_type: str) -> str:
    if media_type in DISABLED_TYPES:
        raise SystemExit(
            f"The '{media_type}' endpoints are not enabled for this API key "
            "(KLIPY returns 'Route not found', verified 2026-09-08), even though "
            "they are documented.\n"
            "Enable the Meme product for this app in the Partner Panel at "
            "https://partner.klipy.com, or request production access.\n"
            f"Working types for this key: {', '.join(WORKING_TYPES)}."
        )
    if media_type not in WORKING_TYPES:
        raise SystemExit(f"unknown type {media_type!r}; use one of {WORKING_TYPES}")
    return media_type


def show(items: list, limit: int) -> None:
    for item in items[:limit]:
        files = item.get("file", {})
        best = files.get("md") or files.get("hd") or {}
        print(f"\n{item.get('title', '(untitled)')}")
        print(f"  slug   : {item.get('slug', '-')}")
        tags = item.get("tags") or []
        if tags:
            print(f"  tags   : {', '.join(str(t) for t in tags[:8])}")
        for fmt in ("gif", "mp4"):
            if fmt in best:
                print(f"  {fmt:6} : {best[fmt]['url']}")
    print(f"\n{len(items[:limit])} result(s).")
    print(f"\nNOTE: {ATTRIBUTION}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="search by keyword")
    search.add_argument("query")
    search.add_argument("--type", default="gifs")
    search.add_argument("--limit", type=int, default=5)

    trending = sub.add_parser("trending", help="current trending items")
    trending.add_argument("--type", default="gifs")
    trending.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()
    media_type = check_type(args.type)
    # customer_id is expected by KLIPY for personalisation and ad attribution.
    params = {"per_page": args.limit, "customer_id": "subai-agent"}

    if args.command == "search":
        params["q"] = args.query
        data = request(f"{media_type}/search", params)
    else:
        data = request(f"{media_type}/trending", params)

    show(data.get("data", []), args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
