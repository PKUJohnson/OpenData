# encoding: UTF-8

from opendatatools import sns

if __name__ == '__main__':
    df, msg = sns.get_weibo_index('贸易战', '1month')
    print(df)
