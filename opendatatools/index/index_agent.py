# encoding: utf-8
from opendatatools.common import RestAgent
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime


index_map={
    'SSEC'      :   '上证指数',
    'SZSC1'     :   '深证成份指数',
    'FTXIN9'    :   '富时中国A50',
    'DJSH'      :   'DJ Shanghai',
    'HSI'       :   '恒生指数',
    'DJI'       :   '道琼斯指数',
    'SPX'       :   '标普500指数',
    'IXIC'      :   '纳斯达克综合指数',
    'RUT'       :   '美国小型股2000',
    'VIX'       :   'S&P 500 VIX',
    'GSPTSE'    :   '多伦多S&P/TSX',
    'BVSP'      :   '巴西IBOVESPA',
    'MXX'       :   'S&P/BMV IPC',
    'GDAXI'     :   '德国DAX30',
    'FTSE'      :   '英国富时100',
    'FCHI'      :   '法国CAC40',
    'STOXX50E'  :   '欧洲斯托克50',
    'AEX'       :   '荷兰AEX',
    'IBEX'      :   '西班牙IBEX35',
    'FTMIB'     :   '意大利富时MIB',
    'SSMI'      :   '瑞士SWI20',
    'PSI20'     :   '葡萄牙PSI20',
    'BFX'       :   '比利时BEL20',
    'ATX'      :   'ATX',
    'OMXS30'      :   '瑞典OMX30',
    'IMOEX'      :   '俄罗斯MOEX',
    'IRTS'      :   '俄罗斯市值加权指数',
    'WIG20'      :   '波兰WIG20',
    'BUX'      :   '匈牙利BUX',
    'XU100'      :   '土耳其ISE National-100',
    'TA35'      :   'TA 35',
    'TASI'      :   '沙特TASI',
    'N225'      :   '日经225',
    'AXJO'      :   '澳大利亚S&P/ASX200',
    'TWII'      :   '台湾加权指数',
    'SETI'      :   'SET',
    'KS11'      :   '韩国KOSPI',
    'JKSE'      :   '印尼综合指数',
    'NSEI'      :   '印度S&P CNX NIFTY',
    'BSESN'      :   '印度BSE SENSEX',
    'HNX30'      :   'HNX 30',
    'CSE'      :   '斯里兰卡CSE',
}

index_map_inv = {v:k for k, v in index_map.items()}

class YingWeiAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        self.add_headers({'Referer': 'https://cn.investing.com/indices/shanghai-composite', 'X-Requested-With': 'XMLHttpRequest'})

    def get_index_list(self):
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
                        tds = tr.findAll('td')[2:]
                        time = datetime.datetime.fromtimestamp(int(tds[5]['data-value'])).strftime("%Y-%m-%d %H:%M:%S")
                        data_list.append({'index_name_cn': tr.a.text,
                                          'index_name': index_map_inv[tr.a.text],
                                          'last': tds[0].text,
                                          'high': tds[1].text,
                                          'low': tds[2].text,
                                          'price_change': tds[3].text,
                                          'percent_change': tds[4].text,
                                          'time' : time,
                                          })
        df = pd.DataFrame(data_list)
        return df, ''

    def _get_id(self, symbol):
        url = "https://cn.investing.com/indices/major-indices"
        response = self.do_request(url)
        soup = BeautifulSoup(response, "html5lib")
        tables = soup.find_all('table')
        for table in tables:
            if table.has_attr('id') and table['id'] == 'cr_12':
                rows = table.findAll("tr")
                for row in rows:
                    if row.has_attr('id'):
                        if row.a.text == symbol:
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


