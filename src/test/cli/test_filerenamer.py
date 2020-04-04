import unittest
from .commands import check_filerenamer


class FileRenamerTest(unittest.TestCase):

    def test_help(self):
        with self.assertRaises(SystemExit) as cm:
            check_filerenamer(['-h'])
            self.assertEqual(cm.exception.code, 0)

    def test_unknown(self):
        with self.assertRaises(SystemExit) as cm:
            check_filerenamer(['-ü'])
            self.assertEqual(cm.exception.code, 2)

    def test_string(self):
        check_filerenamer([".", "-p", "read", "-t", "me"])

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
