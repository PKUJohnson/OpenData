# encoding: utf-8

from .futures_agent import SHFAgent, DCEAgent, CZCAgent, CFEAgent
from opendatatools.common import get_target_date, date_convert

shf_agent = SHFAgent()
dce_agent = DCEAgent()
czc_agent = CZCAgent()
cfe_agent = CFEAgent()

def get_trade_rank(market = 'SHF', date = None):
    if date is None:
        date = get_target_date(-1, "%Y-%m-%d")

    if market == 'SHF':
        return shf_agent.get_trade_rank(date)

    if market == 'DCE':
        return dce_agent.get_trade_rank(date)

    if market == 'CZC':
        return czc_agent.get_trade_rank(date)

    if market == "CFE":
        return cfe_agent.get_trade_rank(date)

    return None, '不支持的市场类型'


