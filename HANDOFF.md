# Encrypted handoff: exact format and local install

Fetch current main's config/transfer.json. Download its **versioned_url**, verify SHA256 and bytes before decryption. Do not use a cached stable URL against the checksum of another version. Password comes from the owner; do not store it here. It is NOT the Cloudinary dashboard password.

## Format (all parameters matter)
- Binary OpenSSL `Salted__` envelope, **8-byte salt**; no Base64 wrapper.
- AES-256-CBC; PBKDF2-HMAC-SHA256; **600000 iterations**.
- Decrypted plaintext is **TAR.GZ**, not directly readable text.
- CBC is not authenticated encryption. The expected SHA256 must come from trusted current repository metadata; that checksum is not a secret or a MAC. The owner retained a weak password; encryption does not make that password strong.

Download as `subai-agent-bootstrap.enc`. Bash/OpenSSL command, compatible with both old and new OpenSSL:

```bash
salt_args=()
if openssl enc -help 2>&1 | grep -q -- '-saltlen'; then
  salt_args=(-saltlen 8)
fi
openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -md sha256 \
  "${salt_args[@]}" -in subai-agent-bootstrap.enc -out subai-agent-bootstrap.tar.gz
# Enter the owner-supplied password at OpenSSL's prompt.
tar -tzf subai-agent-bootstrap.tar.gz
```

Use a private directory (mode700) and restrictive umask (`umask 077`). Before extracting, verify members are ordinary relative files under `subai-agent-bootstrap/`, no symlinks or `..`; do not blindly extract an untrusted archive. Inspect `START_HERE.md`. Never print credentials or upload plaintext archives.

## Install supplied secrets locally
Clone/fetch main, then:

```bash
python tools/install-handoff.py --bundle /private/subai-agent-bootstrap --repo /workspace/Subai
python tools/install-handoff.py --bundle /private/subai-agent-bootstrap --repo /workspace/Subai --apply
```

Dry run lists intended destinations only. Apply merges missing environment keys, refuses differing existing credentials, writes mode600 files, and makes no external API calls. It will not overwrite a valid newer token silently. Read START_HERE.md and AGENT.md next; verify access, then proceed without unnecessary questions.

## Maintenance
`tools/build-handoff.py --upload` keeps the same Cloudinary public ID and records a new versioned URL/hash. It tests a round trip before upload and checks the downloaded ciphertext. The format explicitly pins salt length where OpenSSL supports that switch. CI refreshes run under the shared publisher lock. Use the workflow, not concurrent local uploads, for the authoritative refresh. The archive contains current START_HERE.md, credentials and a tracked repo snapshot, but never its own passphrase.
