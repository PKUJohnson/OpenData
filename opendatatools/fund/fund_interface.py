# encoding: utf-8

from .fund_agent import EastMoneyAgent

eastmoney_agent = EastMoneyAgent()

def get_fund_list():
    return eastmoney_agent.get_fund_list()

def get_fund_company():
    return eastmoney_agent.get_fund_company()

def get_fundlist_by_company(companyid):
    return eastmoney_agent.get_fundlist_by_company(companyid)

def get_fund_type():
    return eastmoney_agent.get_fund_type()

def get_fundlist_by_type(type):
    return eastmoney_agent.get_fundlist_by_type(type)

def get_fund_nav(fund_code):
    return eastmoney_agent.get_fund_nav(fund_code)