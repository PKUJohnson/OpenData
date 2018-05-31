# encoding: utf-8

from opendatatools import stock

if __name__ == '__main__':

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
    #df_total, df_detail = stock.get_rzrq_info(market = 'SH', date = '20040529')
    #print(df_total)
    #print(df_detail)

    # 获取分红信息
    df = stock.get_dividend('600000.SH')
    print(df)