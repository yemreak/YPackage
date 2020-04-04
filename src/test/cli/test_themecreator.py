import unittest

from .commands import check_themecreator


class ThemeCreatorTest(unittest.TestCase):

    def test_help(self):
        with self.assertRaises(SystemExit) as cm:
            check_themecreator(['-h'])
            self.assertEqual(cm.exception.code, 0)

    def test_unknown(self):
        with self.assertRaises(SystemExit) as cm:
            check_themecreator(['-ü'])
            self.assertEqual(cm.exception.code, 2)

    def test_simple_case(self):
        check_themecreator("../DarkCode-Theme/core/settings.json")

    def test_error(self):
        with self.assertRaises(SystemExit) as cm:
            check_themecreator("../DarkCode-Theme/core/darkcode.json")
            self.assertEqual(cm.exception.code, -1)
