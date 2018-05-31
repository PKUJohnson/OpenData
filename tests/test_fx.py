# encoding: utf-8
from opendatatools import fx
import unittest

class TestFx(unittest.TestCase):
    def test_get_his_cny_cpr(self):
        df,msg = fx.get_hist_cny_cpr()
        assert (len(df) >= 100)

        df, msg = fx.get_hist_cny_cpr('2017-01-01', '2018-05-01')
        assert(df == None)
