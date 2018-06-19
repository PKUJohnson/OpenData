# encoding: utf-8

from opendatatools.common import RestAgent
from progressbar import ProgressBar
import demjson
import json
import pandas as pd

fund_type = {
    "全部开放基金" :  {"t": 1, "lx": 1},
    "股票型基金"   :  {"t": 1, "lx": 2},
    "混合型基金"   :  {"t": 1, "lx": 3},
    "债券型基金"   :  {"t": 1, "lx": 4},
    "指数型基金"   :  {"t": 1, "lx": 5},
    "ETF联接基金"  :  {"t": 1, "lx": 6},
    "LOF基金"      :  {"t": 1, "lx": 8},
    "分级基金"     :  {"t": 1, "lx": 9},
    "FOF基金"      :  {"t": 1, "lx": 15},
    "理财基金"     :  {"t": 5},
    "分级A"        :  {"t": 6},
    "货币基金"     : {"t": 7},
}

class EastMoneyAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def _get_and_parse_js(self, url, prefix, param=None):
        response = self.do_request(url, param=param)
        if not response.startswith(prefix):
            return None
        else:
            return response[len(prefix):]

    def get_fund_company(self):
        url    = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=3'
        prefix = 'var gs='
        response = self._get_and_parse_js(url, prefix)
        if response is None:
            return None, '获取数据失败'

        jsonobj = demjson.decode(response)
        df = pd.DataFrame(jsonobj['op'])
        df.columns = ['companyid', 'companyname']
        return df, ''

    def _get_fund_list_onepage(self, company='', page_no = 1, page_size = 100):
        url    = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?page=%d,%d&gsid=%s' % (page_no, page_size, company)
        prefix = 'var db='
        response = self.do_request(url)
        response = self._get_and_parse_js(url, prefix)
        if response is None:
            return None, '获取数据失败'

        jsonobj = demjson.decode(response)
        rsp = jsonobj['datas']
        datestr = jsonobj['showday']
        df = pd.DataFrame(rsp)
        if len(df) > 0:
            df.drop(df.columns[5:], axis=1, inplace=True)
            df.columns = ['fundcode', 'fundname', 'pingyin', 'nav', 'accu_nav']
            df['date'] = datestr[0]
            return df, ''
        else:
            return None, ''

    def get_fundlist_by_company(self, companyid):
        page_no = 1
        page_size = 1000

        df_result = []
        while True:
            df, msg = self._get_fund_list_onepage(company=companyid, page_no=page_no, page_size=page_size)
            if df is not None:
                df_result.append(df)

            if df is None or len(df) < page_size:
                break
            page_no = page_no + 1

        if len(df_result) > 0:
            return pd.concat(df_result), ''
        else:
            return None, ''

    def get_fund_list(self):
        df_company, msg = self.get_fund_company()
        if df_company is None:
            return None, msg

        df_result = []
        process_bar = ProgressBar().start(max_value=len(df_company))
        for index, row in df_company.iterrows():
            companyid   = row['companyid']
            companyname = row['companyname']

            df, msg = self.get_fundlist_by_company(companyid)
            if df is not None:
                df['companyname'] = companyname
                df['companyid']   = companyid
                df_result.append(df)

            process_bar.update(index+1)

        return pd.concat(df_result), ''

    def get_fund_type(self):
        return fund_type.keys()

    def _get_fundlist_by_type_page(self, type, page_no = 1, page_size = 100):
        url    = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?page=%d,%d' % (page_no, page_size)
        prefix = 'var db='
        type_param = fund_type[type]

        response = self._get_and_parse_js(url, prefix, param=type_param)
        jsonobj = demjson.decode(response)
        rsp = jsonobj['datas']
        datestr = jsonobj['showday']
        df = pd.DataFrame(rsp)
        if len(df) > 0:
            df.drop(df.columns[5:], axis=1, inplace=True)
            df.columns = ['fundcode', 'fundname', 'pingyin', 'nav', 'accu_nav']
            df['date'] = datestr[0]
            return df, ''
        else:
            return None, '获取数据失败'

    def get_fundlist_by_type(self, type):
        if type not in fund_type:
            return None, '不正确的基金类型，请通过get_fund_type查询'
        type_param = fund_type[type]

        page_no = 1
        page_size = 1000
        df_result = []
        while True:
            df, msg = self._get_fundlist_by_type_page(type, page_no, page_size)
            if df is not None:
                df_result.append(df)

            if df is None or len(df)< page_size:
                break

            page_no = page_no + 1

        df = pd.concat(df_result)
        df['fund_type'] = type
        return df, ''

    def get_fund_nav(self, fund_code):
        url = 'http://api.fund.eastmoney.com/f10/lsjz'
        self.add_headers({'Referer': 'http://fund.eastmoney.com/f10/jjjz_%s.html' % fund_code})

        page_no   = 1
        page_size = 1000
        df_result = []
        while True:
            data = {
                'fundCode' : fund_code,
                'pageIndex': page_no,
                'pageSize' : page_size,
            }

            response = self.do_request(url, param=data)
            jsonobj = json.loads(response)
            err_code = jsonobj['ErrCode']
            err_msg  = jsonobj['ErrMsg']

            if err_code != 0:
                return None, err_msg

            rsp = jsonobj['Data']['LSJZList']
            df = pd.DataFrame(rsp)
            if len(df) > 0 :
                df_result.append(df)

            if len(df) < page_size:
                break

            page_no = page_no + 1

        df = pd.concat(df_result)
        df_ret = df[['FSRQ', 'DWJZ', 'LJJZ']]
        df_ret.columns = ['date', 'nav1', 'nav2']
        return df_ret, ''