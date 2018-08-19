# encoding: UTF-8

from opendatatools import realestate

if __name__ == '__main__':
    #realestate.set_proxies({"https" : "https://127.0.0.1:1080"})

    #city_list = realestate.get_city_list()
    #print(city_list)

    #district_list = realestate.get_district_list()
    #print(district_list)

    #df = realestate.get_esf_list_lianjia('北京', max_page_no = 3)
    #print(df)

    #df = realestate.get_esf_list_lianjia('成都', max_page_no = 3)
    #print(df)

    #df = realestate.get_esf_list_lianjia('武汉', max_page_no = 3)
    #print(df)

    #city_list = realestate.get_city_list_lianjia()
    #print(city_list)

    #district_map = realestate.get_district_list_lianjia('杭州')
    #print(district_map)

    #df = realestate.get_esf_list_by_district_lianjia('北京', '海淀', max_page_no = 3)
    #print(df)

    #df = realestate.get_esf_list_by_district_lianjia('上海市', '浦东', max_page_no = 100)
    #df['unit_price'] = df['unit_price'].apply(lambda x : float(x.replace('单价', '').replace('元/平米', '')))
    #df.sort_values('unit_price', ascending=False, inplace=True)
    #df = df[df['unit_price'] >= 100000]
    #print(df)

    #df, msg = realestate.get_real_house_price('北京')
    #print(df)

    df, msg = realestate.get_rent('北京', page_no=1000)
    print(df)
