import unittest

from .commands import check_gitbook


class IntegrationTest(unittest.TestCase):

    def test_help(self):
        with self.assertRaises(SystemExit) as cm:
            check_gitbook(['-h'])
            self.assertEqual(cm.exception.code, 0)

    def test_unknown(self):
        with self.assertRaises(SystemExit) as cm:
            check_gitbook(['-ü'])
            self.assertEqual(cm.exception.code, 2)

    def test_dot(self):
        check_gitbook(".")

    def test_path(self):
        check_gitbook("../YLib")

    def test_recreate(self):
        check_gitbook("../YLib -r")

    def test_generate(self):
        check_gitbook("../YLib -g")

    def test_multipath(self):
        check_gitbook("../YLib ../YPython")

    def test_multipath_debug(self):
        check_gitbook("../YLib ../YPython -d")

    def test_wildcard(self):
        check_gitbook("../*")

    def test_changelog(self):
        check_gitbook(
            "../YLib -c -ru https://github.com/YEmreAk/YLib"
        )

    def test_base_integration(self):
        check_gitbook("ygitbookintegration ../YLib -c")
