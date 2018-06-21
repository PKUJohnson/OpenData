# encoding: utf-8

import requests
from PIL import Image
import pytesseract
import io
import pandas as pd
from bs4 import BeautifulSoup

from opendatatools.common import RestAgent

dict_commodity_spot_indicator = {
    '65': '钢材指数',
    '61': '铁矿指数',
    '64': '焦炭指数',
    '1002': '煤炭指数',
    '1003': '水泥指数',
    '1100': 'FTZ指数',
    '118': '钢铁行业PMI指数',
    '119': '钢铁行业PMI生产指数',
    '120': '钢铁行业PMI新订单指数',
    '121': '钢铁行业PMI新出口订单指数',
    '122': '钢铁行业PMI产成品库存指数',
    '123': '钢铁行业PMI原材料库存指数',
    '74': '沪市终端线螺每周采购量监控',
    '72': '沪螺纹钢社会库存',
    '67': '国内螺纹钢社会库存量',
    '68': '国内线材社会库存量',
    '69': '国内主要城市热轧卷板库存',
    '70': '国内主要城市冷轧卷板库存',
    '73': '国内主要城市中厚板库存',
    '117': '全国主要钢材品种库存总量',
    '108': '热轧价格走势',
    '109': '冷轧价格走势',
    '110': '中板价格走势',
    '111': '型材价格走势',
    '127': '沪二级螺纹钢价格走势',
    '99': '重点企业粗钢日均产量（旬报）',
    '124': '重点企业钢材库存量（旬报）',
    '159': '国内月度粗钢日均产量',
    '35': '国内月度粗钢产量',
    '88': '国内月度钢材产量',
    '40': '国内月度螺纹钢产量',
    '41': '国内月度线材产量',
    '114': '国内月度热轧板卷产量',
    '115': '国内月度冷轧板卷产量',
    '116': '国内月度中厚板产量',
    '177': '国内月度生铁产量',
    '37': '国内月度焦炭产量',
    '36': '国内月度铁矿石原矿产量',
    '42': '国内月度铁矿石进口量',
    '38': '国内月度钢材出口量',
    '39': '国内月度钢材进口量',
    '43': '国内铁矿石港口存量',
    '161': '唐山地区钢坯库存量',
    '100': '印度矿港口库存',
    '77': '波罗的海干散货指数（BDI）',
    '78': '废钢价格走势',
    '79': '钢坯价格走势',
    '178': '钢材成本指数',
    '93': '铁矿石进口月度均价',
    '94': '巴西图巴朗-北仑铁矿海运价',
    '95': '西澳-北仑铁矿海运价',
    '1006': '澳大利亚粉矿价格（56.5%，日照港）',
    '106': '澳大利亚粉矿价格(61.5%青岛港，元/吨）',
    '107': '巴西粉矿价格（ 65% 日照港，元/吨）',
    '125': '62%铁矿石指数',
    '126': '63.5%印度粉矿外盘报价',
    '162': '全球粗钢月度产量（万吨）',
    '163': '全球粗钢日均产量（万吨）',
    '164': '全球粗钢产能利用率（%）',
}

class SpotAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    @staticmethod
    def clear_text(text):
        return text.replace('\n', '').strip()

    def get_captcha(self):
        url = 'http://www.96369.net/Other/ValidateCode.aspx'
        response = self.do_request(url, method='GET', type='binary')
        img = Image.open(io.BytesIO(response))
        img = img.convert('L')

        # 二值化
        threshold = 160
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        # 由于都是数字
        # 对于识别成字母的 采用该表进行修正
        rep = {'O': '0',
               'I': '1', 'L': '1',
               'Z': '2',
               'S': '8'
               }

        img = img.point(table, '1')
        img = img.convert('RGBA')
        rsp = pytesseract.image_to_string(img, config='-psm 6')
        try:
            answer = eval(rsp)
            return answer, self.get_cookies()
        except:
            return None, None

    def get_commodity_spot_indicator(self):
        df = pd.DataFrame.from_dict(dict_commodity_spot_indicator, orient='index')
        df.columns=['indicator_name']
        df = df.rename_axis('indicator_id').reset_index()
        return df

    def get_commodity_spot_indicator_data(self, indicator_id):
        url = 'http://www.96369.net/indices/%s' % indicator_id
        captcha, cookies = self.get_captcha()
        data = {
            'txtStartTime': '2000-01-01',
            'txtEndTime': '2018-06-21',
            'txtyzcode': captcha
        }
        response = self.do_request(url, param=data, cookies=cookies)

        if response is None:
            return None, '获取数据失败'

        soup = BeautifulSoup(response, "html5lib")
        divs = soup.find_all('div')

        data = []
        for div in divs:
            if div.has_attr('class') and 'wll-commodity' in div['class']:
                tables = div.find_all('table')

                for table in tables:
                    if table.has_attr('class') and 'mod_tab' in table['class']:
                        rows = table.findAll('tr')
                        for row in rows:
                            cols = row.findAll('td')
                            if len(cols) == 4:
                                date = SpotAgent.clear_text(cols[0].text)
                                value = SpotAgent.clear_text(cols[1].text)
                                change = SpotAgent.clear_text(cols[2].text)
                                chg_pct = SpotAgent.clear_text(cols[3].text)

                                data.append({
                                    "date": date,
                                    "value": value,
                                    "change": change,
                                    "chg_pct": chg_pct,
                                })

        return pd.DataFrame(data), ''

