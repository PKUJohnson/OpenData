# encoding: utf-8

from opendatatools import aqi

# 获取某日全国各大城市的AQI数据
#df = aqi.get_daily_aqi('2018-01-01')

# 获取单个城市的AQI历史数据
# df = aqi.get_daily_aqi_onecity('淄博市')
# print(df)

#获取单个城市某日的AQI小时数据
#aqi_hour = aqi.get_hour_aqi_onecity('北京市', '2018-05-26')
#aqi_hour.set_index('time', inplace=True)
#print(aqi_hour)

#获取实时AQI小时数据
#aqi_hour = aqi.get_hour_aqi()
#print(aqi_hour)

aqi_recent = aqi.get_recent_daily_aqi_onecity('北京市')
print(aqi_recent)