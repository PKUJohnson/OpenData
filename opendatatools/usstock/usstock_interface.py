# encoding: utf-8

from .usstock_agent import USStockAgent

usstock_agent = USStockAgent()

def set_proxies(proxies):
    return usstock_agent.set_proxies(proxies)

def get_symbols():
    return usstock_agent.get_symbols()

def get_daily(symbol):
    return usstock_agent.get_daily(symbol)

def get_dividend(symbol):
    return usstock_agent.get_dividend(symbol)

def get_split(symbol):
    return usstock_agent.get_split(symbol)