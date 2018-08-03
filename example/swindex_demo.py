
from opendatatools import swindex

if __name__ == '__main__':
#    df, msg = swindex.get_index_list()
#    print(df)

#    df, msg = swindex.get_index_cons('801030')
#    print(df)

    df, msg = swindex.get_index_daily('805001')
    print(df)

#    df, msg = swindex.get_index_dailyindicator('805001', '2017-01-01', '2018-08-02')
#    print(df)