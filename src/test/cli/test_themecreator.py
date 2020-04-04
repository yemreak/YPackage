import pytest

from .commands import check_themecreator


def test_help():
    with pytest.raises(SystemExit, match="0"):
        check_themecreator(['-h'])


def test_unknown():
    with pytest.raises(SystemExit, match="2"):
        check_themecreator(['-ü'])


def test_simple_case():
    check_themecreator("../DarkCode-Theme/core/settings.json")


def test_error():
    with pytest.raises(SystemExit, match="1"):
        check_themecreator("../DarkCode-Theme/core/darkcode.json")
