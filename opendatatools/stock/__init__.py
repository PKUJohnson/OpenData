# encoding: utf-8

from .stock_interface import *

__all__ = [ 'set_proxies',
            'get_index_list', 'get_index_component', 'get_rzrq_info', 'get_dividend',
            'get_quote', 'get_kline',
            'get_kline_multisymbol', 'get_kline_multidate', 'get_daily',
            'get_adj_factor', 'get_trade_detail', 'get_report_data',
            ]
