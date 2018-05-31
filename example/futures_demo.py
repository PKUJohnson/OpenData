# encoding: utf-8

from opendatatools import futures

if __name__ == '__main__':
    df, msg = futures.get_trade_rank(market = 'CFE')
    print(df)
