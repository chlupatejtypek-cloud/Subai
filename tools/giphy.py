#!/usr/bin/env python3
"""Read-only GIPHY client for GIF / sticker lookup.

Like tools/klipy.py, this tool deliberately does NOT download media, because
GIPHY's terms do not permit what our render pipeline would do with it:

  User ToS section 5: "you shall not copy, modify, publish, transmit, distribute,
  perform, or display any content, nor shall you sell, license, rent, or otherwise
  use or exploit any content for commercial use". GIPHY's own plain-English gloss:
  content may be used "solely for personal and non-commercial purposes."

  API Terms section 1: the API is licensed "solely to allow for the creation of
  software applications that interface with Giphy's products and services".
  A rendered MP4 re-hosted on Cloudinary and published to YouTube/TikTok is not
  an application interfacing with GIPHY.

  API Terms sections 4 and 5: any application must be conspicuously labelled
  "Powered by GIPHY" with the GIPHY logo, and every piece of content must carry
  GIPHY user/source attribution where available.

So this is a discovery tool for research and inspiration. See MEME-APIS.md.

Reads GIPHY_API_KEY from the environment; the key is never printed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "https://api.giphy.com/v1"
TYPES = ("gifs", "stickers")

# GIPHY requires this label on any application built with the API, plus per-item
# user/source attribution. Printed with every result set so it is never forgotten.
ATTRIBUTION = (
    "Powered by GIPHY. GIPHY requires the 'Powered by GIPHY' mark plus the GIPHY "
    "logo on any application, and per-item user/source attribution. GIPHY content "
    "is licensed for personal, NON-COMMERCIAL use only — do NOT composite these "
    "into a published video."
)


def api_key() -> str:
    key = os.environ.get("GIPHY_API_KEY")
    if not key:
        raise SystemExit("GIPHY_API_KEY is not set. Run: set -a; source .env; set +a")
    return key


def request(path: str, params: dict) -> dict:
    params = dict(params, api_key=api_key())
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = json.loads(response.read())
    meta = payload.get("meta", {})
    if meta.get("status") != 200:
        raise SystemExit(f"GIPHY error {meta.get('status')}: {meta.get('msg')}")
    return payload


def check_type(media_type: str) -> str:
    if media_type not in TYPES:
        raise SystemExit(f"unknown type {media_type!r}; use one of {TYPES}")
    return media_type


def attribution_for(item: dict) -> str:
    """GIPHY requires user and/or source attribution where available."""
    user = (item.get("user") or {}).get("display_name") or \
           (item.get("user") or {}).get("username")
    source = item.get("source_post_url") or item.get("source_tld") or ""
    parts = [p for p in (user, source) if p]
    return " / ".join(parts) if parts else "(no attribution available)"


def show(items: list, limit: int) -> None:
    for item in items[:limit]:
        images = item.get("images", {})
        original = images.get("original", {})
        downsized = images.get("downsized_medium") or original
        print(f"\n{item.get('title') or '(untitled)'}")
        print(f"  id       : {item.get('id')}")
        print(f"  rating   : {item.get('rating', '-')}")
        print(f"  attribute: {attribution_for(item)}")
        if downsized.get("url"):
            print(f"  gif      : {downsized['url']}")
        if original.get("mp4"):
            print(f"  mp4      : {original['mp4']}")
        if item.get("url"):
            print(f"  page     : {item['url']}")
    print(f"\n{len(items[:limit])} result(s).")
    print(f"\nNOTE: {ATTRIBUTION}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="search by keyword")
    search.add_argument("query")
    search.add_argument("--type", default="gifs")
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--rating", default="pg",
                        help="content rating filter: g, pg, pg-13, r")

    trending = sub.add_parser("trending", help="current trending items")
    trending.add_argument("--type", default="gifs")
    trending.add_argument("--limit", type=int, default=5)
    trending.add_argument("--rating", default="pg")

    args = parser.parse_args()
    media_type = check_type(args.type)
    params = {"limit": args.limit, "rating": args.rating}

    if args.command == "search":
        params["q"] = args.query
        payload = request(f"{media_type}/search", params)
    else:
        payload = request(f"{media_type}/trending", params)

    show(payload.get("data", []), args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
