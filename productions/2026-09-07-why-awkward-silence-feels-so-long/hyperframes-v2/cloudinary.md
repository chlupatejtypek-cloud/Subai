# Verified durable deliverables

- silence-hyperframes-final.mp4: https://res.cloudinary.com/e5cjysjx/video/upload/v1788817627/subai/productions/stiles-psychology/2026-09-07-awkward-silence/hyperframes-v2/silence-hyperframes-final.mp4
  - SHA256 `068b07705935d85a22dbe00dd64e5047e04b4bf6d4490a1a5adc8845d03092f3`, HTTP 200 downloaded/checksum matched.
- project-part-1.json: https://res.cloudinary.com/e5cjysjx/raw/upload/v1788817711/subai/productions/stiles-psychology/2026-09-07-awkward-silence/hyperframes-v2/project-part-1.json
  - SHA256 `6fac6e7df49b37f70f3733487887e04bb3e8e6538edb872eba116977fa0bfde9`, HTTP 200 downloaded/checksum matched.
- project-part-2.json: https://res.cloudinary.com/e5cjysjx/raw/upload/v1788817713/subai/productions/stiles-psychology/2026-09-07-awkward-silence/hyperframes-v2/project-part-2.json
  - SHA256 `685309add4fa118b10383db5a6f385ce2171e1d94b5e9f7aead3bc88491b86c3`, HTTP 200 downloaded/checksum matched.
- project-part-3.json: https://res.cloudinary.com/e5cjysjx/raw/upload/v1788817715/subai/productions/stiles-psychology/2026-09-07-awkward-silence/hyperframes-v2/project-part-3.json
  - SHA256 `51536e25032f8ca81a4ad6548aa19ca226d4cfd2ddc0147f65715b3e7c95caec`, HTTP 200 downloaded/checksum matched.
- sfx-zoom-ui-preview.wav: https://res.cloudinary.com/e5cjysjx/video/upload/v1788817716/subai/productions/stiles-psychology/2026-09-07-awkward-silence/hyperframes-v2/sfx-zoom-ui-preview.wav
  - SHA256 `a89b025892bdd9a4f261ca2ccc12d9caafea0613c95c8d3074c5b17961a58876`, HTTP 200 downloaded/checksum matched.

Direct ZIP and TAR.GZ delivery returned HTTP 401; they are NOT relied on as backups. Full project is instead stored as three plain JSON/base64 parts above, each HTTP/checksum verified. Concatenate decoded payloads in part order to reconstruct TAR.GZ, verify archive_sha256, then safely extract.
