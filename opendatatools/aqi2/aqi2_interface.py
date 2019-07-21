# encoding: UTF-8

from .aqi2_agent import AQIStudyAgent

aqistudy_agent = AQIStudyAgent()

def set_proxies(proxies):
    aqistudy_agent.set_proxies(proxies)

def get_city_list():
    return aqistudy_agent.get_city_list()

def get_hist_daily_aqi(city, month):
    return aqistudy_agent.get_hist_daily_aqi(city, month)

