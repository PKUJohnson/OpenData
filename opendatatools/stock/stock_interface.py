# encoding: utf-8

from .stock_agent import SHExAgent, SZExAgent

shex_agent = SHExAgent()
szex_agent = SZExAgent()

def get_index_list(market='SH'):
    if market == 'SH':
        return shex_agent.get_index_list()

    if market == 'SZ':
        return szex_agent.get_index_list()
