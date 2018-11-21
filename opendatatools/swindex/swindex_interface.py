# encoding: utf-8

from .swindex_agent import SWIndexAgent

sw_agent = SWIndexAgent()

def get_index_list():
    return sw_agent.get_index_list()

def get_index_cons(index_code):
    return sw_agent.get_index_cons(index_code)

def get_index_daily(index_code, start_date, end_date):
    return sw_agent.get_index_daily(index_code, start_date, end_date)

def get_index_dailyindicator(index_code, start_date, end_date, freq):
    if freq == "D":
        type = "Day"
    elif freq == "M":
        type = "Month"
    elif freq == "W":
        type = "Week"
    else:
        type = "Day"
    return sw_agent.get_index_dailyindicator(index_code, start_date, end_date, type)

