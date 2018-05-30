# encoding: utf-8
from opendatatools import aqi
import unittest

class TestAQI(unittest.TestCase):

    # 获取某日全国各大城市的AQI数据
    def test_get_daily_aqi(self):
        df = aqi.get_daily_aqi('2018-01-01')
        assert(len(df)>0)

    # 获取单个城市的AQI历史数据
    def test_get_daily_aqi_onecity(self):
        df = aqi.get_daily_aqi_onecity('北京市')
        assert(len(df)>0)

    # 获取单个城市某日的AQI小时数据
    def test_get_hour_aqi_onecity(self):
        aqi_hour = aqi.get_hour_aqi_onecity('北京市', '2018-05-26')
        assert(len(aqi_hour)>0)

    #获取实时AQI小时数据
    def test_get_hour_aqi(self):
        aqi_hour = aqi.get_hour_aqi()
        assert (len(aqi_hour) > 0)

