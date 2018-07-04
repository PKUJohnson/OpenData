# encoding: utf-8

from .anjuke_agent import AnjukeAgent

anjuke_agent  = AnjukeAgent()

def set_proxies(proxies):
    anjuke_agent.set_proxies(proxies)

def get_city_list():
    return anjuke_agent.get_city_list()

def get_real_house_price(city):
    return anjuke_agent.get_real_house_price(city)