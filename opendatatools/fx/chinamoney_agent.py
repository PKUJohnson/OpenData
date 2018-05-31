# encoding: utf-8

from opendatatools.common import RestAgent
import json
import pandas as pd

class ChinaMoneyAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    # cpr : central parity rate
    def get_hist_cny_cpr(self, start_date, end_date):
        url = 'http://www.chinamoney.com.cn/dqs/rest/dqs-u-fx-base/CcprHisNew'

        data = {
            'startDate' : start_date,
            'endDate'   : end_date,
        }

        response = self.do_request(url, data)
        rsp = json.loads(response)

        data = rsp['data']
        head = data['head']
        message = data['flagMessage']
        if len(message) > 0:
            return None, message
        else:
            records = rsp['records']
            row_data = []
            for rec in records:
                single_row = []
                single_row.append(rec['date'])
                single_row.extend(rec['values'])
                row_data.append(single_row)

            df = pd.DataFrame(row_data)
            columns = ['date']
            columns.extend(head)
            df.columns = columns
            return df, ""

    def get_cny_spot_price(self):
        url = 'http://www.chinamoney.com.cn/r/cms/www/chinamoney/data/fx/rfx-sp-quot.json'
        response = self.do_request(url, None)
        rsp = json.loads(response)
        time = rsp['data']['showDateCN']
        records = rsp['records']
        df = pd.DataFrame(records)
        df['time'] = time
        return df

    def get_realtime_shibor(self):
        url = 'http://www.chinamoney.com.cn/r/cms/www/chinamoney/data/shibor/shibor.json'
        response = self.do_request(url, None)
        rsp = json.loads(response)
        time = rsp['data']['showDateCN']
        records = rsp['records']
        df = pd.DataFrame(records)
        df['time'] = time
        return df

    def get_his_shibor(self, start_date, end_date):
        url = 'http://www.chinamoney.com.cn/ags/ms/cm-u-bk-shibor/ShiborHis'
        data = {
            'startDate' : start_date,
            'endDate'   : end_date,
        }

        response = self.do_request(url, data)
        rsp = json.loads(response)

        data = rsp['data']
        message = data['message']
        if len(message) > 0:
            return None, message
        else:
            records = rsp['records']
            df = pd.DataFrame(records)
            return df, ""
