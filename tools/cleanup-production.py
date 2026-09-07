#!/usr/bin/env python3
"""Safely remove disposable production media from the Arena workspace.

Only untracked files ignored by git are candidates. A production's tracked
`.media-keep` file lists ignored media that must remain locally for pending
work. Dry-run is the default; pass --apply to delete.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def human(n: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(n)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{n} B"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("production", type=Path, help="Path under productions/")
    parser.add_argument("--apply", action="store_true", help="Actually delete; default is dry-run")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    prod = args.production.resolve()
    allowed = (repo / "productions").resolve()
    try:
        prod.relative_to(allowed)
    except ValueError:
        parser.error("production must be inside this repo's productions/ directory")
    if not prod.is_dir():
        parser.error(f"not a production directory: {prod}")

    keep_file = prod / ".media-keep"
    keep: set[Path] = set()
    if keep_file.exists():
        for raw in keep_file.read_text().splitlines():
            line = raw.strip()
            if line and not line.startswith("#"):
                target = (prod / line).resolve()
                try:
                    target.relative_to(prod)
                except ValueError:
                    parser.error(f"unsafe .media-keep path: {line}")
                keep.add(target)

    tracked_raw = subprocess.check_output(
        ["git", "-C", str(repo), "ls-files", "-z", "--", str(prod.relative_to(repo))]
    )
    tracked = {(repo / p.decode()).resolve() for p in tracked_raw.split(b"\0") if p}

    candidates: list[Path] = []
    for path in prod.rglob("*"):
        if not path.is_file() or path.resolve() in keep or path.resolve() in tracked:
            continue
        check = subprocess.run(
            ["git", "-C", str(repo), "check-ignore", "-q", str(path)],
            check=False,
        )
        if check.returncode == 0:
            candidates.append(path)

    candidates.sort()
    total = sum(p.stat().st_size for p in candidates)
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"mode={mode} files={len(candidates)} bytes={total} ({human(total)})")
    for path in candidates:
        print(f"{'DELETE' if args.apply else 'would-delete'} {path.relative_to(prod)} ({human(path.stat().st_size)})")
        if args.apply:
            path.unlink()

    if args.apply:
        for directory in sorted((p for p in prod.rglob("*") if p.is_dir()), reverse=True):
            try:
                directory.rmdir()
            except OSError:
                pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
