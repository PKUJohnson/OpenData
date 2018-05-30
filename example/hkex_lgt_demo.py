# encoding: utf-8

from opendatatools import hkex
import pandas as pd

if __name__ == '__main__':
    # 获取陆港通 北向 持股 情况
    # 参数：市场SH/SZ，日期YYYY-MM-DD
    df = hkex.get_lgt_share(market = 'SZ', date = '2018-05-28')
    print(df)
