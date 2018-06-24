#encoding: utf - 8

from opendatatools import usstock

if __name__ == '__main__':
    usstock.set_proxies({"https": "https://127.0.0.1:1080"})

    #df, msg = usstock.get_symbols()
    #print(df)

    #df, msg = usstock.get_daily('AAPL')
    #print(df)

    #df, msg = usstock.get_dividend('AAPL')
    #print(df)

    #df, msg = usstock.get_split('AAPL')
    #print(df)