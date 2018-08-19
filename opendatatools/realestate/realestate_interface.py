# encoding: utf-8

from .anjuke_agent import AnjukeAgent, anjuke_city_map
from .lianjia_agent import LianjiaAgent
import pandas as pd

anjuke_agent  = AnjukeAgent()
lianjia_agent = LianjiaAgent()

def set_proxies(proxies):
    anjuke_agent.set_proxies(proxies)
    lianjia_agent.set_proxies(proxies)

def get_city_list():
    return anjuke_agent.get_city_list()

def get_real_house_price(city):
    return anjuke_agent.get_real_house_price(city)

def get_city_list_lianjia():
    return lianjia_agent.get_city_list()

def get_district_list_lianjia(city):
    return lianjia_agent.get_district_by_city(city)

def get_esf_list_lianjia(city, max_page_no=10):
    city_list = lianjia_agent.get_city_list()
    if city not in city_list:
        msg = "invalid city, please use " + ".".join(city_list)
        return None, msg

    return lianjia_agent.get_esf_list(city, max_page_no)

def get_esf_list_by_district_lianjia(city, district, max_page_no=10):
    city_list = lianjia_agent.get_city_list()
    if city not in city_list:
        msg = "invalid city, please use " + ".".join(city_list)
        return None, msg

    district_map = lianjia_agent.get_district_by_city(city)
    if district not in district_map:
        msg = "invalid district, please use " + ".".join(district_map.keys())
        return None, msg

    return lianjia_agent.get_esf_list_by_district(city, district, max_page_no)

def get_rent(city, page_no):
    if city in anjuke_city_map.keys():
        city = anjuke_city_map[city]
        column = ['shape', 'area', 'floor', 'part', 'direction', 'trans', 'price', 'name', 'location', 'title']
        data_all = []
        for i in range(page_no):
            print('get data from page %s' % (i+1))
            data_list, msg = anjuke_agent.get_rent(city, i+1)
            data_all.extend(data_list)
        df = pd.DataFrame(data_all, columns=column)
        return df, ''
    else:
        return None, '暂不支持该城市'