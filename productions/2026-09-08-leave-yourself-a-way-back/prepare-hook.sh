#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -y -v error -i assets/hook.mp4 -vf 'trim=duration=2.8,setpts=PTS*1.42857143,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,tpad=stop_mode=clone:stop_duration=0.5' -t 4.45 -an -c:v libx264 -preset fast -crf 20 -threads 2 assets/hook-ready.mp4
