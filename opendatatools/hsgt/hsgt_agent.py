# encoding: utf-8

from opendatatools.common import RestAgent
import pandas as pd
import json

class EastMoneyAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    # direct： north, south
    def _get_realtime_moneyflow(self, direct):
        url = 'http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?id=%s&type=EFR&rtntype=2&acces_token=1942f5da9b46b069953c873404aad4b5&js={"data":[(x)]}' % direct
        response = self.do_request(url)
        if response is None:
            return None

        jsonobj = json.loads(response)
        result = []
        for data in jsonobj['data']:
            items = data.split(',')
            if (items[1] == ''):
                break
            result.append({
                'time' : items[0],
                'hgtzj': items[1],
                'sgtzj': items[2],
                'hgtye': items[3],
                'sgtye': items[4],
            })
        return pd.DataFrame(result)

    def get_realtime_moneyflow(self):
        directs = ['north', 'south']
        df_data = []
        for direct in directs:
            df = self._get_realtime_moneyflow(direct)
            df['direct'] = direct
            if df is not None:
                df_data.append(df)

        if len(df_data) > 0:
            return pd.concat(df_data), ''

        return None, '获取数据失败'

    def get_hist_moneyflow(self):
        url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTZJZS&token=70f12f2f4f091e459a279469fe49eca5&js={"data":(x)}'
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        jsonobj = json.loads(response)
        df = pd.DataFrame(jsonobj['data'])
        return df, ''

    def _get_his_tradestat_onepage(self, markettype, page_no):
        url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=%d)&js={"data":(x)}&ps=500&p=%d' % (markettype, page_no)
        response = self.do_request(url)
        if response is None:
            return None

        jsonobj = json.loads(response)
        return pd.DataFrame(jsonobj['data'])

    def get_his_tradestat(self, markettype):
        page_no = 1
        df_data = []
        while True:
            df = self._get_his_tradestat_onepage(markettype, page_no)
            if df is None:
                return None, '获取数据失败'
            if len(df) > 0:
                df_data.append(df)

            if len(df) < 500:
                break

            page_no = page_no + 1

        if len(df_data) == 0:
            return None, '获取数据失败'

        return pd.concat(df_data), ''

    def get_ah_compare(self):
        url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&p=1&ps=1000&sty=FCABHL&cmd=C._AHH&js={"data":[(x)]}'
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        jsonobj = json.loads(response)
        result = []
        for data in jsonobj['data']:
            items = data.split(',')
            result.append({
                "hshare_code" : items[1],
                'hshare_name' : items[2],
                'hshare_last' : items[3],
                'hshare_chg'  : items[4],
                "ashare_code" : items[5],
                'ashare_name' : items[7],
                'ashare_last' : items[8],
                'ashare_chg'  : items[9],
                'ah_ratio'    : items[13],
            })
        df = pd.DataFrame(result)
        return df, ''