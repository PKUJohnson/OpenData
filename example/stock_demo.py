# encoding: utf-8

from opendatatools import stock

if __name__ == '__main__':

    #index_list = stock.get_index_list('CSI')
    #print(index_list)

    #stock_list = stock.get_index_component('000050.SH')
    #print(stock_list)

    #stock_list = stock.get_index_component('399300.SZ')
    #print(stock_list)

    #stock_list = stock.get_index_component('000300.CSI')
    #print(stock_list)

    df_total, df_detail = stock.get_rzrq_info(market = 'SZ', date = '20180529')
    print(df_total)
    print(df_detail)