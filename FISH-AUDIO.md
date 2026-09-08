# Fish Audio: speech versus sound effects
Verified2026-09-08. Existing integration uses FISH_API_KEY with official API for one continuous narration and timestamps, selected reference in config/channels.json. It does not automatically expose every web-app feature.

Fish DOES offer text-prompt Sound Effects in its web app:
https://docs.fish.audio/overview/platform
https://fish.audio/app/sound-effects/
The web page shows Login/Sign up. Public developer OpenAPI https://docs.fish.audio/api-reference/openapi.json was downloaded and all29paths inspected: no path containing sound/effect/sfx/music, matching the developer index. This establishes absence from the inspected public specification, NOT proof no private/beta SFX API exists. No documented SFX request was available to run with the supplied API key. No web login/session has been supplied. Do not invent an endpoint, send keys to unofficial domains, or treat spoken “whoosh” as an SFX generator.

To integrate Fish SFX: use an owner-authorized signed-in web session or obtain official SFX API documentation and verify access/rights; then generate, download, listen/review and mix restrained cues. No paid plan change or secret re-request for working TTS. The Fish SFX product page states commercial rights on paid plans; verify applicable plan/rights before production reuse: https://fish.audio/sound-effects/ . Do not assume API credits prove a web subscription.

Current video fallback is original procedural effects, explicitly labeled as such. No Fish SFX output or successful SFX API call is claimed.

Prepared prompts for future verified Fish SFX access:
- Dry soft paper envelope opening, single gesture,0.5seconds, no voice, no music, no room ambience.
- Two light coins touching a wooden tabletop,0.4seconds, close and restrained, no cash-register bell, no voice or music.
- Soft airy UI panel transition,0.25seconds, gentle, no tonal melody, no speech.
- Quiet soft button confirmation,0.15seconds, no jingle, no voice.
