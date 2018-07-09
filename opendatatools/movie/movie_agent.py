# encoding: utf-8

from opendatatools.common import RestAgent
import pandas as pd
from bs4 import BeautifulSoup
import json

class MovieAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    @staticmethod
    def clear_text(text):
        return text.replace('\n', '').strip()

    def _get_boxoffice_onepage(self, page_no):
        url = 'http://www.cbooo.cn/BoxOffice/getInland'
        data = {
            'pIndex' : page_no,
            't'       : 0,
        }
        response = self.do_request(url, param=data, encoding='utf8')
        if response is None:
            return None

        jsonobj = json.loads(response)

        df = pd.DataFrame(jsonobj)
        return df

    def get_boxoffice(self):
        df_list= []
        for page_no in range(1,6):
            df = self._get_boxoffice_onepage(page_no)
            if df is None:
                return None, '获取数据失败'

            df_list.append(df)

        if len(df_list) == 0:
            return None, '获取数据失败'

        return pd.concat(df_list), ''

    def get_realtime_boxoffice(self):
        url = 'http://www.cbooo.cn/BoxOffice/GetHourBoxOffice'
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        jsonobj = json.loads(response)
        return pd.DataFrame(jsonobj['data2']), ''

    def get_recent_boxoffice(self, day):
        url = 'http://www.cbooo.cn/BoxOffice/GetDayBoxOffice?num=-%d' % (day)
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        jsonobj = json.loads(response)
        df = pd.DataFrame(jsonobj['data1'])
        df['date'] = jsonobj['data2'][0]['BoxDate']
        return df, ''

    def get_monthly_boxoffice(self, date):
        url = 'http://www.cbooo.cn/BoxOffice/getMonthBox?sdate=%s' % (date)
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        jsonobj = json.loads(response)
        return pd.DataFrame(jsonobj['data1']), ''

    def get_yearly_boxoffice(self, year):
        url = 'http://www.cbooo.cn/year?year=%d' % (year)
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        soup = BeautifulSoup(response, "html5lib")
        divs = soup.find_all('div')

        data = []
        for div in divs:
            if div.has_attr('id') and div['id'] == 'tabcont':
                rows = div.table.findAll('tr')
                for row in rows:
                    cols = row.findAll('td')
                    if len(cols) == 7:
                        movie_name = MovieAgent.clear_text(cols[0].text)
                        movie_type = MovieAgent.clear_text(cols[1].text)
                        boxoffice  = MovieAgent.clear_text(cols[2].text)
                        avgprice   = MovieAgent.clear_text(cols[3].text)
                        audience   = MovieAgent.clear_text(cols[4].text)
                        country    = MovieAgent.clear_text(cols[5].text)
                        showtime   = MovieAgent.clear_text(cols[6].text)

                        data.append({
                            "movie_name": movie_name,
                            "movie_type": movie_type,
                            "boxoffice" : boxoffice,
                            "avgprice"  : avgprice,
                            "audience"  : audience,
                            "country"   : country,
                            "showtime"  : showtime,
                        })

        return pd.DataFrame(data), ''