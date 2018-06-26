from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime

from opendatatools.common import RestAgent, get_current_day, date_convert

class HKExAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    @staticmethod
    def clear_text(text):
        return text.replace('\n', '').strip()

    # hongkong exchange 90000 -> 600000
    @staticmethod
    def process_code(market, text):
        code = HKExAgent.clear_text(text)
        if market == "SH":
            return "60" + code[1:] + ".SH"
        else:
            if code.startswith('77'):
                return "300" + code[2:] + ".SZ"
            else:
                return "00" + code[1:] + ".SZ"

    def get_lgt_share(self, market='SH', date = None):
        url = "http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=%s" % (market)

        today = get_current_day()
        if date is None:
            date = today

        search_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        year, month, day = search_date.year, search_date.month, search_date.day

        data = {
            'today' : date_convert(today, "%Y-%m-%d", "%Y%m%d"),
            'ddlShareholdingDay' : "%02d" % day,
            'ddlShareholdingMonth' : "%02d" % month,
            'ddlShareholdingYear' : year,
            'sortBy': '',
            'alertMsg': '',
            'btnSearch.x' : 23,
            'btnSearch.y' : 5,
        }
        aspx_param = self.get_aspx_param(url)
        data.update(aspx_param)

        self.add_headers({
            "Content-Type" : "application/x-www-form-urlencoded",
        })

        rsp = self.do_request(url, data, "POST")

        # 2. 开始解析返回数据，并从html中提取需要的内容
        data = list()
        soup = BeautifulSoup(rsp, "html5lib")
        divs = soup.find_all('div')

        result_date = ""
        for div in divs:
            if div.has_attr('id') and 'pnlResult' in div['id']:

                res_div = div.find_all('div')
                if (len(res_div)) > 0:
                    result_date = HKExAgent.clear_text(res_div[0].text)
                    result_date = result_date.replace("持股日期: ", "").strip()
                    result_date = date_convert(result_date, "%d/%m/%Y", "%Y-%m-%d")
                rows = div.table.findAll('tr')
                for row in rows:
                    cols = row.findAll('td')
                    if len(cols) == 4:
                        code = HKExAgent.clear_text(cols[0].text)
                        name = HKExAgent.clear_text(cols[1].text)
                        share_num  = HKExAgent.clear_text(cols[2].text)
                        percent = HKExAgent.clear_text(cols[3].text)
                        data.append({
                            "code": HKExAgent.process_code(market, code),
                            "name": name,
                            "share_num": share_num,
                            "percent": percent,
                            "date" : result_date,
                        })

        df = pd.DataFrame(data)
        return df