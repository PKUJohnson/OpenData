# encoding = 'utf-8'
from opendatatools.index import *

agent = YingWeiAgent()

time_map = {
    '1h' : 3600,
    '1d' : 86400,
    '1w' : 'week',
    '1m' : 'month',
    '3m' : '3-months',
    '6m' : '6-months',
    '1y' : '1-year',
    '5y' : '5-years',
    'max': 'max',
}


def get_index_data(symbol, freq, period):
    period = time_map[period]
    freq = time_map[freq]
    return agent.get_index_data(symbol=symbol, period=period, interval=freq)


def get_index_list():
    df, msg = agent.get_index_list()
    return df, msg

def set_proxies(proxies):
    return agent.set_proxies(proxies)




