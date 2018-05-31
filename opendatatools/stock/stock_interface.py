# encoding: utf-8

from .stock_agent import SHExAgent, SZExAgent, CSIAgent
from opendatatools.common import get_current_day

shex_agent = SHExAgent()
szex_agent = SZExAgent()
csi_agent  = CSIAgent()

def get_index_list(market='SH'):
    if market == 'SH':
        return shex_agent.get_index_list()

    if market == 'SZ':
        return szex_agent.get_index_list()

    if market == 'CSI':
        return csi_agent.get_index_list()

def get_index_component(symbol):
    temp = symbol.split(".")

    if len(temp) == 2:
        market = temp[1]
        index  = temp[0]
        if market == 'SH':
            return shex_agent.get_index_component(index)
        elif market == 'SZ':
            return szex_agent.get_index_component(index)
        elif market == 'CSI':
            return csi_agent.get_index_component(index)
        else:
            return None
    else:
        return None

def get_rzrq_info(market='SH', date = None):
    if date is None:
        date = get_current_day(format = '%Y%m%d')

    if market == 'SH':
        return shex_agent.get_rzrq_info(date)

    if market == 'SZ':
        return szex_agent.get_rzrq_info(date)

    return None, None

def get_dividend(symbol):
    temp = symbol.split(".")

    if len(temp) == 2:
        market = temp[1]
        code = temp[0]
        if market == 'SH':
            return shex_agent.get_dividend(code)