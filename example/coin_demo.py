# encoding: utf-8

from opendatatools import coin

def test():

    # 获取数字货币的信息
    # 从这里可以获取到数字货币的symbol，比如比特币BTC，以太币ETH
    data, msg = coin.get_coin_list()

    # 获取数字货币行情快照
    # 参数：目标币，支付币
    snap, df, msg = coin.get_coin_snapshot('BTC', 'USD')

    # 获取数字货币的实时行情
    # 参数：目标币，支付币，交易所（支付币可以是多个，结果返回多个）
    data, msg = coin.get_coin_price('BTC', 'USD,EUR', 'Bitfinex')

    # 获取分钟线，小时线，日线
    # 参数：目标币，支付币，交易所
    data, msg = coin.get_his_min('BTC', 'USD', 'Bitfinex')
    data, msg = coin.get_his_hour('BTC', 'USD', 'Bitfinex')
    data, msg = coin.get_his_day('BTC', 'USD', 'Bitfinex')

if __name__ == '__main__':
    coin.set_proxies({"https" : "https://127.0.0.1:1080"})
    test()