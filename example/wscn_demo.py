# encoding: utf-8

from opendatatools import wscn

if __name__ == '__main__':
    wscn.login("18612562791", "xxxxxx")
    #df, msg = wscn.get_xuangubao_theme()
    df, msg = wscn.get_xuangubao_theme_stock("16843401")
    print(df)


