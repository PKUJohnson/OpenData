# encoding: UTF-8

import datetime
from .aqi_agent import AQIAgent

aqi_agent = AQIAgent()

def set_proxies(proxies):
    aqi_agent.set_proxies(proxies)

def get_hour_aqi(time = None):
    if time is None:
        i = 0
        while i < 3:
            pub_time = datetime.datetime.now() - datetime.timedelta(hours=i)
            time = datetime.datetime.strftime(pub_time, "%Y-%m-%d %H:00:00")
            df_aqi = aqi_agent.get_hour_aqi(time)
            if len(df_aqi) > 0:
                return df_aqi
            i = i + 1
        return None

    else:
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

# recent 30 days
def get_recent_daily_aqi_onecity(city):
    return aqi_agent.get_recent_daily_aqi_onecity(city)