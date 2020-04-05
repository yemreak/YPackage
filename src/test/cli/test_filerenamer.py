import pytest

from .commands import check_filerenamer


def test_help():
    with pytest.raises(SystemExit, match="0"):
        check_filerenamer(['-h'])


def test_unknown():
    with pytest.raises(SystemExit, match="2"):
        check_filerenamer(['-ü'])


def test_string():
    check_filerenamer([".", "-p", "read", "-t", "me"])


def test_debug():
    check_filerenamer(". -p \"\" -t \"\" -d")


def test_silent():
    check_filerenamer(". -p \"\" -t \"\" -d")


def test_dir_mode():
    check_filerenamer(". -p \"\" -t \"\" -dm")


def test_case_sensitive():
    check_filerenamer(". -p \"\" -t \"\" -cs")


def test_regex():
    check_filerenamer(". -p \"(re)(ad)\" -t \"$2$1\"")


def test_all():
    check_filerenamer(". -p \"\" -t \"\" -dm -d -cs")
