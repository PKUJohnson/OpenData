# encoding: utf-8

from opendatatools import hsgt

if __name__ == '__main__':
    hsgt.set_proxies({"https" : "https://127.0.0.1:1080"})

    # 沪港通实时资金流向
    #df, msg = hsgt.get_realtime_moneyflow()
    #print(df)

    # 沪港通历史资金流向
    #df, msg = hsgt.get_hist_moneyflow()
    #print(df.tail(1))

    # 沪港通历史交易和资金统计
    #df, msg = hsgt.get_his_tradestat(2)
    #print(df.tail(2))

    # 实时A/H 比价
    #df, msg = hsgt.get_ah_compare()
    #print(df.sort_values('ah_ratio'))

    # 获取陆港通 北向 持股 情况
    # 参数：市场SH/SZ，日期YYYY-MM-DD
    df = hsgt.get_lgt_share(market = 'SZ', date = '2018-05-28')
    print(df)

    pass