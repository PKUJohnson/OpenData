# encoding: UTF-8

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from opendatatools.common import RestAgent
from opendatatools.aqi.constant import city_code_map


class AQIAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

        '''
        df_proxy = self.get_proxy_list()
        if df_proxy is None:
            self.proxies = None
        else:
            rand_num = np.random.randint(100)

            df1  = df_proxy[df_proxy['Type'] == "HTTP"]
            df2 = df_proxy[df_proxy['Type'] == "HTTPS"]

            pos1  = rand_num % len(df1)
            pos2 = rand_num % len(df2)

            url1 = "http://"  + df1.iat[pos1, 0] + ":" + df1.iat[pos1, 1]
            url2 = "https://" + df2.iat[pos2, 0] + ":" + df2.iat[pos2, 1]
            self.proxies = {"http" : url1, "https" : url2}
        '''

        #self.proxies = {"http": "http://183.95.80.168:80"}
        self.proxies = None

    def get_daily_aqi(self, date):
        url = "http://datacenter.mep.gov.cn/websjzx/report/list.vm"
        page_no = 0
        aqi_result = list()

        while True:
            page_no = page_no + 1
            # 1. 分页爬取数据
            data = {
                'pageNum': page_no,
                'V_DATE': date,
                'xmlname': 1512478367400,
                'roleType': 'CFCD2084',
            }

            rsp = self.do_request(url, data, self.proxies)

            if rsp is None:
                return None

            data = list()
            soup = BeautifulSoup(rsp)
            divs = soup.find_all('div')

            for div in divs:
                if div.has_key('class') and 'report_main' in div['class']:
                    rows = div.table.findAll('tr')
                    for row in rows:
                        cols = row.findAll('td')
                        if len(cols) == 9:
                            city      = cols[3].text
                            aqi       = cols[4].text
                            indicator = cols[5].text
                            date      = cols[6].text
                            code      = cols[7].text
                            level     = cols[8].text
                            data.append ({
                                "date"  : date,
                                "city"  : city,
                                "aqi"   : aqi,
                                "code"  : code,
                                "level" : level,
                                "indicator" : indicator,
                            })

            if len(data) == 0:
                break;

            print(data)
            aqi_result.extend(data)

        return pd.DataFrame(aqi_result)

    '''
    def get_daily_aqi_onecity(self, city, start_date, end_date):
        aqi_result = dict()
        page_no = 0

        while True:
            page_no = page_no + 1

            # 1. 分页爬取数据
            data = {
                'page.pageNo': page_no,
                'CITY': city,
                'V_DATE': start_date,
                'E_DATE': end_date,
                'xmlname': 1462259560614
            }

            res = self.do_request(self.url, params=data)
            if res.status_code != 200:
                print("query_error, status_code = ", res.status_code)
                return None

            rsp = res.text

            # 2. 开始解析返回数据，并从html中提取需要的内容
            data = dict()
            soup = BeautifulSoup(rsp)
            divs = soup.find_all('div')

            for div in divs:
                if div.has_key('class') and 'report_main' in div['class']:
                    rows = div.table.tbody.findAll('tr')
                    for row in rows:
                        cols = row.findAll('td')
                        if len(cols) == 9:
                            data[cols[6].text] = cols[3].text

            if len(data) == 0:
                break;

            aqi_result.update(data)

        session.close()
        return aqi_result

    '''

if __name__ == '__main__':
    aqi = AQIAgent()
    result = aqi.get_daily_aqi('2018-02-26')
    result.to_csv("1.csv")
    print(result)