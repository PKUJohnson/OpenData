# encoding: utf-8

from opendatatools import hedgefund


if __name__ == '__main__':
    hedgefund.set_proxies({"https" : "https://127.0.0.1:1080"})

    # 登录
    #user_info, msg = hedgefund.login('18612562791', 'a123456')

    # 加载数据
    #hedgefund.load_data()

    # 获取私募基金列表
    #df, msg = hedgefund.get_fund_list()
    #print(df)

    #df, msg = hedgefund.get_fund_nav('HF00004571')
    #print(df)


    #df, msg = hedgefund.get_barclay_data()
    #print(df)

    # 获取目前支持的指数（目前只配置了Barclay网站hedge fund模块指数）
    barclay_index_list, msg = hedgefund.get_barclay_index_list()
    print(barclay_index_list)

    # 获取指数数据
    # input为：hedgefund.get_barclay_index_list返回值中的index
    barclay_index_data, msg = hedgefund.get_barclay_data("Technology_Index")
    print(barclay_index_data)
