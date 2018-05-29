# encoding: utf-8

from opendatatools import aqi
from pyecharts import Geo

import pandas as pd

if __name__ == '__main__':

    df_aqi = aqi.get_daily_aqi('2018-05-27')
    df_aqi.to_csv("aqi_daily.csv")

    #df_aqi = pd.read_csv("aqi_daily.csv")

    # some city cannot by process by echart
    echart_unsupported_city = ["菏泽市", "襄阳市", "恩施州", "湘西州","阿坝州", "延边州",
                               "甘孜州", "凉山州", "黔西南州", "黔东南州", "黔南州", "普洱市", "楚雄州", "红河州",
                               "文山州", "西双版纳州", "大理州", "德宏州", "怒江州", "迪庆州", "昌都市", "山南市",
                               "林芝市", "临夏州", "甘南州", "海北州", "黄南州", "海南州", "果洛州", "玉树州", "海西州",
                               "昌吉州", "博州", "克州", "伊犁哈萨克州"]

    data = []
    for index, row in df_aqi.iterrows():
        city = row['city']
        aqi  = row['aqi']

        if city in echart_unsupported_city:
            continue

        data.append( (city, aqi) )

    geo = Geo("全国主要城市空气质量（AQI) - 2018-05-27", "数据来源于环保部网站",
              title_color="#fff",
              title_pos="center", width=1000,
              height=600, background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value,
            visual_range=[0, 200], maptype='china',visual_text_color="#fff",
            symbol_size=10, is_visualmap=True,
            label_formatter='{b}',  # 指定 label 只显示城市名
            tooltip_formatter='{c}',  # 格式：经度、纬度、值
            label_emphasis_textsize=15,  # 指定标签选中高亮时字体大小
            label_emphasis_pos='right'  # 指定标签选中高亮时字体位置
        )

    geo.render("aqi.html")

    geo
