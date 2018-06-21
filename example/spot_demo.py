# encoding: utf-8

from opendatatools import spot
import time

if __name__ == '__main__':

    df_indicator = spot.get_commodity_spot_indicator()
    print(df_indicator)

    for index, row in df_indicator.iterrows():
        id   = row['indicator_id']
        name = row['indicator_name']

        df, msg = spot.get_commodity_spot_indicator_data(id)
        if df is None:
            print('error occurs on %s, %s' % (name, msg))
            continue

        print(df)
        time.sleep(2)



