import unittest

from .commands import check_themecreator


class ThemeCreatorTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_case(self):
        check_themecreator("../DarkCode-Theme/core/settings.json")

    def test_error(self):
        check_themecreator("../DarkCode-Theme/core/darkcode.json")

    def tearDown(self):
        pass
