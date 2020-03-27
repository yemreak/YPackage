import unittest

from .commands import check_googledrive


class GoogleDriveTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_case(self):
        check_googledrive('"https://drive.google.com/open?id=1H6W_NiMSKJqAbeQfJC0pABiCq6j-klEb"')

    def test_reverse_case(self):
        check_googledrive('"https://drive.google.com/uc?id=1H6W_NiMSKJqAbeQfJC0pABiCq6j-klEb" - r')

    def test_id(self):
        check_googledrive('"https://drive.google.com/uc?id=1H6W_NiMSKJqAbeQfJC0pABiCq6j-klEb"')

    def tearDown(self):
        pass
