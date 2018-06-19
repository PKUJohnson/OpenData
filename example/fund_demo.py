# encoding: utf-8

from opendatatools import fund


if __name__ == '__main__':

    # 获取基金公司列表
    #df, msg = fund.get_fund_company()
    #df.sort_values('companyid', inplace=True)
    #print(df)

    '''
    80000220        南方基金
    80000221        富国基金
    80000222        华夏基金
    '''

    # 根据基金公司获取基金列表
    #df, msg = fund.get_fundlist_by_company('80000222')
    #df.sort_values('fundcode', inplace=True)
    #print(df)
    '''
    fundcode    fundname          pingyin       nav         accu_nav    date
    000001      华夏成长          HXCZ          1.1010      3.5120      2018-06-15
    000011      华夏大盘精选      HXDPJX        13.9360     18.1160     2018-06-15
    000014      华夏聚利债券      HXJLZQ        1.1230      1.1230      2018-06-15
    000015      华夏纯债债券A     HXCZZQA       1.1990      1.2290      2018-06-15
    000016      华夏纯债债券C     HXCZZQC       1.1730      1.2030      2018-06-15
    '''

    # 获取基金类型列表
    # type_list= fund.get_fund_type()
    # print(type_list)
    # ['全部开放基金',
    #  '股票型基金', '混合型基金', '债券型基金', '指数型基金', 'ETF联接基金', 'LOF基金', '分级基金', 'FOF基金',
    #  '理财基金', '分级A', '货币基金']

    # 根据类型获取基金信息
    # df, msg = fund.get_fundlist_by_type('分级A')
    # df.sort_values('fundcode', inplace=True)
    # print(df)
    '''
    fundcode   fundname                   pingyin             nav       accu_nav        date  
    000008     嘉实中证500ETF联接         JSZZ500ETFLJ        1.5245     1.5245       2018-06-15   
    000042     中证财通可持续发展100指数A  ZZCTKCXFZ100ZSA     1.6741     1.6741       2018-06-15   
    000051     华夏沪深300ETF联接A        HXHS300ETFLJA       1.2230     1.2230       2018-06-15   
    000059     国联安中证医药100          GLAZZYY100          1.0424     1.6024        2018-06-15   
    '''

    # 根据基金代码，获取基金历史净值
    # date nav1 nav2
    # 对于‘理财基金’、‘货币基金’，nav1, nav2 分别表示万分收益和7日年华收益
    # 对于其他类型的基金，nav1, nav2分别表示 单位净值 和 累计净值
    # 华夏大盘
    # df, msg = fund.get_fund_nav('000011')
    # print(df)

    # 余额宝
    # df, msg = fund.get_fund_nav('000198')
    # print(df)

    # 获取全部的基金列表（这个运行会很慢）
    df, msg = fund.get_fund_list()
    print(df)

