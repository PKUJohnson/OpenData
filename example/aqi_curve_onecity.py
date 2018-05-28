# encoding: utf-8

from opendatatools import aqi
from pyecharts import Line

import pandas as pd

if __name__ == '__main__':
    df_aqi = aqi.get_daily_aqi_onecity('北京市')
    df_aqi.set_index('date', inplace=True)
    df_aqi.sort_index(ascending=True, inplace=True)

    df_aqi = df_aqi[df_aqi.index >= "2018-01-01"]

    axis_x = df_aqi.index
    axis_y = df_aqi['aqi']

    line = Line("北京AQI趋势图")
    line.add("aqi curve for beijing", axis_x, axis_y, mark_point=["average"])
    line.render("aqi_bj_curve.html")

