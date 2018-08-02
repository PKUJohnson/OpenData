# encoding: utf-8

import datetime
import pandas as pd
from bs4 import BeautifulSoup
from xml.etree import ElementTree

from opendatatools.common import RestAgent

class SWIndexAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_index_list(self):
        url = 'http://www.swsindex.com/idx0110.aspx'

        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        soup = BeautifulSoup(response, "html5lib")

        sections = soup.find_all("div", class_="honor")

        section_names = [
            '量化策略', '市场表征', '一级行业', '风格指数', '申万商品期货指数', '新三板', '定制发布'
        ]

        data = []
        for section in sections:
            name = section.h3.text.strip()
            if name not in section_names:
                continue

            table = section.table
            rows = table.findAll('tr')
            for row in rows:
                cols = row.findAll('td')
                if (len(cols) >= 4):
                    index_name = cols[0].text
                    start_date = cols[1].text
                    index_code = cols[0].a['href'][-6:]

                    data.append({
                        'index_code'   : index_code,
                        'index_name'   : index_name,
                        'start_date'   : start_date,
                        'section_name' : name
                    })
        return pd.DataFrame(data), ''

    def get_index_cons(self, index_code):
        url = 'http://www.swsindex.com/downfile.aspx?code=%s' %  index_code
        response = self.do_request(url, None, method='GET', type='text')
        if response is not None:
            soup = BeautifulSoup(response, "html5lib")

            data = []
            table = soup.findAll('table')[0]
            rows = table.findAll('tr')
            for row in rows:
                cols = row.findAll('td')
                if (len(cols) >= 4):
                    index_code = cols[0].text
                    index_name = cols[1].text
                    weight     = cols[2].text
                    start_date = cols[3].text

                    data.append({
                        'index_code': index_code,
                        'index_name': index_name,
                        'start_date': start_date,
                        'weight'     : weight
                    })
            df = pd.DataFrame(data)
            df['start_date'] = df['start_date'].apply(lambda x : datetime.datetime.strptime(x, '%Y/%m/%d %H:%M:%S'))
            return df, ''

        return None, '获取数据失败'

    def get_index_daily(self, index_code):
        url = 'http://222.73.228.238/chartdata/Day-K/%s.xml' % index_code
        response = self.do_request(url, None, method='GET', type='text', encoding='utf8')
        root = ElementTree.fromstring(response)
        data = []
        for dataElements in root:
            open = dataElements.attrib['op']
            high = dataElements.attrib['hp']
            low = dataElements.attrib['lp']
            close = dataElements.attrib['ep']
            vol = dataElements.attrib['vol']
            amount = dataElements.attrib['tot']
            date = dataElements.attrib['tdd']

            data.append({
                'open': open,
                'high': high,
                'low': low,
                'close': close,
                'vol': vol,
                'amount': amount,
                'date': date
            })

        df = pd.DataFrame(data)
        df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
        return df, ''

    def get_index_dailyindicator(self, index_code, start_date, end_date):
        url = 'http://www.swsindex.com/excel.aspx?ctable=V_Report&where=%s'
        where_cond = "swindexcode in ('%s') and BargainDate >= '%s' and BargainDate <= '%s' and type='Day'" % (index_code, start_date, end_date)
        url = url % where_cond

        response = self.do_request(url, None, method='GET', type='text', encoding='utf8')
        if response is None:
            return None, '获取数据失败'

        soup = BeautifulSoup(response, "html5lib")
        data = []
        table = soup.findAll('table')[0]
        rows = table.findAll('tr')
        for row in rows:
            cols = row.findAll('td')
            if (len(cols) >= 14):
                index_code = cols[0].text
                index_name = cols[1].text
                date = cols[2].text
                close = cols[3].text
                volume = cols[4].text
                chg_pct = cols[5].text
                turn_rate = cols[6].text
                pe = cols[7].text
                pb = cols[8].text
                vwap = cols[9].text
                float_mv = cols[11].text
                avg_float_mv = cols[12].text
                dividend_yield_ratio = cols[13].text

                data.append({
                    'index_code': index_code,
                    'index_name': index_name,
                    'date': date,
                    'close': close,
                    'volume': volume,
                    'chg_pct': chg_pct,
                    'turn_rate': turn_rate,
                    'pe': pe,
                    'pb': pb,
                    'vwap': vwap,
                    'float_mv': float_mv,
                    'avg_float_mv': avg_float_mv,
                    'dividend_yield_ratio': dividend_yield_ratio,
                })

        df = pd.DataFrame(data)
        df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y/%m/%d %H:%M:%S'))
        return df, ''
