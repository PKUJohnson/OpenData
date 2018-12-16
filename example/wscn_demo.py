# encoding: utf-8

from opendatatools import wscn

if __name__ == '__main__':
    wscn.login("18612562791", "xxxxxx")
    df, msg = wscn.get_xuangubao_theme()

    for index, row in df.iterrows():
        tid = int(row["plate_id"])
        df_data, msg2 = wscn.get_xuangubao_theme_event(tid)
        print(df_data["Title"])
