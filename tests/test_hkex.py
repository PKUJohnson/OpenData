# encoding: utf-8
from opendatatools import hkex
import unittest

class TestHKEx(unittest.TestCase):

    # 获取陆港通 北向 持股 情况
    # 参数：市场SH/SZ，日期YYYY-MM-DD
    def test_get_lgt_share(self):
        df = hkex.get_lgt_share(market = 'SZ', date = '2018-05-28')
        assert(len(df) > 100)

        df = hkex.get_lgt_share(market='SH', date='2018-05-28')
        assert(len(df) > 100)

        df = hkex.get_lgt_share()
        assert(len(df) > 0)