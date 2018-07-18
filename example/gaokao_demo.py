# encoding: utf-8

from opendatatools import gaokao


if __name__ == '__main__':

    # 查询学校列表/模糊查询
    #df, msg = gaokao.get_school_list('北京')

    # 获取学校基本信息
    #df, msg = gaokao.get_school_baseinfo('北京大学')

    # 获取专业信息
    #df, msg = gaokao.get_school_major('北京大学')

    # 获取录取分数线信息
    #df, msg = gaokao.get_school_score('北京大学')

    # 获取省录取分数线
    df, msg = gaokao.get_batch_score('北京', '理科')

    print(df)
