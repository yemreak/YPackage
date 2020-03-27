import unittest

from .commands import check_googlesearch


class GoogleSearchTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_case(self):
        check_googlesearch("site:yemreak.com")

    def test_status_code(self):
        check_googlesearch("site:www.yemreak.com -sc 404")

    def test_exclude(self):
        check_googlesearch("site:lib.yemreak.com -ex knowed_url.txt")

    def test_output(self):
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

    def tearDown(self):
        pass
