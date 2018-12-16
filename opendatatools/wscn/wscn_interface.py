# encoding: utf-8

from .wscn_agent import XuangubaoAgent

xgb_agent = XuangubaoAgent()


def login(username, password):
    return xgb_agent.login(username, password)

def get_xuangubao_theme():
    return xgb_agent.get_theme()

def get_xuangubao_theme_stock(tid):
    return xgb_agent.get_theme_stock(tid)

def get_xuangubao_theme_kline(tid):
    return xgb_agent.get_theme_kline(tid)

def get_xuangubao_theme_event(tid):
    return xgb_agent.get_theme_event(tid)
