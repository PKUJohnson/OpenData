# encoding: utf-8

from .coin_agent import CoinAgent

coin_agent = CoinAgent()

def set_proxies(proxies):
    coin_agent.set_proxies(proxies)

# get all coin list
def get_coin_list():
    return coin_agent.get_coin_list()

def get_coin_snapshot(fsym, tsym):
    return coin_agent.get_coin_snapshot(fsym, tsym)

def get_coin_price(fsym, tsym, exchange = "CCCAGG"):
    return coin_agent.get_coin_price(fsym, tsym, exchange)

def get_his_min(fsym, tsym, exchange = "CCCAGG", limit = 2000):
    return coin_agent.get_his_min(fsym, tsym, exchange, limit)

def get_his_hour(fsym, tsym, exchange = "CCCAGG", limit = 2000):
    return coin_agent.get_his_hour(fsym, tsym, exchange, limit)

def get_his_day(fsym, tsym, exchange = "CCCAGG", limit = 2000):
    return coin_agent.get_his_day(fsym, tsym, exchange, limit)
