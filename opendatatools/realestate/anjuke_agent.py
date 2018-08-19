# encoding: utf-8

from opendatatools.common import RestAgent
from bs4 import BeautifulSoup
import pandas as pd
import json
anjuke_city_map = {
    '北京' : 'bj',
    '上海' : 'sh',
    '杭州' : 'hz',
    '广州' : 'gz',
    '深圳' : 'sz',
    '厦门' : 'xm',
    '苏州' : 'su',
    '重庆' : 'cq',
    '长沙' : 'cs',
    '海口' : 'hk',
    '合肥' : 'hf',
    '济南' : 'jn',
    '青岛' : 'qd',
    '南京' : 'nj',
    '石家庄': 'sjz',
    '沈阳' : 'sy',
    '天津' : 'tj',
    '武汉' : 'wh',
    '无锡' : 'wx',
    '西安' : 'xa',
    '珠海' : 'zh',
    '郑州' : 'zz',
}
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

    def get_rent(self, city, page_no):

        url = "https://%s.zu.anjuke.com/p%s/" % (city, page_no)
        response = self.do_request(url, encoding='utf-8')
        soup = BeautifulSoup(response, 'html5lib')
        divs = soup.find_all('div')
        data_list = []
        for div in divs:
            if div.has_attr('class') and 'zu-itemmod' in div['class']:
                try:
                    title = div.find_all('h3')[0].a.text
                    row1 = div.find_all('p')[0].text.split('|')
                    type = row1[0].replace('\n', '').replace(' ', '')
                    area = row1[1].replace('\n', '').replace(' ', '')
                    height = row1[2].split('层')[0]

                    row2 = div.find_all('p')[1].text.replace(' ', '').split('\n')
                    part = row2[1]
                    direction = row2[2]
                    trans = row2[3]
                    price = div.find_all('p')[2].text
                    row3 = div.find_all('address')[0].text.split('\n')

                    addr = row3[1].replace(' ', '')
                    location = row3[2].replace(' ', '').split(r"\\")[0]
                    data_list.append([type, area, height, part, direction, trans, price, addr, location, title])
                except:
                    print('error occurs on this item')
        return data_list, ''


