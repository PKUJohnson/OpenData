
# encoding: utf-8

from opendatatools import nhindex

if __name__ == '__main__':
    df, msg = nhindex.get_index_list()
    print(df)

    df, msg = nhindex.get_index_daily('NHCI')
    print(df)

    df, msg = nhindex.get_index_snapshot()
    print(df)

    df, msg = nhindex.get_index_weight()
    print(df)
