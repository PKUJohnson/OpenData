# encoding: UTF-8

from opendatatools import realestate

if __name__ == '__main__':
    realestate.set_proxies({"https" : "https://127.0.0.1:1080"})
    #df = realestate.get_rsf_list_lianjia('北京市', max_page_no = 10)
    #print(df)

    #df = realestate.get_esf_list_by_distinct_lianjia('北京市', '海淀', max_page_no = 3)
    df = realestate.get_esf_list_by_distinct_lianjia('上海市', '浦东', max_page_no = 100)
    df['unit_price'] = df['unit_price'].apply(lambda x : float(x.replace('单价', '').replace('元/平米', '')))
    df.sort_values('unit_price', ascending=False, inplace=True)
    df = df[df['unit_price'] >= 100000]
    print(df)
