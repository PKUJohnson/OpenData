
# encoding: utf-8

from opendatatools import index

if __name__ == '__main__':
    index.set_proxies({"https" : "https://127.0.0.1:1080"})

    # 全球股票指数列表
    df, msg = index.get_index_list()
    print(df)

    # 获取指数数据
    # 时间：1h、1d、1w、1m、3m、6m、1y、5y、max
    df, msd = index.get_index_data(symbol='SSEC', freq='1d', period='max')
    print(df)