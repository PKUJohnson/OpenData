# encoding: utf-8

import datetime

from .stock_agent import SHExAgent, SZExAgent, CSIAgent, XueqiuAgent, SinaAgent, CNInfoAgent, EastMoneyAgent
from opendatatools.common import get_current_day

shex_agent   = SHExAgent()
szex_agent   = SZExAgent()
csi_agent    = CSIAgent()
xq_agent     = XueqiuAgent()
sina_agent   = SinaAgent()
cninfo_agent = CNInfoAgent()
eastmoney_agent = EastMoneyAgent()

xq_count_map = {
    '1m': -240,
    '5m': -48,
    '15m': -16,
    '30m': -8,
    '60m': -4,
    '1d' : -1,
}

bar_span_map = {
    '1m'  : 1,
    '5m'  : 5,
    '15m' : 15,
    '30m' : 30,
    '60m' : 60,
}


def make_index(period, trade_date):
    bar_index = list()
    span = bar_span_map[period]
    dt = datetime.datetime.strptime(trade_date,'%Y-%m-%d')
    bar_index.extend(pd.DatetimeIndex(start="%s 09:30:00" % trade_date, end="%s 11:30:00" % trade_date, freq='%sT' % span)[1:])
    bar_index.extend(pd.DatetimeIndex(start="%s 13:00:00" % trade_date, end="%s 15:00:00" % trade_date, freq='%sT' % span)[1:])
    return bar_index

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
        date = get_current_day(format = '%Y-%m-%d')

    if market == 'SH':
        return shex_agent.get_rzrq_info(date)

    if market == 'SZ':
        return szex_agent.get_rzrq_info(date)

    return None, None

def get_pledge_info(market='SH', date = None):
    if date is None:
        date = get_current_day(format = '%Y-%m-%d')

    if market == 'SH':
        return shex_agent.get_pledge_info(date)

    if market == 'SZ':
        return szex_agent.get_pledge_info(date)

    return None, None

def get_dividend(symbol):
    temp = symbol.split(".")

    if len(temp) == 2:
        market = temp[1]
        code = temp[0]
        if market == 'SH':
            return shex_agent.get_dividend(code)

def get_quote(symbols):
    return xq_agent.get_quote(symbols)

def fill_df(df, period, trade_date, symbol):
    df.index = df['time']
    index = make_index(period, trade_date)
    df_new = pd.DataFrame(index=index, columns=['last'])
    df_new['last'] = df['last']
    df_new.fillna(method='ffill', inplace=True)
    df_new['high'] = df['high']
    df_new['low'] = df['low']
    df_new['open'] = df['open']
    df_new.fillna(method='ffill', axis=1, inplace=True)
    df_new['change'] = df['change']
    df_new['percent'] = df['percent']
    df_new['symbol'] = symbol
    df_new['turnover_rate'] = df['turnover_rate']
    df_new['volume'] = df['volume']
    df_new['time'] = df_new.index
    df_new.fillna(0, inplace=True)
    return df_new

# period 1m, 5m, 15m, 30m, 60m
def get_kline(symbol, trade_date, period):
    curr_date = datetime.datetime.strptime(trade_date, '%Y-%m-%d')
    next_date = datetime.datetime.strptime(trade_date, '%Y-%m-%d') + datetime.timedelta(days=1)
    timestamp = next_date.timestamp()

    timestamp = int ( timestamp * 1000)
    df, msg = xq_agent.get_kline(symbol, timestamp, period, xq_count_map[period])
    if df is None:
        return df, msg

    df = df[(df.time < next_date) & (df.time >= curr_date)]
    if len(df) < abs(xq_count_map[period]):
        df_new = fill_df(df, period, trade_date, symbol)
        return df_new, ''
    else:
        return df, ''

def get_kline_multisymbol(symbols, trade_date, period):

    symbol_list = symbols.split(',')

    timestamp = datetime.datetime.strptime(trade_date, '%Y-%m-%d').timestamp()
    timestamp = int ( timestamp * 1000)
    df, msg = xq_agent.get_kline_multisymbol(symbol_list, timestamp, period, xq_count_map[period])
    next_date = datetime.datetime.strptime(trade_date, '%Y-%m-%d') + datetime.timedelta(days=1)
    if df is None:
        return df, msg

    df = df[df.time < next_date]
    gp = df.groupby('symbol')
    df_list = list()
    for symbol, df_item in gp:
        if len(df_item) < xq_count_map[period]:
            df_list.append(fill_df(df_item, period, trade_date, symbol))
        else:
            df_list(df_item)

    return pd.concat(df_list), ''

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

def get_adj_factor(symbol):
    return sina_agent.get_adj_factor(symbol)

def get_trade_detail(symbol, trade_date):
    return sina_agent.get_trade_detail(symbol, trade_date)

def get_report_data(symbol='600000.SH', type='资产负债表'):

    dict_type = {
        '利润表'    : 'lrb',
        '资产负债表' : 'fzb',
        '现金流量表' : 'llb',
    }

    if type not in dict_type:
        return None, 'type输入错误，可以输入 %s' % dict_type.keys()

    data = symbol.split(sep='.')
    market = data[1].lower()
    code = data[0]
    return cninfo_agent.get_report_data(market, code, dict_type[type])

def get_shareholder_structure(symbol='600000.SH'):
    data = symbol.split(sep='.')
    market = data[1].lower()
    code = data[0]
    return cninfo_agent.get_shareholder_structure(market, code)

# 单位：百万元
def get_hist_money_flow(symbol):
    data = symbol.split(sep='.')
    market = data[1]
    if market == 'SH':
        marketnum = '1'
    else:
        marketnum = '2'
    code = data[0]+marketnum
    return eastmoney_agent.get_hist_money_flow(code)

# 单位：万元
def get_realtime_money_flow(symbol):
    data = symbol.split(sep='.')
    market = data[1]
    if market == 'SH':
        marketnum = '1'
    else:
        marketnum = '2'
    code = data[0]+marketnum
    return eastmoney_agent.get_realtime_money_flow(code)

# 单位：亿元
def get_realtime_money_flow_market():
    return eastmoney_agent.get_realtime_money_flow_market()

def get_hist_money_flow_market():
    return eastmoney_agent.get_hist_money_flow_market()
def get_allstock_flow():
    return eastmoney_agent.get_allstock_flow()
