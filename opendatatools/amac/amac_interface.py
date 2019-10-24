# encoding: UTF-8

import datetime
from .amac_agent import AMACAgent

amac_agent = AMACAgent()

def set_proxies(proxies):
    amac_agent.set_proxies(proxies)

def get_company_list():
    return amac_agent.get_company_list()

def get_company_detail(company_id):
    return amac_agent.get_company_detail(company_id)

def get_fund_list():
    return amac_agent.get_fund_list()

def get_fund_detail(fund_id):
    return amac_agent.get_fund_detail(fund_id)
