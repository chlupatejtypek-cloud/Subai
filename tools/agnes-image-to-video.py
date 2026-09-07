#!/usr/bin/env python3
"""Animate a public first-frame image with Agnes Video 2.5.

The API key is read from AGNES_API_KEY only; it is never accepted as a CLI
argument, written to task metadata, or printed.

Example:
  set -a; source .env; set +a
  python3 tools/agnes-image-to-video.py \
    --image-url https://res.cloudinary.com/.../scene-01.png \
    --prompt "Subtle breathing, trembling hands, slow camera push..." \
    --seconds 4 --output hook.mp4
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def request_json(method: str, url: str, key: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Subai-Agnes/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:1000]
        raise RuntimeError(f"Agnes HTTP {exc.code}: {body}") from exc


def find_url(value) -> str | None:
    """Find a generated HTTPS video URL in known or nested response fields."""
    if isinstance(value, str):
        if value.startswith("https://") and any(x in value.lower() for x in (".mp4", "video", "output")):
            return value
        return None
    if isinstance(value, dict):
        for key in ("url", "video_url", "output_url", "download_url"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.startswith("https://"):
                return candidate
        for child in value.values():
            candidate = find_url(child)
            if candidate:
                return candidate
    if isinstance(value, list):
        for child in value:
            candidate = find_url(child)
            if candidate:
                return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-url", required=True, help="Public HTTPS first-frame URL")
    parser.add_argument("--prompt", required=True, help="English motion/camera prompt")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seconds", type=int, default=4, choices=range(4, 13), metavar="4..12")
    parser.add_argument("--aspect-ratio", default="9:16")
    parser.add_argument("--model", default="agnes-video-2.5")
    parser.add_argument("--poll-seconds", type=float, default=3.0)
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()

    key = os.environ.get("AGNES_API_KEY", "").strip()
    if not key:
        parser.error("AGNES_API_KEY is not set (load the gitignored .env first)")
    if not args.image_url.startswith("https://"):
        parser.error("--image-url must be a public HTTPS URL (upload it to Cloudinary first)")

    base = os.environ.get("AGNES_API_BASE", "https://apihub.agnes-ai.com/v1").rstrip("/")
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "seconds": str(args.seconds),
        "mode": "keyframe",
        "size": "720P",
        "aspect_ratio": args.aspect_ratio,
        "first_frame": args.image_url,
        "n": 1,
    }
    created = request_json("POST", f"{base}/videos", key, payload)
    video_id = created.get("video_id") or created.get("id")
    if not video_id:
        raise RuntimeError("Agnes create response had no video_id/id: " + json.dumps(created)[:1000])
    print(f"task_created={video_id}", flush=True)

    deadline = time.monotonic() + args.timeout
    latest = created
    while time.monotonic() < deadline:
        status = str(latest.get("status", "")).lower()
        if status in {"completed", "succeeded", "success", "done"}:
            break
        if status in {"failed", "error", "cancelled", "canceled"}:
            raise RuntimeError("Agnes task failed: " + json.dumps(latest)[:1500])
        time.sleep(args.poll_seconds)
        query = urllib.parse.urlencode({"video_id": video_id, "model_name": args.model})
        latest = request_json("GET", f"https://apihub.agnes-ai.com/agnesapi?{query}", key)
        progress = latest.get("progress")
        print(f"status={latest.get('status', 'unknown')} progress={progress if progress is not None else '?'}", flush=True)
    else:
        raise TimeoutError(f"Agnes task {video_id} exceeded {args.timeout}s")

    video_url = find_url(latest)
    if not video_url:
        raise RuntimeError("Completed Agnes response contained no video URL: " + json.dumps(latest)[:1500])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(video_url, headers={"User-Agent": "Subai-Agnes/1.0"})
    with urllib.request.urlopen(req, timeout=180) as response, args.output.open("wb") as target:
        while chunk := response.read(1024 * 1024):
            target.write(chunk)
    if args.output.stat().st_size < 10_000:
        raise RuntimeError("Downloaded Agnes result is unexpectedly small")

    metadata = {
        "model": args.model,
        "video_id": video_id,
        "image_url": args.image_url,
        "prompt": args.prompt,
        "requested_seconds": args.seconds,
        "aspect_ratio": args.aspect_ratio,
        "source_url": video_url,
        "output": str(args.output),
        "bytes": args.output.stat().st_size,
    }
    args.output.with_suffix(args.output.suffix + ".json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"output={args.output}")
    print(f"bytes={args.output.stat().st_size}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
