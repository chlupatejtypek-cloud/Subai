# YouTube account connection

## Verified connection — 2026-09-07
- Owner completed Google OAuth consent with `youtube.upload` and `youtube.readonly`.
- A subsequent live channels.list(mine=true) request returned HTTP 200.
- Connected channel: **Chlupatej Typek** (`UCcWp-VFQ1zzI8Bl3n7krB6w`).
- This is the authenticated channel; do not assume it is a different Stiles Psychology channel.
- Access and refresh tokens are stored only in `.git/credentials`, mode 600. This JSON file is excluded from workspace snapshots, never tracked in Git. Do not configure git credential-store to use it.
- OAuth client configuration remains in gitignored `credentials/youtube-client.json`.
- The owner requested removal of the connection webpage. Its server was stopped and its source was deleted from the current branch. No authorization code or token is recorded here.

## Future authorization
The owner prefers a direct Google authorization link in chat rather than a separate form. Explain that a callback URL contains a short-lived sensitive code; never repeat or store it in project files or logs. Retain state and PKCE verifier securely for the exchange, validate state, and use only Google's OAuth token endpoint. A fresh login will be required if the environment loses its token files. Testing-mode refresh tokens for these scopes can expire after seven days.

## Upload/publication gate
Connection alone does not upload or publish anything. Confirm the intended channel, video, metadata and visibility with the owner. Prefer a private test upload followed by explicit publication approval. An unverified YouTube API project may be restricted to private uploads and may require audit before public uploads.

No video has been uploaded by this connection workflow. Upload tooling is still to be implemented/tested.
