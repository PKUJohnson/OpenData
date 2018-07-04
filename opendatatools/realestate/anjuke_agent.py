# encoding: utf-8

from opendatatools.common import RestAgent
from bs4 import BeautifulSoup
import pandas as pd
import json

class AnjukeAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        self.city_map = {}

    def load_city(self):
        url = 'https://www.anjuke.com/sy-city.html'
        response = self.do_request(url)
        if response is None:
            return {}

        soup = BeautifulSoup(response, "html5lib")
        divs = soup.find_all('div')
        for div in divs:
            if div.has_attr('class') and 'letter_city' in div['class']:
                links = div.find_all('a')
                for link in links:
                    url = link['href']
                    city = link.text
                    self.city_map[city] = url

    @staticmethod
    def extract_word(text, start_tag, end_tag):
        index1 = text.find(start_tag)
        index2 = text.find(end_tag, index1)
        return text[index1 + len(start_tag): index2]

    def get_city_list(self):
        if len(self.city_map) == 0:
            self.load_city()

        return self.city_map.keys()

    def get_real_house_price(self, city):

        if len(self.city_map) == 0:
            self.load_city()

        if city not in self.city_map:
            return None, "城市输入错误"

        url = self.city_map[city]
        url_market = url + "/market/"
        response = self.do_request(url_market)
        if response is None:
            return None, '获取数据失败'

        content = AnjukeAgent.extract_word(response, 'drawChart(', ');')
        xyear = json.loads('{' + AnjukeAgent.extract_word(content, 'xyear:{', '},') + '}')
        ydata = json.loads(AnjukeAgent.extract_word(content, 'ydata:', '] '))
        list_date = []
        for month, year in xyear.items():
            month = int(month.replace('月', ''))
            year = int(year.replace('年', ''))
            date = '%04d%02d' % (year, month)
            list_date.append(date)
        list_price = ydata[0]['data']

        df = pd.DataFrame({'date': list_date, 'price': list_price})
        df['city'] = city
        return df, ''

