# YouTube account connection and limits

Registered channel: Chlupatej Typek, UCcWp-VFQ1zzI8Bl3n7krB6w; brand Stiles Psychology. Verify channels.list(mine=true), never assume a Google email identifies the right channel.

## Existing credentials
Owner supplied OAuth with youtube.upload + youtube.readonly. Private client JSON: credentials/youtube-client.json. Private token JSON: .git/credentials (not Git credential-store). Both mode600. If the sandbox loses a file, restore the owner-supplied encrypted handoff before asking for another login. Access tokens are refreshed on demand, not stored as durable credentials.

## Capability distinction
- Upload and readonly account/video checks were successfully exercised. Original phone OYEY9ZKOitA was verified public and processed.
- **Existing-video status edits/cancelling publishAt failed403 ACCESS_TOKEN_SCOPE_INSUFFICIENT on2026-09-08.** Upload permission is not update permission. The owner authorized cancelling FACZAzrfEdU, but that API operation did NOT succeed. Its last recorded lookup still had23:00 Prague publishAt; check live state, do not assume cancellation.
- To cancel now, owner can change visibility to Private in Studio. For agent-side edits, request Google's consent for an appropriate documented videos.update scope, preserving existing necessary scopes. A new refresh token must then be verified and propagated to local files, Actions secrets and encrypted handoff. Merely editing a scope string or re-encrypting the old token grants nothing.
- Do not issue more identical update requests after an insufficient-scope response. Do not delete/reupload as a permission workaround.

## Authorization UX
Owner prefers a direct Google authorization link in chat, not a separate OAuth webpage. Securely retain state/PKCE, validate callbacks and use Google's token endpoint. Never echo authorization codes, access tokens, refresh tokens or full callbacks into public records. External consent cannot be automated away.

## Publishing and verification
The90-video calendar has delegated publication after QA; do not ask approval for every routine topic/script. Respect rejected work, new-style preview holds, specific replacement permissions and owner cancellation requests. Check actual post-upload processing/schedule; an unavailable video ID is a reconciliation problem, not a reason for blind retries. Do not make test uploads during an audit.

Consent-screen mode and formal audit state remain unknown. Testing-mode tokens may expire; a previously successful public upload is not proof that all future credentials/permissions remain valid.
