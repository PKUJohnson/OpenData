
from .simu_agent import SimuAgent

simu_agent = SimuAgent()


def set_proxies(proxies):
    simu_agent.set_proxies(proxies)

def login(username, password):
    user_info, msg = simu_agent.login(username, password)
    return user_info, msg

def load_data():
    df_fundlist, msg = simu_agent.load_data()
    return df_fundlist, msg

def get_fund_list():
    return simu_agent.get_fund_list()

def get_fund_nav(fund_id):
    return simu_agent.get_fund_nav(fund_id)