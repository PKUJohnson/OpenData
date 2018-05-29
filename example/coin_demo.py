# encoding: utf-8

from opendatatools import coin

def test():

    #data, msg = coin.get_coin_list()
    #print(data)
    #print(msg)

    snap, df, msg = coin.get_coin_snapshot('BTC', 'USD')
    print(snap)
    print(df)
    print(msg)

    #data, msg = coin.get_coin_price('BTC', 'USD,EUR', 'CCCAGG')
    #print(data)
    #print(msg)

    #data, msg = coin.get_his_min('BTC', 'USD', 'Bitfinex')
    #data, msg = coin.get_his_hour('BTC', 'USD', 'Bitfinex')
    #data, msg = coin.get_his_day('BTC', 'USD', 'Bitfinex')
    #print(data)
    #print(msg)

if __name__ == '__main__':
    coin.set_proxies({"https" : "https://127.0.0.1:1080"})
    test()