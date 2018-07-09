# encoding: utf-8

from opendatatools import fx

if __name__ == '__main__':
    # 人民币汇率中间价历史数据
    df,msg = fx.get_hist_cny_cpr()
    print(df)

    # shibor历史数据
    #df, msg = fx.get_his_shibor()
    #print(df)

    # shibor实时数据
    #df = fx.get_realtime_shibor()
    #print(df)

    # 人民币汇率最新数据
    #df = fx.get_cny_spot_price()
    #print(df)