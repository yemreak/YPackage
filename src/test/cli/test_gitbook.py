import pytest

from .commands import check_gitbook


def test_help():
    with pytest.raises(SystemExit, match="0"):
        check_gitbook(['-h'])


def test_unknown():
    with pytest.raises(SystemExit, match="2"):
        check_gitbook(['-ü'])


def test_dot():
    check_gitbook(".")


def test_path():
    check_gitbook("../YLib")


def test_recreate():
    check_gitbook("../YLib -r")


def test_generate():
    check_gitbook("../YLib -g")


def test_multipath():
    check_gitbook("../YLib ../YPython")


def test_multipath_debug():
    check_gitbook("../YLib ../YPython -d")


def test_wildcard():
    check_gitbook("../*")


def test_changelog():
    check_gitbook(
        "../YLib -c -ru https://github.com/YEmreAk/YLib"
    )


def test_base_integration():
    check_gitbook("ygitbookintegration ../YLib -c")
