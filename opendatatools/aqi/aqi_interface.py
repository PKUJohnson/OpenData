# encoding: UTF-8

import datetime
from .aqi_agent import AQIAgent

aqi_agent = AQIAgent()

def get_hour_aqi(time = None):
    if time is None:
        time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:00:00")
    return aqi_agent.get_hour_aqi(time)

def get_hour_aqi_onecity(city, date = None):
    if date is None:
        date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    return aqi_agent.get_hour_aqi_onecity(city, date)

# can only get history data
def get_daily_aqi(date):
    return aqi_agent.get_daily_aqi(date)

# can only get history data
def get_daily_aqi_onecity(city):
    return aqi_agent.get_daily_aqi_onecity(city)

