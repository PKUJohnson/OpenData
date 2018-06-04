# encoding: utf-8

from .lianjia_agent import LianjiaAgent

lianjia_agent = LianjiaAgent()

def set_proxies(proxies):
    lianjia_agent.set_proxies(proxies)

def get_esf_list_lianjia(city, max_page_no = 100):
    return lianjia_agent.get_esf_list(city, max_page_no)

def get_esf_list_by_distinct_lianjia(city, distinct, max_page_no = 100):
    return lianjia_agent.get_esf_list_by_distinct(city, distinct, max_page_no)