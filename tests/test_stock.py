# encoding: utf-8
from opendatatools import stock
import unittest

class TestStock(unittest.TestCase):
    def test_get_index_list(self):
        index_list = stock.get_index_list('SH')
        assert(len(index_list) > 0)

        index_list = stock.get_index_list('SZ')
        assert (len(index_list) > 0)

    def test_get_index_component(self):
        stock_list = stock.get_index_component('000001.SH')
        print(stock_list)
        assert(len(stock_list)>0)

        stock_list = stock.get_index_component('399001.SZ')
        print(stock_list)
        assert(len(stock_list)>0)