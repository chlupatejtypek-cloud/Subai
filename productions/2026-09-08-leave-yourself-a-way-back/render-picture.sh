#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PATH="/home/user/hyperframes-runtime/node_modules/node/bin:$PATH"
export TMPDIR=/home/user/.cache/hyperframes-tmp
mkdir -p "$TMPDIR"
/home/user/hyperframes-runtime/node_modules/.bin/hyperframes render . --output output/hyperframes-picture.mp4 --fps 30 --quality standard --workers 2 --no-low-memory-mode --no-browser-gpu --strict
