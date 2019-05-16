# encoding: utf-8
from opendatatools.common import RestAgent
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime
import re


index_map={
    'SSEC'      :   '上证综合指数',
    'SZSC1'     :   '深证成份指数（价格）',
    'FTXIN9'    :   '富时中国A50指数',
    'DJSH'      :   '道琼斯上海指数',
    'HSI'       :   '香港恒生指数 (CFD)',
    'DJI'       :   '道琼斯工业平均指数',
    'SPX'       :   '美国标准普尔500指数 (CFD)',
    'IXIC'      :   '纳斯达克综合指数',
    'RUT'       :   '美国小型股2000 (CFD)',
    'VIX'       :   'VIX恐慌指数 (CFD)',
    'GSPTSE'    :   '加拿大多伦多S&P/TSX 综合指数 (CFD)',
    'BVSP'      :   '巴西IBOVESPA股指',
    'MXX'       :   'S&P/BMV IPC',
    'GDAXI'     :   '德国DAX30指数 (CFD)',
    'FTSE'      :   '英国富时100指数 (CFD)',
    'FCHI'      :   '法国CAC40指数',
    'STOXX50E'  :   '欧洲斯托克(Eurostoxx)50指数 (CFD)',
    'AEX'       :   '荷兰AEX指数',
    'IBEX'      :   '西班牙IBEX35指数 (CFD)',
    'FTMIB'     :   '意大利富时MIB指数 (CFD)',
    'SSMI'      :   '瑞士SWI20指数 (CFD)',
    'PSI20'     :   '葡萄牙PSI20指数',
    'BFX'       :   '比利时BEL20指数 (CFD)',
    'ATX'      :   'ATX',
    'OMXS30'      :   '瑞典OMX斯德哥尔摩30指数',
    'IMOEX'      :   '俄罗斯MOEX Russia指数',
    'IRTS'      :   '俄罗斯交易系统市值加权指数',
    'WIG20'      :   '波兰华沙WIG20指数',
    'BUX'      :   '匈牙利股票交易指数',
    'XU100'      :   '土耳其伊斯坦堡100指数',
    'TA35'      :   'TA 35',
    'TASI'      :   '沙特阿拉伯TASI指数',
    'N225'      :   '日经225指数 (CFD)',
    'AXJO'      :   '澳大利亚S&P/ASX200指数',
    'TWII'      :   '台湾加权指数',
    'SETI'      :   'SET Index',
    'KS11'      :   '韩国KOSPI指数',
    'JKSE'      :   '印尼雅加达综合指数',
    'NSEI'      :   '印度S&P CNX NIFTY指数',
    'BSESN'      :   '印度孟买30指数',
    'HNX30'      :   'HNX 30',
    'CSE'      :   '斯里兰卡科伦坡指数',
    'VIX'      :   'VIX恐慌指数 (CFD)',
    'FTXIN41350': '富时中国A600行业指数 - 化工制品',

}

index_map_inv = {v:k for k, v in index_map.items()}

class YingWeiAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        self.add_headers({'Referer': 'https://cn.investing.com/indices/shanghai-composite', 'X-Requested-With': 'XMLHttpRequest'})

    def get_major_index_list(self):
        url = "https://cn.investing.com/indices/major-indices"

        response = self.do_request(url)
        soup = BeautifulSoup(response, "html5lib")
        tables = soup.find_all('table')
        data_list = []
        for table in tables:
            if table.has_attr('id') and table['id'] == 'cr_12':
                trs = table.findAll("tr")
                for tr in trs:
                    if tr.has_attr('id'):
                        tds = tr.findAll('td')
                        time = datetime.datetime.fromtimestamp(int(tds[7]['data-value'])).strftime("%Y-%m-%d %H:%M:%S")
                        data_list.append({'index_name_cn': tr.a['title'],
                                          'index_name':  index_map_inv[tr.a['title']] if tr.a['title'] in index_map_inv else '',
                                          'country' : tds[0].span['title'],
                                          'last': tds[2].text,
                                          'high': tds[3].text,
                                          'low': tds[4].text,
                                          'price_change': tds[5].text,
                                          'percent_change': tds[6].text,
                                          'time' : time,
                                          })
        df = pd.DataFrame(data_list)
        return df, ''

    def _get_symbol(self, link):
        url = "https://cn.investing.com" + link
        response = self.do_request(url)
        soup = BeautifulSoup(response, "html5lib")
        divs = soup.find_all("div")
        for div in divs:
            if div.has_attr("class") and "instrumentHead" in div["class"]:
                text = div.h1.text
                symbol = re.split("[()]", text)[1]
                return symbol

        return ""

    def get_all_index_list(self):
        url = "https://cn.investing.com/indices/world-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"
        response = self.do_request(url)
        soup = BeautifulSoup(response, "html5lib")
        tables = soup.find_all('table')
        data = list()
        for table in tables:
            if (table.has_attr("id") and table["id"].startswith("indice_table_")):
                rows = table.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) <= 8:
                        continue
                    # id = row["id"][5:]
                    country = cols[0].span["title"]
                    instname = cols[1].a["title"]
                    url = cols[1].a["href"]
                    symbol = self._get_symbol(url)

                    item = {"country": country, "instname": instname, "symbol": symbol}#,, "investing.com.id" : id}
                    print(item)
                    data.append(item)

        df = pd.DataFrame(data)
        return df, ''

    def _get_id(self, symbol):
        url = "https://cn.investing.com/indices/world-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"
        response = self.do_request(url)
        soup = BeautifulSoup(response, "html5lib")
        tables = soup.find_all('table')
        for table in tables:
            if table.has_attr('id') and table["id"].startswith("indice_table_"):
                rows = table.findAll("tr")
                for row in rows:
                    if row.has_attr('id'):
                        if row.a['title'] == symbol:
                            return row['id'][5:]
        return None

    def get_index_data(self, symbol, interval, period):
        symbol = index_map[symbol]
        id = self._get_id(symbol)
        if id is None:
            return None, '暂不支持该指数'
        url = "https://cn.investing.com/common/modules/js_instrument_chart/api/data.php"
        param = {
            'pair_id': id,
            'pair_id_for_news': id,
            'chart_type': 'area',
            'pair_interval': interval,
            'candle_count': 120,
            'events': 'yes',
            'volume_series': 'yes',
            'period': period,
        }
        response = self.do_request(url, param=param, encoding='gzip')
        if response is not None:
            jsonobj = json.loads(response)
            df = pd.DataFrame(jsonobj['candles'])
            df.columns = ['time', 'close', '2', '3']
            df = df[['time', 'close']]
            df['time'] = df['time'].apply(lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
            return df, ''
        else:
            return None, 'error, no data'

    def get_index_data_id(self, id):
        url = "https://cn.investing.com/common/modules/js_instrument_chart/api/data.php"
        param = {
            'pair_id': id,
            'pair_id_for_news': id,
            'chart_type': 'area',
            'pair_interval': interval,
            'candle_count': 120,
            'events': 'yes',
            'volume_series': 'yes',
            'period': period,
        }
        response = self.do_request(url, param=param, encoding='gzip')
        if response is not None:
            jsonobj = json.loads(response)
            df = pd.DataFrame(jsonobj['candles'])
            df.columns = ['time', 'close', '2', '3']
            df = df[['time', 'close']]
            df['time'] = df['time'].apply(lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
            return df, ''
        else:
            return None, 'error, no data'
