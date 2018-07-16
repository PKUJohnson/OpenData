# encoding: utf-8

from opendatatools import hedgefund


if __name__ == '__main__':
    hedgefund.set_proxies({"https" : "https://127.0.0.1:1080"})

    # 登录
    user_info, msg = hedgefund.login('18612562791', 'a123456')

    # 加载数据
    hedgefund.load_data()

    # 获取私募基金列表
    df, msg = hedgefund.get_fund_list()
    print(df)

    df, msg = hedgefund.get_fund_nav('HF000025PG')
    print(df)