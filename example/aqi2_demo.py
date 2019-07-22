# encoding: utf-8

from opendatatools import aqi2

# 获取城市列表
citylist = aqi2.get_city_list()
print(citylist)

# 获取某日全国各大城市的AQI数据
for city in ["北京", "上海", "三亚", "深圳"]:
    print(city)
    df, msg = aqi2.get_hist_daily_aqi(city, "2019-07-01", "2019-07-22")
    print(df)

    df, msg = aqi2.get_daily_hour_aqi(city, "2019-07-22")
    print(df)

