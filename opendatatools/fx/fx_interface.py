# encoding: utf-8

from .chinamoney_agent import ChinaMoneyAgent
from opendatatools.common import date_convert, get_current_day, get_target_date, get_target_date2
import pandas as pd

chinamoney_agent = ChinaMoneyAgent()

def format_date_param(start_date, end_date):
    if end_date is None:
        end_date = get_current_day()

    if start_date is None:
        start_date = get_target_date(-360, '%Y-%m-%d')

    return start_date, end_date

def _split_qry_range(start_date, end_date):
    list_qry_date = []
    p_start_date = start_date
    while True:
        p_end_date   = get_target_date2(p_start_date, 360)
        if p_end_date > end_date:
            p_end_date = end_date
        list_qry_date.append((p_start_date, p_end_date))

        p_start_date = get_target_date2(p_end_date, 1)
        if p_start_date > end_date:
            break

    return list_qry_date

def get_hist_cny_cpr(start_date = None, end_date = None):
    start_date, end_date = format_date_param(start_date, end_date)
    list_qry_date = _split_qry_range(start_date, end_date)
    df_list = []
    for p_start_date, p_end_date in list_qry_date:
        df, msg = chinamoney_agent.get_hist_cny_cpr(p_start_date, p_end_date)
        if df is None:
            return df, msg
        df_list.append(df)

    df_result = pd.concat(df_list)
    df_result.set_index('date', inplace=True)
    df_result.sort_index(inplace=True)

    return df_result, ""

def get_his_shibor(start_date = None, end_date = None):
    start_date, end_date = format_date_param(start_date, end_date)
    list_qry_date = _split_qry_range(start_date, end_date)
    df_list = []
    for p_start_date, p_end_date in list_qry_date:
        df, msg = chinamoney_agent.get_his_shibor(p_start_date, p_end_date)
        if df is None:
            return df, msg
        df_list.append(df)

    df_result = pd.concat(df_list)
    df_result.set_index('showDateCN', inplace=True)
    df_result.sort_index(inplace=True)

    return df_result, ""

def get_realtime_shibor():
    return chinamoney_agent.get_realtime_shibor()

def get_cny_spot_price():
    return chinamoney_agent.get_cny_spot_price()
