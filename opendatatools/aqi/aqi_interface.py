# encoding: UTF-8

from .aqi_agent import AQIAgent

aqi_agent = AQIAgent()

def get_hour_aqi_onecity(city, date):
    return aqi_agent.get_hour_aqi_onecity(city, date)

def get_daily_aqi(date):
    return aqi_agent.get_daily_aqi(date)

def get_daily_aqi_onecity(city):
    return aqi_agent.get_daily_aqi_onecity(city)

