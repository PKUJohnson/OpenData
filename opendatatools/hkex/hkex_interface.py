# encoding: UTF-8

import datetime
from .hkex_agent import HKExAgent

hkex_agent = HKExAgent()

def set_proxies(proxies):
    hkex_agent.set_proxies(proxies)

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