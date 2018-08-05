# encoding: utf-8

import json
import pandas as pd
import datetime
from opendatatools.common import RestAgent

class EastMoneyAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

        self.index_code = {
            'BDI' : ('EMI00107664', '波罗的海干散货指数'),
            'BPI' : ('EMI00107665', '巴拿马型运费指数'),
            'BCI' : ('EMI00107666', '海岬型运费指数'),
            'BSI' : ('EMI00107667', '超灵便型船运价指数'),
            'BDTI': ('EMI00107668', '原油运输指数'),
            'BCTI': ('EMI00107669', '成品油运输指数'),
        }

    def get_index_list(self):
        index_list = []
        for index, (code, name) in self.index_code.items():
            index_list.append({'index' : index, 'name' : name})

        return pd.DataFrame(index_list), ''

    def _get_index(self, url):
        page_no = 1
        df_list = []
        while True:
            page_url = url + '&p=%d&ps=1000' % page_no
            response = self.do_request(page_url)
            if response is None:
                return None, '获取数据失败'

            jsonobj = json.loads(response)
            df = pd.DataFrame(jsonobj['data'])
            df_list.append(df)

            if len(df) < 1000:
                break

            page_no = page_no + 1

        df_result = pd.concat(df_list)[['DATADATE', 'VALUE']]
        df_result['DATADATE'] = df_result['DATADATE'].apply(lambda x : datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'))

        return df_result, ''

    def get_index_data(self, index):
        base_url  = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=HYZS_PageStock&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID='%s')&st=DATADATE&js={\"pages\":(tp),\"data\":(x)}"
        index_url = base_url % self.index_code[index][0]
        return self._get_index(index_url)

