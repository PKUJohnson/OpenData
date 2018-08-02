
from opendatatools import swindex

if __name__ == '__main__':
    df, msg = swindex.get_index_list()
    print(df)

    df, msg = swindex.get_index_cons('801030')
    print(df)

    df, msg = swindex.get_index_daily('801030')
    print(df)

    df, msg = swindex.get_index_dailyindicator('801030', '2018-01-01', '2018-08-02')
    print(df)