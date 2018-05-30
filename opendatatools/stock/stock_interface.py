# encoding: utf-8

from .stock_agent import SHExAgent, SZExAgent

shex_agent = SHExAgent()
szex_agent = SZExAgent()

def get_index_list(market='SH'):
    if market == 'SH':
        return shex_agent.get_index_list()

    if market == 'SZ':
        return szex_agent.get_index_list()

def get_index_component(symbol):
    temp = symbol.split(".")

    if len(temp) == 2:
        market = temp[1]
        index  = temp[0]
        if market == 'SH':
            return shex_agent.get_index_component(index)
        elif market == 'SZ':
            return szex_agent.get_index_component(index)
        else:
            return None
    else:
        return None
