import pytest

from .commands import check_googledrive


def test_help():
    with pytest.raises(SystemExit, match="0"):
        check_googledrive(['-h'])


def test_unknown():
    with pytest.raises(SystemExit, match="2"):
        check_googledrive(['-ü'])


def test_simple_case():
    check_googledrive(
        '"https://drive.google.com/open?id=1H6W_NiMSKJqAbeQfJC0pABiCq6j-klEb"')


def test_reverse_case():
    check_googledrive(
        '"https://drive.google.com/uc?id=1H6W_NiMSKJqAbeQfJC0pABiCq6j-klEb" - r')


def test_id():
    check_googledrive(
        '"https://drive.google.com/uc?id=1H6W_NiMSKJqAbeQfJC0pABiCq6j-klEb"')
