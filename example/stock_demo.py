# encoding: utf-8

from opendatatools import stock
import pandas as pd
from progressbar import ProgressBar

def get_pledge_info(market='SZ', date='2018-06-21'):
    df_total, df_detail = stock.get_pledge_info(market, date='2018-06-21')

    data = []
    progress_bar = ProgressBar().start(max_value=len(df_detail))
    for index, row in df_detail.iterrows():
        progress_bar.update(index + 1)
        symbol = str(row['证券代码']) + '.' + market
        if market == 'SZ':
            pledge_share = float(row['待购回无限售条件证券余量'].replace(',', '')) + float(row['待购回有限售条件证券余量'].replace(',', ''))
        else:
            pledge_share = float(row['待购回余量（股/份/张）'].replace(',', ''))

        df, msg = stock.get_shareholder_structure(symbol)
        if df is None:
            # print('error occurs on ', symbol)
            continue

        total_share = float(df[df.indicator == '总股本'].iloc[0, 1].replace(',', ''))
        tradable_share = float(df[df.indicator == '流通股'].iloc[0, 1].replace(',', ''))

        data.append({'total_share': total_share, 'tradable_share': tradable_share, 'pledge_share': pledge_share,
                     'pledge_ratio': pledge_share / total_share})

    df = pd.DataFrame(data)

    return df

if __name__ == '__main__':

    stock.set_proxies({"https" : "https://127.0.0.1:1080"})

    # 获取指数列表，market=SH/SZ/CSI
    #index_list = stock.get_index_list('CSI')
    #print(index_list)

    # 获取指数成份股数据
    #stock_list = stock.get_index_component('000050.SH')
    #print(stock_list)

    # 获取指数成份股数据
    #stock_list = stock.get_index_component('399300.SZ')
    #print(stock_list)

    # 获取指数成份股数据
    #stock_list = stock.get_index_component('000300.CSI')
    #print(stock_list)

    # 获取融资融券市场信息
    #df_total, df_detail = stock.get_rzrq_info(market = 'SH', date = '2018-06-14')
    #print(df_total)
    #print(df_detail)

    # 获取股权质押信息
    #df_total, df_detail = stock.get_pledge_info(market = 'SZ', date = '2018-06-20')
    #print(df_total)
    #print(df_detail)


    # 获取分红信息
    #df = stock.get_dividend('600000.SH')
    #print(df)

    # 获取实时行情
    #df, msg = stock.get_quote('600000.SH,000002.SZ')
    #print(df)
    #print(msg)

    # 获取分钟线
    #df, msg = stock.get_kline('000002.SZ', '2018-06-21', '1m')
    #print(df)
    #df, msg = stock.get_kline('000002.SZ', '2018-06-07', '1m')
    #print(df)
    #print(msg)

    #df, msg = stock.get_kline_multisymbol('000002.SZ,600000.SH', '2018-06-11', '1m')
    #print(df)
    #print(msg)

    #df, msg = stock.get_kline_multidate('600000.SH', start_date='2018-06-06', end_date='2018-06-07', period = '1m')

    # 获取日线
    #df, msg = stock.get_daily('600000.SH', start_date='2017-06-06', end_date='2018-06-07')
    #print(df)
    #print(msg)

    # 获取复权因子数据
    #df, msg = stock.get_adj_factor('600000.SH')
    #print(df)

    # 获取成交明细数据
    #df, msg = stock.get_trade_detail('600000.SH', trade_date='2018-06-07')
    #print(df)
    #print(msg)

    # 获取财务报表数据
    #df, msg = stock.get_report_data('000002.SZ', type='利润表')
    #df, msg = stock.get_report_data('600000.SH', type='fzb')
    #print(df[df['报告年度'] == '2017-12-31'].T)
    #print(msg)

    # 获取股本数据
    #df, msg = stock.get_shareholder_structure('002511.SZ')
    #print(df)

    # 获取股权质押数据
    #df_total, df_detail = stock.get_pledge_info(market='SZ', date='2018-06-21')
    #print(df_detail)

    #df_sz = stock.get_pledge_info('SZ', '2018-06-21')
    #print(df_sz)

    #df, msg = stock.get_hist_money_flow('000002.SZ')
    #print(df)

    df, msg = stock.get_realtime_money_flow('300033.SZ')
    print(df)

    #df, msg = stock.get_hist_money_flow_market()
    #print(df)

    #df, msg = stock.get_realtime_money_flow_market()
    #print(df)