#!/usr/bin/env bash
# Local renderer only: no HeyGen account, API token or cloud charge.
set -euo pipefail
RUNTIME="${HYPERFRAMES_RUNTIME:-/home/user/hyperframes-runtime}"
mkdir -p "$RUNTIME"
cd "$RUNTIME"
[[ -f package.json ]] || npm init -y >/dev/null
npm install --save-exact node@22.23.2 hyperframes@0.8.31 gsap@3.15.0 --no-audit --no-fund
export PATH="$RUNTIME/node_modules/node/bin:$PATH"
"$RUNTIME/node_modules/.bin/hyperframes" telemetry disable
# On a minimal Debian host Chrome may additionally need libnss3 and libnspr4.
# If the renderer reports missing libraries, install those OS packages explicitly.
