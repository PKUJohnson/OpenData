
from opendatatools import swindex

if __name__ == '__main__':
    #df, msg = swindex.get_index_list()
    #print(df)

    #df, msg = swindex.get_index_cons('801030')
    #print(df)

    df, msg = swindex.get_index_daily('801003', '2000-01-01', '2018-11-02')
    print(df)

	# freq 'D', 'W', 'M'
    #df, msg = swindex.get_index_dailyindicator('801040', '2000-01-01', '2018-11-02', 'W')
    #print(df)
