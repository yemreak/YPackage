import unittest

from .commands import check_filerenamer


class FileRenamerTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_string(self):
        check_filerenamer(". -p read -t mee")

    def test_regex(self):
        check_filerenamer(". -p \"(re)(ad)\" -t \"$2$1\"")

    def tearDown(self):
        pass
