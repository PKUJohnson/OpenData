from .simu_agent import SimuAgent, BarclayAgent, index_map
import pandas as pd

simu_agent = SimuAgent()
barclay_agent = BarclayAgent()

def set_proxies(proxies):
    simu_agent.set_proxies(proxies)
    barclay_agent.set_proxies(proxies)

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

def get_barclay_data(index):
    return barclay_agent.get_data(index)

def get_barclay_index_list():
    data_list = []
    for k, v in index_map.items():
        data_list.append([k, v])
    df = pd.DataFrame(data_list, columns=['index', 'prog_cod'])
    return df[['index']], ''