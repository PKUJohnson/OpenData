# encoding: UTF-8

from opendatatools import shippingindex

if __name__ == "__main__":
    df, msg = shippingindex.get_index_list()
    print(df)

    for index, row in df.iterrows():
        code = row['index']
        df_data, msg = shippingindex.get_index_data(code)
        print(df_data)

