# YouTube connection (interactive, no automatic publishing)

Owner requested agent-side account connection after approving the spotlight-effect video.

## Connect
- Enable YouTube Data API v3 in the Google Cloud project.
- Configure OAuth consent. If External/Testing, add the owner's Google account as a test user.
- Put the owner-provided desktop OAuth client JSON in gitignored `credentials/youtube-client.json`, mode 600.
- Run `python tools/youtube-connect.py`; open its live port 8080 preview.
- Owner signs in directly with Google and selects the intended channel. Requested scopes: `youtube.upload` and `youtube.readonly` (channel verification).
- Google redirects to `http://localhost:8765/` on the owner's computer. No local listener is expected. Copy the entire failed-loopback callback URL into the connector form, NEVER chat or public logs. This uses the desktop client's loopback redirect and an authorization-code exchange with PKCE and state, not the retired OAuth OOB redirect.
- The agent exchanges the code, validates granted scopes, then verifies the channel via channels.list(mine=true).
- Token goes to `.git/credentials`, mode 600, outside Git tracking and excluded from workspace snapshots. This file contains JSON, not a Git credential-helper record; do not configure git credential-store to use it.
- The current connector's state/PKCE verifier are in memory. Restarting it requires a new authorization attempt. Tokens are not guaranteed to survive environment replacement. No secrets in git, Cloudinary, generated reports or chat.
- After successful connection, stop the connector. Revoke access in the owner's Google account when no longer needed.

## Before uploading
Connection alone is not approval to upload or publish. Confirm the verified channel, video, metadata and visibility with the owner. Prefer private upload for review, then explicit publication approval. Upload support will use the connected account and refresh tokens only against Google's token endpoint.

Testing-mode OAuth refresh tokens for these scopes may expire after seven days. Unverified YouTube API projects can be restricted to private uploads; an API audit may be required for public uploads. Do not promise unattended indefinite publishing until project and channel restrictions are checked.
