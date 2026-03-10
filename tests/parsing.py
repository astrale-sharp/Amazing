from unittest import TestCase
from source.parse import Parser
from source.vector2 import Vector2


class ParsingTests(TestCase):
    def test_empty(self):
        txt = """"""
        try:
            Parser.parse(txt)
            self.fail("should raise Value Error with missing keys")
        except ValueError as v:
            pass

    def test_missing_key(self):
        txt = """WIDTH=4
                 HEIGHT=5
                 ENTRY=6,7
                 OUTPUT_FILE=x
                 PERFECT=True
                 """
        try:
            Parser.parse(txt)
            self.fail("should fail with missing key")
        except ValueError as v:
            pass

    def test_bad_int_value(self):
        txt = """WIDTH=4
                 HEIGHT=ewr
                 ENTRY=6,7
                 EXIT=0,9
                 OUTPUT_FILE=x
                 PERFECT=True
                 """
        try:
            Parser.parse(txt)
            self.fail("should fail with bad int value")
        except ValueError as v:
            pass

    def test_bad_bool_value(self):
        txt = """WIDTH=4
                 HEIGHT=5
                 ENTRY=6,7
                 EXIT=0,9
                 OUTPUT_FILE=x
                 PERFECT=Treue
                 """
        try:
            Parser.parse(txt)
            self.fail("should fail with bas bool")
        except ValueError as v:
            pass

    def test_too_big(self):
        txt = """WIDTH=14000
                 HEIGHT=5
                 ENTRY=6,7
                 EXIT=0,9
                 OUTPUT_FILE=x
                 PERFECT=True
                 """
        try:
            Parser.parse(txt)
            self.fail("should fail with too large")
        except ValueError as v:
            pass

    def test_outside(self):
        txt = """WIDTH=14
                 HEIGHT=5
                 ENTRY=14,7
                 EXIT=0,9
                 OUTPUT_FILE=x
                 PERFECT=True
                 """
        try:
            Parser.parse(txt)
            self.fail("should fail with outside")
        except ValueError:
            pass

    def test_good_data(self):
        txt = """WIDTH=7
                 HEIGHT=8
                 ENTRY=1,2
                 EXIT=3,0
                 OUTPUT_FILE=x
                 PERFECT=True
                 """
        ret = Parser.parse(txt)
        self.assertEqual(ret.width, 7)
        self.assertEqual(ret.height, 8)
        self.assertEqual(Vector2.from_iter(ret.entry), Vector2(1, 2))
        self.assertEqual(Vector2.from_iter(ret.exit), Vector2(3, 0))
        self.assertEqual(ret.output_file, "x")
        self.assertEqual(ret.perfect, True)
        self.assertEqual(ret.seed, None)


    def test_good_data_with_alt(self):
        txt = """WIDTH=7
                 HEIGHT=8
                 ENTRY=1,2
                 EXIT=3,0
                 OUTPUT_FILE=x
                 PERFECT=True
                 ALT=True
                 """
        ret = Parser.parse(txt)
        self.assertEqual(ret.width, 7)
        self.assertEqual(ret.height, 8)
        self.assertEqual(Vector2.from_iter(ret.entry), Vector2(1, 2))
        self.assertEqual(Vector2.from_iter(ret.exit), Vector2(3, 0))
        self.assertEqual(ret.output_file, "x")
        self.assertEqual(ret.perfect, True)
        self.assertEqual(ret.seed, None)
        self.assertEqual(ret.alt, True)

    def test_good_data_with_seed(self):
        txt = """WIDTH=7
                 HEIGHT=8
                 ENTRY=1,2
                 EXIT=3,0
                 OUTPUT_FILE=x
                 PERFECT=True
                 SEED=eyyeyeye
                 """
        ret = Parser.parse(txt)
        self.assertEqual(ret.seed, "eyyeyeye")


    def test_with_theme(self):
        txt = """WIDTH=7
                 HEIGHT=8
                 ENTRY=1,2
                 EXIT=3,0
                 OUTPUT_FILE=x
                 PERFECT=True
                 THEME=rgb
                 """
        ret = Parser.parse(txt)
        self.assertEqual(ret.theme, "rgb")

    def test_with_invalid_theme(self):
        txt = """WIDTH=7
                 HEIGHT=8
                 ENTRY=1,2
                 EXIT=3,0
                 OUTPUT_FILE=x
                 PERFECT=True
                 THEME=rgba
                 """
        try:
            Parser.parse(txt)
            self.fail("Should have failed with rgba invalid")
        except ValueError:
            pass

    def test_with_drawing(self):
        txt = """WIDTH=7
                 HEIGHT=8
                 ENTRY=1,2
                 EXIT=3,0
                 OUTPUT_FILE=x
                 PERFECT=True
                 DRAWING=42
                 """
        r = Parser.parse(txt)
        self.assertEqual(r.drawing, "42")

    def test_with_invalid_drawing(self):
        txt = """WIDTH=7
                 HEIGHT=8
                 ENTRY=1,2
                 EXIT=3,0
                 OUTPUT_FILE=x
                 PERFECT=True
                 DRAWING=rgb
                 """
        try:
            Parser.parse(txt)
            self.fail("Should have failed with rgb invalid")
        except ValueError:
            pass
