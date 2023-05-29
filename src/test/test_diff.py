import unittest

from src.common import handle_bybit, handle_dydx


class TestDiff(unittest.TestCase):

    def test_diff(self):
        handle_bybit(1.543)
        handle_dydx(1.544)
