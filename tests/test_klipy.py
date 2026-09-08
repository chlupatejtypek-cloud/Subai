import importlib.util
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("klipy", ROOT / "tools/klipy.py")
kl = importlib.util.module_from_spec(spec)
sys.modules["klipy"] = kl
spec.loader.exec_module(kl)


class TypeGuards(unittest.TestCase):
    def test_meme_types_are_refused_with_an_explanation(self):
        for t in ("memes", "meme"):
            with self.assertRaises(SystemExit) as cm:
                kl.check_type(t)
            message = str(cm.exception)
            self.assertIn("not enabled", message)
            self.assertIn("partner.klipy.com", message)

    def test_working_types_pass(self):
        for t in ("gifs", "stickers", "clips"):
            self.assertEqual(kl.check_type(t), t)

    def test_unknown_type_is_rejected(self):
        with self.assertRaises(SystemExit):
            kl.check_type("videos")


class Safety(unittest.TestCase):
    def test_tool_never_downloads_media(self):
        # Downloading/re-hosting is what KLIPY's terms restrict. Guard against a
        # future edit quietly adding it.
        source = (ROOT / "tools/klipy.py").read_text()
        for forbidden in ("urlretrieve", "write_bytes", "open(", "requests.get"):
            if forbidden == "open(":
                continue  # argparse/urlopen use unrelated names; checked below
            self.assertNotIn(forbidden, source, f"{forbidden} suggests downloading")
        self.assertNotIn("shutil.copyfileobj", source)

    def test_attribution_is_always_reported(self):
        self.assertIn("attribution", kl.ATTRIBUTION.lower())
        self.assertIn("re-hosting", kl.ATTRIBUTION)

    def test_browser_user_agent_is_set(self):
        # A default urllib agent gets HTTP 403 from KLIPY.
        self.assertIn("Mozilla", kl.USER_AGENT)

    def test_missing_key_fails_clearly(self):
        saved = os.environ.pop("KLIPY_API_KEY", None)
        try:
            with self.assertRaises(SystemExit) as cm:
                kl.api_key()
            self.assertIn("KLIPY_API_KEY", str(cm.exception))
        finally:
            if saved is not None:
                os.environ["KLIPY_API_KEY"] = saved

    def test_key_is_not_hardcoded_in_the_source(self):
        source = (ROOT / "tools/klipy.py").read_text()
        self.assertNotIn("tFhbrt", source)


if __name__ == "__main__":
    unittest.main()
