# encoding: utf-8

import datetime
from .nbs_agent import NBSAgent

nbs_agent = NBSAgent()

def convert_date(date, date_format):
    if date_format == '%YQ':
        date_format = '%Y%m'
        date = date.replace('A', '03').replace('B', '06').replace('C', '09').replace('D', '12')

    return datetime.datetime.strptime(date, date_format)

def disp_result(df, date_format = '%Y%m'):
    import matplotlib.pyplot as plt
    import datetime

    from matplotlib.pylab import mpl
    # 指定默认字体
    mpl.rcParams['font.sans-serif'] = ['FangSong']
    # 解决保存图像是负号'-'显示为方块的问题
    mpl.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(figsize=(16,10))
    for name, sub_df in df.groupby('indicator_name'):
        sub_df['date'] = sub_df['date'].apply(lambda x : convert_date(x, date_format))
        sub_df.set_index('date', inplace = True)
        sub_df.sort_index(ascending=True, inplace=True)
        plt.plot(sub_df.index, sub_df['value'], label=name)
        plt.legend()

    plt.grid(True)
    plt.show()

# 指标名称映射表
def get_indicator_map():
    return nbs_agent.get_indicator_map()

# 省份名称
def get_region_map():
    return nbs_agent.get_region_map()

# 城市名称
def get_city_map():
    return nbs_agent.get_city_map()

# 年度数据
def get_gdp_y():
    return nbs_agent.get_gdp_y()

def get_region_gdp_y():
    return nbs_agent.get_region_gdp_y()

def get_population_size_y():
    return nbs_agent.get_population_size_y()

def get_population_structure_y():
    return nbs_agent.get_population_structure_y()

def get_house_price_index(region):
    return nbs_agent.get_house_price_index(region)

def get_cpi():
    return nbs_agent.get_cpi()

def get_region_cpi(region):
    return nbs_agent.get_region_cpi(region)

def get_ppi():
    return nbs_agent.get_ppi()

def get_region_ppi(region):
    return nbs_agent.get_region_ppi(region)

def get_gdp():
    return nbs_agent.get_gdp()

def get_region_gdp(region):
    return nbs_agent.get_region_gdp(region)

def get_gdp_q2q():
    return nbs_agent.get_gdp_q2q()

def get_M0_M1_M2():
    return nbs_agent.get_M0_M1_M2()

def get_fiscal_revenue():
    return nbs_agent.get_fiscal_revenue()

def get_fiscal_expend():
    return nbs_agent.get_fiscal_expend()

def get_manufacturing_pmi():
    return nbs_agent.get_manufacturing_pmi()

def get_non_manufacturing_pmi():
    return nbs_agent.get_non_manufacturing_pmi()

def get_pmi():
    return nbs_agent.get_pmi()

def get_import_export():
    return nbs_agent.get_import_export()

def get_fdi():
    return nbs_agent.get_fdi()

def get_retail_sales():
    return nbs_agent.get_retail_sales()

def get_online_retail_sales():
    return nbs_agent.get_online_retail_sales()

def get_realestate_investment():
    return nbs_agent.get_realestate_investment()

def get_region_realestate_investment(region):
    return nbs_agent.get_region_realestate_investment(region)

def get_fixed_asset_investment():
    return nbs_agent.get_fixed_asset_investment()

def get_region_fixed_asset_investment(region):
    return nbs_agent.get_region_fixed_asset_investment(region)