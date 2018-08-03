# encoding: utf-8

from .nhindex_agent import NHIndexAgent

nh_agent = NHIndexAgent()

def get_index_list():
    return nh_agent.get_index_list()

def get_index_daily(index_code):
    return nh_agent.get_index_daily(index_code)

def get_index_snapshot():
    return nh_agent.get_index_snapshot()

def get_index_weight():
    return nh_agent.get_index_weight()

