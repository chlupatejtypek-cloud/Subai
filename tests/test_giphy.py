import importlib.util
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("giphy", ROOT / "tools/giphy.py")
gp = importlib.util.module_from_spec(spec)
sys.modules["giphy"] = gp
spec.loader.exec_module(gp)


class TypeGuards(unittest.TestCase):
    def test_supported_types_pass(self):
        for t in ("gifs", "stickers"):
            self.assertEqual(gp.check_type(t), t)

    def test_unknown_type_is_rejected(self):
        with self.assertRaises(SystemExit):
            gp.check_type("clips")


class Attribution(unittest.TestCase):
    def test_user_display_name_is_preferred(self):
        item = {"user": {"display_name": "Kim's Convenience", "username": "kims"}}
        self.assertIn("Kim's Convenience", gp.attribution_for(item))

    def test_falls_back_to_username_then_source(self):
        self.assertIn("natgeo", gp.attribution_for({"user": {"username": "natgeo"}}))
        self.assertIn("bbc.co.uk", gp.attribution_for({"source_tld": "bbc.co.uk"}))

    def test_missing_attribution_is_stated_not_faked(self):
        # API Terms section 5: never falsely attribute content.
        self.assertIn("no attribution available", gp.attribution_for({}))

    def test_warning_states_non_commercial_and_powered_by(self):
        self.assertIn("Powered by GIPHY", gp.ATTRIBUTION)
        self.assertIn("NON-COMMERCIAL", gp.ATTRIBUTION)


class Safety(unittest.TestCase):
    def test_tool_never_downloads_media(self):
        source = (ROOT / "tools/giphy.py").read_text()
        for forbidden in ("urlretrieve", "write_bytes", "shutil.copyfileobj",
                          "requests.get"):
            self.assertNotIn(forbidden, source, f"{forbidden} suggests downloading")

    def test_missing_key_fails_clearly(self):
        saved = os.environ.pop("GIPHY_API_KEY", None)
        try:
            with self.assertRaises(SystemExit) as cm:
                gp.api_key()
            self.assertIn("GIPHY_API_KEY", str(cm.exception))
        finally:
            if saved is not None:
                os.environ["GIPHY_API_KEY"] = saved

    def test_key_is_not_hardcoded(self):
        self.assertNotIn("zsDD0Gw", (ROOT / "tools/giphy.py").read_text())

    def test_default_rating_is_family_safe(self):
        source = (ROOT / "tools/giphy.py").read_text()
        self.assertIn('default="pg"', source)


if __name__ == "__main__":
    unittest.main()
