# encoding: utf-8
from opendatatools import futures
import unittest

class TestFutures(unittest.TestCase):
    def test_get_trade_rank(self):
        markets = ['SHF', 'CZC', 'DCE', 'CFE']
        for market in markets:
            df,msg = futures.get_trade_rank(market)
            assert (len(df) >= 100)
