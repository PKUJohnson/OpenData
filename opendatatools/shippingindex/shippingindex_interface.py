# encoding: utf-8

from .eastmoney_agent import EastMoneyAgent

eastmoney_agent = EastMoneyAgent()

def get_index_list():
    return eastmoney_agent.get_index_list()

def get_index_data(index_code):
    return eastmoney_agent.get_index_data(index_code)

