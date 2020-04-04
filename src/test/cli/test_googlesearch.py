import unittest

from .commands import check_googlesearch


class GoogleSearchTest(unittest.TestCase):

    def test_help(self):
        with self.assertRaises(SystemExit) as cm:
            check_googlesearch(['-h'])
            self.assertEqual(cm.exception.code, 0)

    def test_unknown(self):
        with self.assertRaises(SystemExit) as cm:
            check_googlesearch(['-ü'])
            self.assertEqual(cm.exception.code, 2)

    def test_simple_case(self):
        return
        check_googlesearch("site:yemreak.com")

    def test_status_code(self):
        return
        check_googlesearch("site:www.yemreak.com -sc 404")

    def test_exclude(self):
        return
        check_googlesearch("site:lib.yemreak.com -ex known_urls.txt")

    def test_output(self):
        return
        check_googlesearch(
            ""
            + "site:ai.yemreak.com"
            + "site:windows.yemreak.com"
            + "site:linux.yemreak.com"
            + "site:ds.yemreak.com"
            + "site:java.yemreak.com"
            + "site:web.yemreak.com"
            + "site:android.yemreak.com"
            + "site:iuce.yemreak.com"
            + "-sc 404 -o wrong_urls.txt"
        )
