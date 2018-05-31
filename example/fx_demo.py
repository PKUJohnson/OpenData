# encoding: utf-8

from opendatatools import fx

if __name__ == '__main__':
    #df,msg = fx.get_hist_cny_cpr()
    #print(df)

    #df, msg = fx.get_his_shibor()
    #print(df)

    #df = fx.get_realtime_shibor()
    #print(df)

    df = fx.get_cny_spot_price()
    print(df)