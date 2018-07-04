# encoding: utf-8

from opendatatools.common import RestAgent
from bs4 import BeautifulSoup
from progressbar import ProgressBar

import pandas as pd
import re

lianjia_city_map = {
    '北京市' : 'bj',
    '上海市' : 'sh',
}

district_map = {
    '东城':'dongcheng',
    '西城':'xicheng',
    '朝阳':'chaoyang',
    '海淀':'haidian',
    '丰台':'fengtai',
    '石景山':'shijingshan',
    '通州':'tongzhou',
    '昌平':'changping',
    '大兴':'daxing',
    '亦庄':'yizhuangkaifaqu',
    '顺义':'shunyi',
    '房山':'fangshan',
    '门头沟':'mentougou',
    '平谷':'pinggu',
    '怀柔':'huairou',
    '密云':'miyun',
    '延庆':'yanqing',

    '浦东': 'pudong',
    '闵行': 'minhang',
    '宝山': 'baoshan',
    '徐汇': 'xuhui',
    '普陀': 'putuo',
    '杨浦': 'yangpu',
    '长宁': 'changning',
    '松江': 'songjiang',
    '嘉定': 'jiading',
    '黄浦': 'huangpu',
    '静安': 'jingan',
    '闸北': 'zhabei',
    '虹口': 'hongkou',
    '青浦': 'qingpu',
    '奉贤': 'fengxian',
    '金山': 'jinshan',
    '崇明': 'chongming',
}


class LianjiaAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_city_list(self):
        return lianjia_city_map.keys()

    def get_district_list(self):
        return district_map.keys()

    @staticmethod
    def clear_text(text):
        return text.replace('\n', '').strip()

    def get_esf_list(self, city, max_page_no):
        if max_page_no>100:
            max_page_no = 100
        if city in lianjia_city_map:
            city_code = lianjia_city_map[city]
            return self._get_esf_list(city_code, max_page_no)

    def get_esf_list_by_distinct(self, city, distinct, max_page_no):
        if max_page_no>100:
            max_page_no = 100

        if city in lianjia_city_map:
            city_code = lianjia_city_map[city]

        if distinct in district_map:
            distinct_code = district_map[distinct]

        return self._get_esf_list_by_distinct(city_code, distinct_code, max_page_no)

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

    def _get_esf_list_by_distinct(self, city_code, distinct_code, max_page_no):
        page_no = 1
        result_list = []
        process_bar = ProgressBar().start(max_value=max_page_no)
        while page_no <= max_page_no:
            process_bar.update(page_no)
            #print('getting data from lianjia.com for page %d' % page_no)
            data_list = self._get_erf_list_url('https://%s.lianjia.com/ershoufang/%s/pg%d/' % (city_code, distinct_code, page_no))
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

