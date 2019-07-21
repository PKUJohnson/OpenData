# encoding: utf-8

from opendatatools import aqi2

# 获取城市列表
citylist = aqi2.get_city_list()
for city, value in citylist.items():
    print(city)
    # 获取某日全国各大城市的AQI数据
    df, msg = aqi2.get_hist_daily_aqi(city, "201907")
    print(df)
