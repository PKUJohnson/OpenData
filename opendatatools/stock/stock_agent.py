# encoding: utf-8

from opendatatools.common import RestAgent
from opendatatools.common import date_convert
import json
import pandas as pd
import io

class SHExAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        headers = {
            "Accept": '*/*',
            'Referer': 'http://www.sse.com.cn/market/sseindex/indexlist/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        }
        self.add_headers(headers)

    def get_index_list(self):
        url = 'http://query.sse.com.cn/commonSoaQuery.do'
        data = {
            'sqlId': 'DB_SZZSLB_ZSLB',
        }

        response = self.do_request(url, data)
        rsp = json.loads(response)

        if 'pageHelp' in rsp:
            data = rsp['pageHelp']['data']
            return pd.DataFrame(data)
        else:
            return None

    def get_index_component(self, index):
        url = 'http://query.sse.com.cn/commonSoaQuery.do'
        data = {
            'sqlId': 'DB_SZZSLB_CFGLB',
            'indexCode' : index,
        }

        response = self.do_request(url, data)
        rsp = json.loads(response)

        if 'pageHelp' in rsp:
            data = rsp['pageHelp']['data']
            return pd.DataFrame(data)
        else:
            return None

    def get_dividend(self, code):
        url = 'http://query.sse.com.cn/commonQuery.do'
        data = {
            'sqlId' : 'COMMON_SSE_GP_SJTJ_FHSG_AGFH_L_NEW',
            'security_code_a' : code,
        }

        response = self.do_request(url, data)
        rsp = json.loads(response)

        if 'result' in rsp:
            data = rsp['result']
            return pd.DataFrame(data)
        else:
            return None

    def get_rzrq_info(self, date):
        url = 'http://www.sse.com.cn/market/dealingdata/overview/margin/a/rzrqjygk%s.xls' % (date)
        response = self.do_request(url, None, method='GET', type='binary')
        if response is not None:
            excel = pd.ExcelFile(io.BytesIO(response))
            df_total = excel.parse('汇总信息').dropna()
            df_detail = excel.parse('明细信息').dropna()
            df_total['date'] = date
            df_detail['date'] = date
            return df_total, df_detail
        else:
            return None, None

class SZExAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_index_list(self):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE'  : 'xls',
            'CATALOGID' : '1812',
        }

        response = self.do_request(url, data, method='GET', type='binary')
        df = pd.read_excel(io.BytesIO(response))
        return df

    def get_index_component(self, index):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE': 'xls',
            'CATALOGID': '1747',
            'ZSDM' : index
        }

        response = self.do_request(url, data, method='GET', type='binary')
        if response is not None:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None

    def get_rzrq_info(self, date):

        date = date_convert(date, '%Y%m%d', '%Y-%m-%d')

        df_total  = self._get_rzrq_total(date)
        df_detail = self._get_rzrq_detail(date)
        if df_total is not None:
            df_total['date'] = date
        if df_detail is not None:
            df_detail['date'] = date
        return df_total, df_detail

    def _get_rzrq_total(self, date):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE': 'xls',
            'CATALOGID': '1837_xxpl',
            'TABKEY' : 'tab1',
            "txtDate": date,
        }

        response = self.do_request(url, data, method='GET', type='binary')
        if response is not None and len(response) > 0:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None

    def _get_rzrq_detail(self, date):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE': 'xls',
            'CATALOGID': '1837_xxpl',
            'TABKEY': 'tab2',
            "txtDate" : date,
        }

        response = self.do_request(url, data, method='GET', type='binary')
        if response is not None and len(response) > 0:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None


class CSIAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_index_list(self):
        url = 'http://www.csindex.com.cn/zh-CN/indices/index'

        page = 1
        result_data = []
        while True:
            data = {
                "data_type" : "json",
                "page"       : page,
            }
            response = self.do_request(url, data, method='GET')
            rsp = json.loads(response)

            page = page + 1
            print("fetching data at page %d" % (page) )
            if "list" in rsp:
                result_data.extend(rsp['list'])
                if len(rsp['list']) == 0:
                    break
            else:
                return None

        return pd.DataFrame(result_data)

    def get_index_component(self, index):
        url = 'http://www.csindex.com.cn/uploads/file/autofile/cons/%scons.xls' % (index)

        response = self.do_request(url, None, method='GET', type='binary')
        if response is not None:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None