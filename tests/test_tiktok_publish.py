import importlib.util
import json
import os
import tempfile
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("tiktok_publish",
                                              ROOT / "tools/tiktok-publish.py")
tp = importlib.util.module_from_spec(spec)
sys.modules["tiktok_publish"] = tp
spec.loader.exec_module(tp)


def make_production(tmp, *, cover_ok=True, cover=True, mp4=True, hold=False,
                    duration=43.1):
    p = Path(tmp) / "prod"
    p.mkdir()
    if cover:
        (p / "cover.png").write_bytes(b"x")
        (p / "cover.json").write_text(json.dumps({
            "all_checks_passed": cover_ok,
            "checks": [{"name": "headline_contrast", "ok": cover_ok, "detail": ""}],
        }))
    assets = [{"file": "final.mp4", "url": "https://example.com/final.mp4"}] if mp4 else []
    (p / "assets.json").write_text(json.dumps(assets))
    (p / "technical-qc.json").write_text(json.dumps({"duration_seconds": duration}))
    (p / "review-status.json").write_text(json.dumps({"publication_hold": hold}))
    return p


class Preflight(unittest.TestCase):
    def test_clean_production_has_no_problems(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t)
            self.assertEqual(tp.preflight(p, 18000, "SELF_ONLY", False), [])

    def test_missing_cover_blocks_the_post(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t, cover=False)
            self.assertTrue(any("cover.png missing" in x
                                for x in tp.preflight(p, 18000, "SELF_ONLY", False)))

    def test_failed_cover_checks_block_the_post(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t, cover_ok=False)
            self.assertTrue(any("failed its checks" in x
                                for x in tp.preflight(p, 18000, "SELF_ONLY", False)))

    def test_owner_hold_blocks_the_post(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t, hold=True)
            self.assertTrue(any("publication_hold" in x
                                for x in tp.preflight(p, 18000, "SELF_ONLY", False)))

    def test_cover_timestamp_beyond_the_video_is_rejected(self):
        # TikTok returns invalid-cover-asset for an out-of-range timestamp.
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t, duration=43.1)
            problems = tp.preflight(p, 90000, "SELF_ONLY", False)
            self.assertTrue(any("outside the video" in x for x in problems))

    def test_zero_cover_timestamp_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t)
            self.assertTrue(any("cover-ms 0" in x
                                for x in tp.preflight(p, 0, "SELF_ONLY", False)))

    def test_draft_mode_ignores_the_cover_timestamp(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t)
            self.assertEqual(tp.preflight(p, 999999, "SELF_ONLY", True), [])

    def test_unknown_privacy_level_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t)
            self.assertTrue(any("unknown privacy" in x
                                for x in tp.preflight(p, 18000, "PUBLIC", False)))

    def test_unbacked_video_blocks_the_post(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t, mp4=False)
            self.assertTrue(any("no .mp4 URL" in x
                                for x in tp.preflight(p, 18000, "SELF_ONLY", False)))


class Payload(unittest.TestCase):
    def test_direct_post_carries_the_cover_timestamp(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t)
            pay = tp.build_payload(p, "caption", "SELF_ONLY", 18000, False)
            self.assertEqual(pay["post_mode"], "DIRECT_POST")
            self.assertEqual(pay["post_info"]["video_cover_timestamp_ms"], 18000)

    def test_draft_mode_sends_to_the_inbox_without_a_timestamp(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t)
            pay = tp.build_payload(p, "caption", "SELF_ONLY", 18000, True)
            self.assertEqual(pay["post_mode"], "MEDIA_UPLOAD")
            self.assertNotIn("video_cover_timestamp_ms", pay["post_info"])

    def test_ai_disclosure_is_always_set(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t)
            pay = tp.build_payload(p, "caption", "SELF_ONLY", 18000, False)
            self.assertTrue(pay["post_info"]["is_aigc"])

    def test_video_is_pulled_from_the_backed_up_url(self):
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t)
            pay = tp.build_payload(p, "caption", "SELF_ONLY", 18000, False)
            self.assertEqual(pay["source_info"]["source"], "PULL_FROM_URL")
            self.assertEqual(pay["source_info"]["video_url"],
                             "https://example.com/final.mp4")

    def test_no_custom_cover_url_field_is_ever_sent(self):
        # The v2 Direct Post API rejects external cover URLs.
        with tempfile.TemporaryDirectory() as t:
            p = make_production(t)
            pay = tp.build_payload(p, "caption", "SELF_ONLY", 18000, False)
            self.assertNotIn("video_cover_image_url", json.dumps(pay))


class Secrets(unittest.TestCase):
    def test_missing_secrets_are_reported(self):
        saved = {k: os.environ.pop(k, None) for k in tp.REQUIRED_SECRETS}
        try:
            self.assertEqual(set(tp.missing_secrets()), set(tp.REQUIRED_SECRETS))
        finally:
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v


if __name__ == "__main__":
    unittest.main()
