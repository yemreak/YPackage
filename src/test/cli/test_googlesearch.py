import pytest

from .commands import check_googlesearch


def test_help():
    with pytest.raises(SystemExit, match="0"):
        check_googlesearch(['-h'])


def test_unknown():
    with pytest.raises(SystemExit, match="2"):
        check_googlesearch(['-ü'])


def test_simple_case():
    return
    check_googlesearch("site:yemreak.com")


def test_status_code():
    return
    check_googlesearch("site:www.yemreak.com -sc 404")


def test_exclude():
    return
    check_googlesearch("site:lib.yemreak.com -ex known_urls.txt")


def test_output():
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
