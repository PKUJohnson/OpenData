# encoding: utf-8

from opendatatools import aqi2

# 获取某日全国各大城市的AQI数据
df, msg = aqi2.get_hist_daily_aqi("上海市", "201805")
print(df)
print(msg)
