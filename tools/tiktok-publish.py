#!/usr/bin/env python3
"""Post a finished production to TikTok via the Content Posting API v2.

Dry run by default. Nothing is sent without --execute, and --execute refuses to
run unless credentials exist and the production passes its preflight.

See TIKTOK.md for the constraints this implements, in particular: the v2 Direct
Post API accepts only `video_cover_timestamp_ms`, not a custom cover image, so
the designed cover must correspond to a real frame of the video (or the post
must go to the inbox as a draft and be finished in the app).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

API = "https://open.tiktokapis.com/v2"
ROOT = Path(__file__).resolve().parent.parent

REQUIRED_SECRETS = ("TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET",
                    "TIKTOK_REFRESH_TOKEN")


def missing_secrets() -> list[str]:
    return [k for k in REQUIRED_SECRETS if not os.environ.get(k)]


def load_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def video_url(prod: Path) -> str | None:
    assets = load_json(prod / "assets.json") or []
    vids = [a for a in assets if a["file"].endswith(".mp4")]
    return vids[0]["url"] if vids else None


def video_duration_ms(prod: Path) -> int | None:
    qc = load_json(prod / "technical-qc.json") or {}
    for key in ("duration_seconds", "duration", "runtime_seconds"):
        if key in qc:
            try:
                return int(float(qc[key]) * 1000)
            except (TypeError, ValueError):
                pass
    return None


def access_token() -> str:
    import requests
    r = requests.post(
        f"{API}/oauth/token/",
        data={
            "client_key": os.environ["TIKTOK_CLIENT_KEY"],
            "client_secret": os.environ["TIKTOK_CLIENT_SECRET"],
            "grant_type": "refresh_token",
            "refresh_token": os.environ["TIKTOK_REFRESH_TOKEN"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def creator_info(token: str) -> dict:
    """Must be queried before every post; it defines the allowed privacy levels."""
    import requests
    r = requests.post(
        f"{API}/post/publish/creator_info/query/",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json; charset=UTF-8"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["data"]


def preflight(prod: Path, cover_ms: int, privacy: str, draft: bool) -> list[str]:
    problems = []
    if not (prod / "cover.png").exists():
        problems.append("cover.png missing — run tools/make-cover.py --apply")
    cover = load_json(prod / "cover.json")
    if cover is None:
        problems.append("cover.json missing — cover was never validated")
    elif not cover.get("all_checks_passed"):
        failed = [c["name"] for c in cover.get("checks", []) if not c["ok"]]
        problems.append(f"cover failed its checks: {', '.join(failed)}")

    if not video_url(prod):
        problems.append("no .mp4 URL in assets.json — back the master up first")

    review = load_json(prod / "review-status.json") or {}
    if review.get("publication_hold"):
        problems.append("publication_hold is set — the owner is holding this video")

    dur = video_duration_ms(prod)
    if dur and not draft and not (0 < cover_ms < dur):
        problems.append(
            f"--cover-ms {cover_ms} is outside the video (0..{dur} ms); "
            "TikTok rejects an out-of-range cover timestamp"
        )
    if not draft and cover_ms == 0:
        problems.append("--cover-ms 0 is rejected by TikTok; pick a real frame")
    if privacy not in ("PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS",
                       "FOLLOWER_OF_CREATOR", "SELF_ONLY"):
        problems.append(f"unknown privacy level {privacy!r}")
    return problems


def build_payload(prod: Path, caption: str, privacy: str, cover_ms: int,
                  draft: bool) -> dict:
    post_info = {
        "title": caption,
        "privacy_level": privacy,
        "disable_comment": False,
        "disable_duet": False,
        "disable_stitch": False,
        "video_cover_timestamp_ms": cover_ms,
        # Our illustrations and narration are synthetic. Disclosure is required.
        "is_aigc": True,
    }
    payload = {
        "post_info": post_info,
        "source_info": {"source": "PULL_FROM_URL", "video_url": video_url(prod)},
    }
    if draft:
        # MEDIA_UPLOAD sends the video to the creator inbox so the designed
        # cover.png can be attached by hand in the app.
        payload["post_mode"] = "MEDIA_UPLOAD"
        payload["post_info"].pop("video_cover_timestamp_ms", None)
    else:
        payload["post_mode"] = "DIRECT_POST"
    return payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--production", type=Path, required=True)
    ap.add_argument("--caption", help="first line is printed over the cover gutter")
    ap.add_argument("--privacy", default="SELF_ONLY")
    ap.add_argument("--cover-ms", type=int, default=18000,
                    help="frame used as the cover; must match the designed cover")
    ap.add_argument("--draft", action="store_true",
                    help="send to the TikTok inbox so cover.png can be attached "
                         "manually in the app (preferred, see TIKTOK.md)")
    ap.add_argument("--execute", action="store_true")
    args = ap.parse_args()

    prod = args.production
    if not prod.is_dir():
        raise SystemExit(f"no such production: {prod}")

    caption = args.caption
    if not caption:
        readme = (prod / "README.md")
        caption = readme.read_text().splitlines()[0].lstrip("# ").strip() \
            if readme.exists() else prod.name

    problems = preflight(prod, args.cover_ms, args.privacy, args.draft)
    payload = build_payload(prod, caption, args.privacy, args.cover_ms, args.draft)

    print(f"production : {prod}")
    print(f"caption    : {caption}")
    print(f"mode       : {'MEDIA_UPLOAD (draft, manual cover)' if args.draft else 'DIRECT_POST'}")
    print(f"cover      : {prod / 'cover.png'}")
    print("\npayload that would be sent:")
    print(json.dumps(payload, indent=2))

    secrets = missing_secrets()
    if problems:
        print("\npreflight problems:")
        for p in problems:
            print(f"  - {p}")
    if secrets:
        print(f"\nmissing credentials: {', '.join(secrets)}")
        print("Add them to .env and to the GitHub Actions secrets, then re-run. "
              "See TIKTOK.md section 6.")

    if not args.execute:
        print("\nDRY RUN — nothing was sent. Re-run with --execute to post.")
        return

    if problems or secrets:
        raise SystemExit("\nrefusing to post: resolve the items above first")

    token = access_token()
    info = creator_info(token)
    allowed = info.get("privacy_level_options", [])
    if args.privacy not in allowed:
        raise SystemExit(
            f"privacy {args.privacy} not permitted for this creator; "
            f"allowed: {allowed}"
        )

    import requests
    r = requests.post(
        f"{API}/post/publish/video/init/",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json; charset=UTF-8"},
        json=payload, timeout=60,
    )
    r.raise_for_status()
    publish_id = r.json()["data"]["publish_id"]
    print(f"\npublish_id: {publish_id}")

    for _ in range(40):
        time.sleep(6)
        s = requests.post(
            f"{API}/post/publish/status/fetch/",
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json; charset=UTF-8"},
            json={"publish_id": publish_id}, timeout=30,
        )
        s.raise_for_status()
        status = s.json()["data"]["status"]
        print(f"  status: {status}")
        if status in ("PUBLISH_COMPLETE", "FAILED"):
            break

    record = prod / "tiktok.json"
    record.write_text(json.dumps({
        "publish_id": publish_id,
        "status": status,
        "mode": payload["post_mode"],
        "privacy": args.privacy,
        "caption": caption,
        "cover": "cover.png",
        "cover_timestamp_ms": payload["post_info"].get("video_cover_timestamp_ms"),
        "manual_cover_required": bool(args.draft),
    }, indent=2) + "\n")
    print(f"wrote {record}")
    if status != "PUBLISH_COMPLETE":
        sys.exit(1)


if __name__ == "__main__":
    main()
