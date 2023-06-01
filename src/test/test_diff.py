import unittest

from src.common import handle_bybit, handle_dydx


class TestDiff(unittest.TestCase):

    def test_diff(self):
        handle_dydx(1.544)
        handle_bybit(1.543)
