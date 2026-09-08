import importlib.util
import sys
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("make_cover", ROOT / "tools/make-cover.py")
mc = importlib.util.module_from_spec(spec)
sys.modules["make_cover"] = mc
spec.loader.exec_module(mc)


def base_image(color=(200, 180, 140)):
    return Image.new("RGB", (1080, 1920), color)


class CoverGeometry(unittest.TestCase):
    def test_canvas_is_tiktok_spec(self):
        cover = mc.cover_from(base_image(), "Say it out loud", "kicker", "MARK")
        self.assertEqual(cover.size, (1080, 1920))

    def test_headline_stays_inside_grid_safe_square(self):
        cover = mc.cover_from(base_image(), "Say it out loud", "kicker", "MARK")
        top, bottom = cover.info["headline_band"]
        self.assertGreaterEqual(top, mc.GRID_SAFE[1])
        self.assertLessEqual(bottom, mc.GRID_SAFE[3])

    def test_headline_clears_the_auto_title_gutter(self):
        cover = mc.cover_from(base_image(), "Say it out loud", "kicker", "MARK")
        _, bottom = cover.info["headline_band"]
        self.assertLess(bottom, 1920 - mc.TITLE_GUTTER)

    def test_single_word_and_long_headline_both_fit(self):
        for text in ("Blur", "Add a when", "Same money different story"):
            cover = mc.cover_from(base_image(), text, "", "MARK")
            top, bottom = cover.info["headline_band"]
            self.assertGreaterEqual(top, mc.GRID_SAFE[1], text)
            self.assertLessEqual(bottom, mc.GRID_SAFE[3], text)


class HeadlineFitting(unittest.TestCase):
    def setUp(self):
        self.draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    def test_never_sets_below_minimum_size(self):
        lines, _, size = mc.fit_headline(self.draw, "ADD A WHEN", 936, max_lines=2,
                                         hi=175)
        self.assertGreaterEqual(size, mc.MIN_HEADLINE_PX)
        self.assertLessEqual(len(lines), 2)

    def test_refuses_a_headline_that_cannot_be_read(self):
        with self.assertRaises(SystemExit):
            mc.fit_headline(
                self.draw,
                "THIS HEADLINE IS FAR TOO LONG TO EVER BE LEGIBLE ON A PHONE GRID "
                "THUMBNAIL AT TWO HUNDRED PIXELS WIDE",
                936, max_lines=2, hi=175,
            )


class Validation(unittest.TestCase):
    def test_a_well_formed_cover_passes_every_check(self):
        cover = mc.cover_from(base_image(), "Say it out loud",
                              "The spider test", "STILES PSYCHOLOGY")
        checks = mc.validate(cover, 175)
        failed = [c.name for c in checks if not c.ok]
        self.assertEqual(failed, [], f"unexpected failures: {failed}")

    def test_contrast_check_rejects_pale_type_on_pale_art(self):
        # A cover built without the dark panel: cream on cream must fail.
        flat = Image.new("RGB", (1080, 1920), mc.CREAM)
        d = ImageDraw.Draw(flat)
        font = mc.load_font(mc.FONT_DISPLAY, 175)
        d.text((72, 1150), "SAY IT", font=font, fill=mc.CREAM)
        flat.info["headline_band"] = (1150, 1330)
        checks = {c.name: c for c in mc.validate(flat, 175)}
        self.assertFalse(checks["headline_contrast"].ok)

    def test_gutter_check_rejects_a_busy_bottom_strip(self):
        cover = mc.cover_from(base_image(), "Say it", "", "MARK")
        d = ImageDraw.Draw(cover)
        for x in range(0, 1080, 40):
            d.rectangle([x, 1700, x + 20, 1920], fill=(255, 255, 255))
        checks = {c.name: c for c in mc.validate(cover, 175)}
        self.assertFalse(checks["title_gutter_quiet"].ok)

    def test_contrast_uses_the_actual_headline_band(self):
        cover = mc.cover_from(base_image(), "Say it out loud", "k", "MARK")
        checks = {c.name: c for c in mc.validate(cover, 175)}
        self.assertGreaterEqual(
            float(checks["headline_contrast"].detail.split(":")[0]), 4.5
        )


class Constants(unittest.TestCase):
    def test_grid_safe_square_is_the_centre_1080(self):
        x0, y0, x1, y1 = mc.GRID_SAFE
        self.assertEqual((x1 - x0, y1 - y0), (1080, 1080))
        self.assertEqual(y0, (1920 - 1080) // 2)

    def test_legibility_test_size_is_the_profile_grid_size(self):
        self.assertEqual(mc.THUMB_TEST, (200, 350))


if __name__ == "__main__":
    unittest.main()
