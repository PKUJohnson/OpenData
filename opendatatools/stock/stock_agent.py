# encoding: utf-8

from opendatatools.common import RestAgent
import json
import pandas as pd
import io
import xlrd

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