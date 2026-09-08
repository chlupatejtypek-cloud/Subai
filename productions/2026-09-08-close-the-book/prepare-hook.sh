#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -y -v error -i assets/hook-retry.mp4 -vf 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30' -t 3.6 -an -c:v libx264 -preset fast -crf 20 -threads 2 assets/hook-ready.mp4
