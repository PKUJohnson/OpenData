# encoding: utf-8

from .robo_agent import RoboAgent

robo_agent = RoboAgent()

def set_proxies(proxies):
    robo_agent.set_proxies(proxies)

# 使用前，请在通联数据萝卜投研注册帐号
def login(username, password):
    return robo_agent.login(username, password)

def get_top_items():
    return robo_agent.get_top_items()

def get_sub_items(itemid):
    return robo_agent.get_sub_items(itemid)

def get_series(seriesid):
    return robo_agent.get_series(seriesid)
