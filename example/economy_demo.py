# encoding: utf-8

from opendatatools import economy

if __name__ == '__main__':

    #df = economy.get_indicator_map()
    #print(df)

    #df = economy.get_region_map();
    #print(df)

    #df = economy.get_city_map()
    #print(df)

    # 年度数据
    #df, msg = economy.get_gdp_y()
    #economy.disp_result(df, date_format="%Y")
    #print(df)

    #df,msg = economy.get_population_size_y()
    #economy.disp_result(df, data_format="%Y")
    #print(df)

    #df,msg = economy.get_population_structure_y()
    #df = df[(df['indicator'] == 'A030301') | (df['indicator'] == 'A030302') | (df['indicator'] == 'A030303') | (df['indicator'] == 'A030304')]
    #df = df[df['date'] >= '1990']
    #economy.disp_result(df, data_format="%Y")
    #print(df)

    #df,msg = economy.get_population_structure_y()
    #df = df[(df['indicator'] == 'A030305') | (df['indicator'] == 'A030306') | (df['indicator'] == 'A030307')]
    #df = df[df['date'] >= '1990']
    #economy.disp_result(df, data_format="%Y")
    #print(df)

    # 季度数据
    #df, msg = economy.get_gdp()
    #df = df[ (df['indicator'] == 'A010101') | (df['indicator'] == 'A010102')]
    #economy.disp_result(df, date_format='%YQ')
    #print(df)

    #df, msg = economy.get_gdp_q2q()
    #df = df[(df['date'] >= '2011')]
    #economy.disp_result(df, date_format='%YQ')
    #print(df)

    #df, msg = economy.get_region_gdp('上海')
    #df_1 = df[df['indicator'] == 'A010101']
    #economy.disp_result(df_1, date_format='%YQ')

    #df_2 = df[df['indicator'] == 'A010103']
    #economy.disp_result(df_2, date_format='%YQ')
    #print(df)
    #print(msg)


    # 月度数据

    # CPI
    #df, msg = economy.get_cpi()
    #df = df[(df['date'] >= '201701') & (df['value'] > 0) & (df['indicator'] == 'A01010101')]
    #economy.disp_result(df, '%Y%m')
    #print(df)

    #df, msg = economy.get_cpi()
    #df = df[(df['date'] >= '201701') & (df['value'] > 0) & (df['indicator'] != 'A01010101')]
    #economy.disp_result(df, '%Y%m')

    #df, msg = economy.get_region_cpi('上海')
    #df = df[(df['date'] >= '201701') & (df['value'] > 0)]
    #economy.disp_result(df, '%Y%m')
    #print(df)

    #df, msg = economy.get_ppi()
    #df = df[(df['value'] > 0)]
    #economy.disp_result(df, '%Y%m')
    #print(df)

    #df, msg = economy.get_region_ppi('上海')
    #df = df[(df['value'] > 0)]
    #economy.disp_result(df, '%Y%m')
    #print(df)

    #df, msg = economy.get_manufacturing_pmi()
    #df = df[(df['value'] > 0) & (df['indicator'] == 'A190101')]
    #economy.disp_result(df, '%Y%m')
    #print(df)

    #df, msg = economy.get_non_manufacturing_pmi()
    #df = df[(df['value'] > 0) & (df['indicator'] == 'A190201')]
    #economy.disp_result(df, '%Y%m')
    #print(df)

    #df, msg = economy.get_pmi()
    #df = df[(df['value'] > 0)]
    #economy.disp_result(df, '%Y%m')
    #print(df)

    #df, msg = economy.get_import_export()
    #df = df[(df['value'] > 0) &
    #        ( (df['indicator'] == 'A160101') #| (df['indicator'] == 'A160103')
    #           | (df['indicator'] == 'A160105') #| (df['indicator'] == 'A160107')
    #           | (df['indicator'] == 'A160109') #| (df['indicator'] == 'A16010B')
    #           | (df['indicator'] == 'A16010D') #| (df['indicator'] == 'A16010E')
    #        )]
    #economy.disp_result(df, '%Y%m')
    #print(df)

    '''
    df, msg = economy.get_import_export()
    df = df[(df['value'] > 0) &
            ( (df['indicator'] == 'A160102') #| (df['indicator'] == 'A160104')
               | (df['indicator'] == 'A160106') #| (df['indicator'] == 'A160108')
               | (df['indicator'] == 'A16010A') #| (df['indicator'] == 'A16010C')
            )]
    economy.disp_result(df, '%Y%m')
    print(df)
    '''

    '''
    df, msg = economy.get_fdi()
    df_1 = df[ (df['value'] > 0) & (df['indicator'] == 'A16020B')]
    economy.disp_result(df_1, '%Y%m')
    df_2 = df[ (df['value'] > 0) & (df['indicator'] == 'A16020C')]
    economy.disp_result(df_2, '%Y%m')
    print(df)
    '''

    '''
    df, msg = economy.get_fiscal_revenue()
    df_1 = df[(df['value'] > 0) & ( (df['indicator'] == 'A1A0101') | (df['indicator'] == 'A1A0102'))]
    economy.disp_result(df_1, '%Y%m')
    df_2 = df[(df['value'] > 0) & (df['indicator'] == 'A1A0103')]
    economy.disp_result(df_2, '%Y%m')
    print(df)
    '''

    '''
    df, msg = economy.get_fiscal_expend()
    df_1 = df[(df['value'] > 0) & ( (df['indicator'] == 'A1A0201') | (df['indicator'] == 'A1A0202'))]
    economy.disp_result(df_1, '%Y%m')
    df_2 = df[(df['value'] > 0) & (df['indicator'] == 'A1A0203')]
    economy.disp_result(df_2, '%Y%m')
    print(df)   
    '''

    '''
    df, msg = economy.get_M0_M1_M2()
    df_1 = df[(df['value'] > 0) & ((df['indicator'] == 'A1B0101') | (df['indicator'] == 'A1B0103') | (df['indicator'] == 'A1B0105'))]
    economy.disp_result(df_1, '%Y%m')
    df_2 = df[(df['value'] > 0) & ((df['indicator'] == 'A1B0102') | (df['indicator'] == 'A1B0104') | (df['indicator'] == 'A1B0106'))]
    economy.disp_result(df_2, '%Y%m')
    print(df)
    '''

    '''
    df, msg = economy.get_fixed_asset_investment()
    df_1 = df[(df['value'] > 0) & (df['indicator'] == 'A130101') ]
    economy.disp_result(df_1, '%Y%m')
    df_2 = df[(df['value'] > 0) & (df['indicator'] == 'A130102') ]
    economy.disp_result(df_2, '%Y%m')
    print(df)
    '''

    '''
    df, msg = economy.get_realestate_investment()
    df_1 = df[(df['value'] > 0) & ( (df['indicator'] == 'A140101') | (df['indicator'] == 'A140107') | (df['indicator'] == 'A140109'))]
    economy.disp_result(df_1, '%Y%m')
    df_2 = df[(df['value'] > 0) & ( (df['indicator'] == 'A140102') | (df['indicator'] == 'A140108') | (df['indicator'] == 'A14010A'))]
    economy.disp_result(df_2, '%Y%m')
    print(df)
    '''

    '''
    import pandas as pd
    df1, msg = economy.get_retail_sales()
    df2, msg = economy.get_online_retail_sales()
    df = pd.concat([df1, df2])
    df_1 = df[(df['value'] > 0) & ( (df['indicator'] == 'A150101') | (df['indicator'] == 'A150102') | (df['indicator'] == 'A150801'))]
    economy.disp_result(df_1, '%Y%m')
    df_2 = df[(df['value'] > 0) & ( (df['indicator'] == 'A150103') | (df['indicator'] == 'A150104') | (df['indicator'] == 'A150802'))]
    economy.disp_result(df_2, '%Y%m')
    print(df)
    '''

    df, msg = economy.get_house_price_index('天津')
    df_1 = df[(df['value'] != 0) & (
                                        (df['indicator'] == 'A010801') | (df['indicator'] == 'A010804') | (df['indicator'] == 'A010807') |
                                        (df['indicator'] == 'A01080A') | (df['indicator'] == 'A01080D') | (df['indicator'] == 'A01080G') |
                                        (df['indicator'] == 'A01080J') | (df['indicator'] == 'A01080M') | (df['indicator'] == 'A01080P')
    )]
    economy.disp_result(df_1, '%Y%m')
    df_2 = df[(df['value'] != 0) & (
                                        (df['indicator'] == 'A010802') | (df['indicator'] == 'A010805') | (df['indicator'] == 'A010808') |
                                        (df['indicator'] == 'A01080B') | (df['indicator'] == 'A01080E') | (df['indicator'] == 'A01080H') |
                                        (df['indicator'] == 'A01080K') | (df['indicator'] == 'A01080N') | (df['indicator'] == 'A01080Q')
    )]
    economy.disp_result(df_2, '%Y%m')
    print(df)

    #df, msg = economy.get_region_realestate_investment('上海')
    #print(df)

    #df, msg = economy.get_region_fixed_asset_investment('上海')
    #print(df)

    print()