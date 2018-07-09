# encoding: utf-8

from opendatatools import movie

if __name__ == "__main__":
    print("")

    #df, msg = movie.get_boxoffice_rank()
    #print(df)

    #df, msg = movie.get_realtime_boxoffice()
    #print(df)

    df, msg = movie.get_recent_boxoffice(5)
    print(df)

    #df, msg = movie.get_monthly_boxoffice('2018-06-01')
    #print(df)

    #df, msg = movie.get_yearly_boxoffice(2013)
    #print(df)