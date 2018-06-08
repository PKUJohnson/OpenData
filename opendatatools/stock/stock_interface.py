# encoding: utf-8

import datetime

from .stock_agent import SHExAgent, SZExAgent, CSIAgent, XueqiuAgent
from opendatatools.common import get_current_day

shex_agent = SHExAgent()
szex_agent = SZExAgent()
csi_agent  = CSIAgent()
xq_agent   = XueqiuAgent()

xq_count_map = {
    '1m': 240,
    '5m': 48,
    '15m': 16,
    '30m': 8,
    '60m': 4,
    '1d' : 1,
}

def set_proxies(proxies):
    shex_agent.set_proxies(proxies)
    szex_agent.set_proxies(proxies)
    csi_agent.set_proxies(proxies)
    xq_agent.set_proxies(proxies)

def get_index_list(market='SH'):
    if market == 'SH':
        return shex_agent.get_index_list()

    if market == 'SZ':
        return szex_agent.get_index_list()

    if market == 'CSI':
        return csi_agent.get_index_list()

def get_index_component(symbol):
    temp = symbol.split(".")

    if len(temp) == 2:
        market = temp[1]
        index  = temp[0]
        if market == 'SH':
            return shex_agent.get_index_component(index)
        elif market == 'SZ':
            return szex_agent.get_index_component(index)
        elif market == 'CSI':
            return csi_agent.get_index_component(index)
        else:
            return None
    else:
        return None

def get_rzrq_info(market='SH', date = None):
    if date is None:
        date = get_current_day(format = '%Y%m%d')

    if market == 'SH':
        return shex_agent.get_rzrq_info(date)

    if market == 'SZ':
        return szex_agent.get_rzrq_info(date)

    return None, None

def get_dividend(symbol):
    temp = symbol.split(".")

    if len(temp) == 2:
        market = temp[1]
        code = temp[0]
        if market == 'SH':
            return shex_agent.get_dividend(code)

def get_quote(symbols):
    return xq_agent.quote(symbols)

# period 1m, 5m, 15m, 30m, 60m
def get_kline(symbol, trade_date, period):
    timestamp = datetime.datetime.strptime(trade_date, '%Y-%m-%d').timestamp()
    timestamp = int ( timestamp * 1000)
    return xq_agent.get_kline(symbol, timestamp, period, xq_count_map[period])

def get_kline_multisymbol(symbols, trade_date, period):

    symbol_list = symbols.split(',')

    timestamp = datetime.datetime.strptime(trade_date, '%Y-%m-%d').timestamp()
    timestamp = int ( timestamp * 1000)
    return xq_agent.get_kline_multisymbol(symbol_list, timestamp, period, xq_count_map[period])

def get_timestamp_list(start_date, end_date):
    timestamp_list = []
    curr_date = start_date
    while curr_date <= end_date:
        curr_datetime = datetime.datetime.strptime(curr_date, '%Y-%m-%d')
        timestamp = curr_datetime.timestamp()
        timestamp_list.append(int(timestamp * 1000))
        next_time = curr_datetime + datetime.timedelta(days=1)
        curr_date = datetime.datetime.strftime(next_time, '%Y-%m-%d')

    return timestamp_list

def get_kline_multidate(symbol, start_date, end_date, period):
    timestamp_list = get_timestamp_list(start_date, end_date)
    return xq_agent.get_kline_multitimestamp(symbol, timestamp_list, period, xq_count_map[period])

import pandas as pd
def get_daily(symbol, start_date, end_date):
    curr_date = start_date
    df_result = []
    while curr_date <= end_date:
        curr_datetime = datetime.datetime.strptime(curr_date, '%Y-%m-%d')
        next_time = curr_datetime + datetime.timedelta(days=100)
        next_date = datetime.datetime.strftime(next_time, '%Y-%m-%d')

        timestamp = curr_datetime.timestamp()
        df, msg = xq_agent.get_kline(symbol, int(timestamp*1000), 'day', 100)
        if df is not None:
            df_result.append(df[df['time']<next_time])

        curr_date = next_date

    if len(df_result) > 0:
        df = pd.concat(df_result)
        df = df[(df['time'] >= start_date) & (df['time'] <= end_date) ]
        return df, ''
    else:
        return None, '没有获取到数据'

