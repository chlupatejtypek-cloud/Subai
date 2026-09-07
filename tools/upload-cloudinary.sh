#!/usr/bin/env bash
set -euo pipefail

# Upload one image or video to Cloudinary using a signed request.
# Credentials are read only from environment variables (normally loaded from
# the gitignored root .env). They are never printed or committed.
#
# Usage:
#   set -a; source .env; set +a
#   tools/upload-cloudinary.sh FILE [PUBLIC_ID] [FOLDER]

FILE="${1:?Usage: $0 FILE [PUBLIC_ID] [FOLDER]}"
PUBLIC_ID="${2:-$(basename "${FILE%.*}")}"
FOLDER="${3:-subai/uploads}"

: "${CLOUDINARY_CLOUD_NAME:?CLOUDINARY_CLOUD_NAME is required}"
: "${CLOUDINARY_API_KEY:?CLOUDINARY_API_KEY is required}"
: "${CLOUDINARY_API_SECRET:?CLOUDINARY_API_SECRET is required}"

test -f "$FILE" || { echo "File not found: $FILE" >&2; exit 1; }

TIMESTAMP="$(date +%s)"
PARAMS="folder=${FOLDER}&overwrite=true&public_id=${PUBLIC_ID}&timestamp=${TIMESTAMP}"
SIGNATURE="$(printf '%s%s' "$PARAMS" "$CLOUDINARY_API_SECRET" | sha1sum | cut -d' ' -f1)"
RESPONSE="$(mktemp)"
trap 'rm -f "$RESPONSE"' EXIT

HTTP="$(curl -sS -o "$RESPONSE" -w '%{http_code}' -X POST \
  "https://api.cloudinary.com/v1_1/${CLOUDINARY_CLOUD_NAME}/auto/upload" \
  -F "file=@${FILE}" \
  -F "api_key=${CLOUDINARY_API_KEY}" \
  -F "timestamp=${TIMESTAMP}" \
  -F "signature=${SIGNATURE}" \
  -F "folder=${FOLDER}" \
  -F "public_id=${PUBLIC_ID}" \
  -F "overwrite=true")"

if [[ "$HTTP" != 2* ]]; then
  echo "Cloudinary upload failed (HTTP $HTTP):" >&2
  python3 - "$RESPONSE" <<'PY' >&2
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    print(d.get("error", {}).get("message", "Unknown Cloudinary error"))
except Exception:
    print("Unparseable response")
PY
  exit 1
fi

python3 - "$RESPONSE" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("resource_type=" + str(d.get("resource_type")))
print("public_id=" + str(d.get("public_id")))
print("version=" + str(d.get("version")))
print("bytes=" + str(d.get("bytes")))
print("width=" + str(d.get("width", "")))
print("height=" + str(d.get("height", "")))
print("secure_url=" + str(d.get("secure_url")))
PY
