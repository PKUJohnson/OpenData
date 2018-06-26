# encoding: utf-8

import datetime

from .hsgt_agent import EastMoneyAgent
from .hkex_agent import HKExAgent

eastmoney_agent = EastMoneyAgent()
hkex_agent = HKExAgent()

def set_proxies(proxies):
    hkex_agent.set_proxies(proxies)
    eastmoney_agent.set_proxies(proxies)

# 获取陆港通 北向 持股 情况
# 参数：市场SH/SZ，日期YYYY-MM-DD
def get_lgt_share(market = 'SH', date = None):
    if date is None:
        i = 0
        while i < 5:
            pub_time = datetime.datetime.now() - datetime.timedelta(days=i)
            date = datetime.datetime.strftime(pub_time, "%Y-%m-%d")
            df = hkex_agent.get_lgt_share(market, date)
            if len(df) > 0:
                return df
            i = i + 1
        return None

    else:
        return hkex_agent.get_lgt_share(market, date)

# 单位：亿元
def get_realtime_moneyflow():
    return eastmoney_agent.get_realtime_moneyflow()

# HSMoney : 沪市北向资金  SSMoney : 深市北向资金  NorthMoney : 北向资金汇总
# GGHSMoney : 港股沪市资金  GGSSMoney : 港股深市资金  SouthSumMoney ：南向资金汇总
# 单位：百万元
def get_hist_moneyflow():
    return eastmoney_agent.get_hist_moneyflow()

# markettype: 1 沪股通 2 港股通（沪）3 深股通 4 港股通（深市）
# DRZJLR: 当日资金流入 DRYE：当日余额 LSZJLR：历史资金累计流入 DRCJJME：当日成交净买额 MRCJE：买入成交额 MCCJE：卖出成交额
# 其他字段可以忽略
# 单位：百万元（百万港元 - 涉及港股市场的成交和净买卖金额，单位都是百万港币）
def get_his_tradestat(markettype):
    return eastmoney_agent.get_his_tradestat(markettype)

def get_ah_compare():
    return eastmoney_agent.get_ah_compare()