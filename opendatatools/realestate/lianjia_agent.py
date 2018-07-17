# encoding: utf-8

from opendatatools.common import RestAgent
from bs4 import BeautifulSoup
from progressbar import ProgressBar

import pandas as pd
import re

lianjia_city_map = {
    '北京' : 'bj',
    '上海' : 'sh',
    '成都' : 'cd',
    '杭州' : 'hz',
    '广州' : 'gz',
    '深圳' : 'sz',
    '厦门' : 'xm',
    '苏州' : 'su',
    '重庆' : 'cq',
    '长沙' : 'cs',
    '大连' : 'dl',
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
    '烟台' : 'yt',
    '中山' : 'zs',
    '珠海' : 'zh',
    '郑州' : 'zz',
}

class LianjiaAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_city_list(self):
        return lianjia_city_map.keys()

    def get_district_by_city(self, city):
        city_code = lianjia_city_map[city]
        url = 'https://%s.lianjia.com/ershoufang/' % city_code
        response = self.do_request(url)

        soup = BeautifulSoup(response, "html5lib")
        divs = soup.find_all('div')

        data_map = {}
        for div in divs:
            if div.has_attr('data-role') and 'ershoufang' in div['data-role']:
                sub_divs = div.find_all('div')
                sub_div  = sub_divs[0]
                links = sub_div.find_all('a')
                for link in links:
                    #link_addr = link
                    #data_list.append(data)
                    key   = link.text
                    value = link['href'].replace('/ershoufang/', '').replace('/', '')
                    data_map[key] = value

        return data_map

    @staticmethod
    def clear_text(text):
        return text.replace('\n', '').strip()

    def get_esf_list(self, city, max_page_no):
        if max_page_no>100:
            max_page_no = 100
        if city in lianjia_city_map:
            city_code = lianjia_city_map[city]
            return self._get_esf_list(city_code, max_page_no)

    def get_esf_list_by_district(self, city, district, max_page_no):
        if max_page_no>100:
            max_page_no = 100

        if city in lianjia_city_map:
            city_code = lianjia_city_map[city]

        district_map = self.get_district_by_city(city)
        if district in district_map:
            district_code = district_map[district]

        return self._get_esf_list_by_district(city_code, district_code, max_page_no)

    def _get_esf_list(self, city_code, max_page_no):
        page_no = 1
        result_list = []
        process_bar = ProgressBar().start(max_value=max_page_no)
        while page_no <= max_page_no:
            process_bar.update(page_no)
            #print('getting data from lianjia.com for page %d' % page_no)
            data_list = self._get_erf_list_url('https://%s.lianjia.com/ershoufang/pg%d/' % (city_code, page_no))
            page_no = page_no + 1
            if (len(data_list) == 0):
                break
            result_list.extend(data_list)

        return pd.DataFrame(result_list)

    def _get_esf_list_by_district(self, city_code, district_code, max_page_no):
        page_no = 1
        result_list = []
        process_bar = ProgressBar().start(max_value=max_page_no)
        while page_no <= max_page_no:
            process_bar.update(page_no)
            #print('getting data from lianjia.com for page %d' % page_no)
            data_list = self._get_erf_list_url('https://%s.lianjia.com/ershoufang/%s/pg%d/' % (city_code, district_code, page_no))
            page_no = page_no + 1
            if (len(data_list) == 0):
                break
            result_list.extend(data_list)

        return pd.DataFrame(result_list)

    def _get_erf_list_url(self, url):
        response = self.do_request(url, None)
        soup = BeautifulSoup(response, "html5lib")
        divs = soup.find_all('div')

        data_list = []
        for div in divs:
            if div.has_attr('class') and 'content' in div['class']:
                sub_divs = div.find_all('div')
                for sub_div in sub_divs:
                    if sub_div.has_attr('class') and 'leftContent' in sub_div['class']:
                        uls = sub_div.find_all('ul')
                        for ul in uls:
                            if ul.has_attr('class') and 'sellListContent' in ul['class']:
                                items = ul.find_all('li')
                                for item in items:
                                    data = self._parse_item_content(item)
                                    data_list.append(data)

        return data_list

    def _parse_item_content(self, item):
        divs = item.find_all('div')
        for div in divs:
            if not div.has_attr('class'):
                continue
            div_class = div['class']

            if  'title' in div_class:
                id = div.a.attrs['data-housecode']
                title = div.a.text
            if  'houseInfo' in div_class:
                spans     = re.split('[/|]', div.text)
                name      = spans[0].strip()
                shape     = spans[1].strip()
                area      = spans[2].strip()
                direction = spans[3].strip()
                quality   = spans[4].strip()
                if (len(spans) >= 6):
                    elevator  = spans[5].strip()
                else:
                    elevator  = ""

            if 'positionInfo' in div_class:
                array = re.split('[)-/]',div.text)
                if len(array) >= 3:
                    floor    = array[0].strip()
                    building = array[1].strip()
                    location = array[2].strip()
                else:
                    floor    = array[0].strip()
                    building = array[0].strip()
                    location = array[1].strip()

            if  'totalPrice' in div_class:
                total_price =  div.text

            if 'unitPrice' in div_class:
                unit_price = div.text

        return {
            'id'         : id,
            "title"      : title,
            "name"       : name,
            "shape"      : shape,
            "area"       : area,
            "direction" : direction,
            "quality"   : quality,
            "elevator"  : elevator,
            "floor"     : floor,
            "building"  : building,
            "location"  : location,
            "total_price" : total_price,
            "unit_price"  : unit_price,
        }

