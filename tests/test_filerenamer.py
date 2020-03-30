import unittest

from .commands import check_filerenamer


class FileRenamerTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_help(self):
        check_filerenamer("-h")

    def test_string(self):
        check_filerenamer(". -p read -t mee")

    def test_debug(self):
        check_filerenamer(". -p \"\" -t \"\" -d")

    def test_silent(self):
        check_filerenamer(". -p \"\" -t \"\" -d")

    def test_dir_mode(self):
        check_filerenamer(". -p \"\" -t \"\" -dm")

    def test_case_sensitive(self):
        check_filerenamer(". -p \"\" -t \"\" -cs")

    def test_regex(self):
        check_filerenamer(". -p \"(re)(ad)\" -t \"$2$1\"")

    def test_all(self):
        check_filerenamer(". -p \"\" -t \"\" -dm -d -cs")

    def tearDown(self):
        pass
