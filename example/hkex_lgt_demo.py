# encoding: utf-8

from opendatatools import hkex
import pandas as pd

if __name__ == '__main__':
    df = hkex.get_lgt_share(market = 'SH')
    print(df)
