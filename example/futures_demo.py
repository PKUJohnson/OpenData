# encoding: utf-8

from opendatatools import futures

if __name__ == '__main__':

    markets = ['SHF', 'CZC', 'DCE', 'CFE']
    for market in markets:
        df, msg = futures.get_trade_rank(market, date='2018-05-30')
        print(df)

