# encoding: utf-8

from .chinamoney_agent import ChinaMoneyAgent
from opendatatools.common import date_convert, get_current_day, get_target_date

chinamoney_agent = ChinaMoneyAgent()

def format_date_param(start_date, end_date):
    if end_date is None:
        end_date = get_current_day()

    if start_date is None:
        start_date = get_target_date(-360, '%Y-%m-%d')

    return start_date, end_date

def get_hist_cny_cpr(start_date = None, end_date = None):
    start_date, end_date = format_date_param(start_date, end_date)
    return chinamoney_agent.get_hist_cny_cpr(start_date, end_date)

def get_his_shibor(start_date = None, end_date = None):
    start_date, end_date = format_date_param(start_date, end_date)
    return chinamoney_agent.get_his_shibor(start_date, end_date)

def get_realtime_shibor():
    return chinamoney_agent.get_realtime_shibor()

def get_cny_spot_price():
    return chinamoney_agent.get_cny_spot_price()
