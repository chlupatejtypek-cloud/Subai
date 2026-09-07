#!/usr/bin/env python3
"""Generate Fish Audio speech and preserve provider timestamp alignment.

Reads FISH_API_KEY from the environment. The key is never accepted on the
command line or written to output metadata.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--text-file", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--reference-id", help="Explicit override; defaults to the channel registry voice")
    parser.add_argument("--channel", default="stiles-psychology")
    parser.add_argument("--model", default="s2.1-pro-free")
    parser.add_argument("--format", choices=("opus", "mp3", "wav"), default="opus")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--latency", choices=("normal", "balanced"), default="normal")
    args = parser.parse_args()

    registry = json.loads((Path(__file__).resolve().parents[1] / "config/channels.json").read_text())
    channel = next((c for c in registry["channels"] if c["id"] == args.channel), None)
    if channel is None or channel["voice"]["provider"] != "fish_audio":
        parser.error("Channel not found or not configured for Fish Audio")
    args.reference_id = args.reference_id or channel["voice"]["reference_id"]

    key = os.environ.get("FISH_API_KEY", "").strip()
    if not key:
        parser.error("FISH_API_KEY is not set (load the gitignored .env first)")
    text = args.text if args.text is not None else args.text_file.read_text().strip()
    if not text:
        parser.error("input text is empty")
    # Editorial line breaks are not paragraph-pause instructions for TTS.
    text = " ".join(text.split())

    payload = {
        "text": text,
        "format": args.format,
        "latency": args.latency,
        "normalize": True,
        "prosody": {"speed": args.speed, "volume": 0, "normalize_loudness": True},
    }
    if args.reference_id:
        payload["reference_id"] = args.reference_id

    base = os.environ.get("FISH_API_BASE", "https://api.fish.audio").rstrip("/")
    req = urllib.request.Request(
        f"{base}/v1/tts/stream/with-timestamp",
        data=json.dumps(payload).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "model": args.model,
            "User-Agent": "Subai-FishAudio/1.0",
        },
    )

    audio_parts: list[bytes] = []
    alignments: list[dict] = []
    events = 0
    try:
        response = urllib.request.urlopen(req, timeout=180)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:1200]
        raise RuntimeError(f"Fish Audio HTTP {exc.code}: {detail}") from exc

    with response:
        for raw in response:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data: "):
                continue
            event = json.loads(line[6:])
            events += 1
            encoded = event.get("audio_base64")
            if encoded:
                audio_parts.append(base64.b64decode(encoded))
            if event.get("alignment") is not None:
                alignments.append(
                    {
                        "chunk_seq": event.get("chunk_seq"),
                        "content": event.get("content"),
                        "chunk_audio_offset_sec": event.get("chunk_audio_offset_sec", 0),
                        "alignment": event.get("alignment"),
                    }
                )

    audio = b"".join(audio_parts)
    if len(audio) < 1000:
        raise RuntimeError(f"Fish Audio returned too little audio ({len(audio)} bytes)")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(audio)

    metadata = {
        "provider": "Fish Audio",
        "model": args.model,
        "reference_id": args.reference_id,
        "format": args.format,
        "speed": args.speed,
        "events": events,
        "audio_bytes": len(audio),
        "text": text,
        "alignment_chunks": alignments,
    }
    timing_path = args.output.with_suffix(args.output.suffix + ".timestamps.json")
    timing_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    print(f"output={args.output}")
    print(f"bytes={len(audio)}")
    print(f"events={events}")
    print(f"alignment_chunks={len(alignments)}")
    print(f"timestamps={timing_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
