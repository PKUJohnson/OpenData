# encoding: utf-8

from opendatatools.common import RestAgent
import json
import datetime
import io
import pandas as pd

class XuangubaoAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        self.token = None
        self.add_headers({
            "x-appgo-platform" : "device=pc",
            "referer" : "https://xuangubao.cn/zhutiku",
            "origin": "https://xuangubao.cn",
        })

    def login(self, username, password):
        url = "https://api.xuangubao.cn/api/account/mobile_login"
        data = {
            'Mobile'   : username,
            'Password' : password,
        }

        response = self.do_request(url, param = json.dumps(data), method="POST")
        if response is not None:
            rsp = json.loads(response)
            self.token = rsp["Token"]
            self.add_headers({
                "token" : self.token
            })
            return True
        else:
            return False

    def get_theme(self):
        url = "https://flash-api.xuangubao.cn/api/plate/rank?count=10000&is_asc=true&field=core_avg_pcp"
        response = self.do_request(url, method="GET")
        if response is not None:
            rsp = json.loads(response)
            data = rsp["data"]
            plates = ",".join([str(x) for x in data])
            url_info = "https://flash-api.xuangubao.cn/api/plate/data?fields=core_avg_pcp,plate_name,plate_id&plates=%s" % plates

            response_info = self.do_request(url_info, method="GET")
            if response_info is not None:
                rsp_info = json.loads(response_info)
                info = rsp_info["data"]
                df = pd.DataFrame(info).T
                df.columns = ["core_avg_pcp", "plate_id", "plate_name"]
                return df, ""
        else:
            return None, "获取数据失败"

    def get_theme_stock(self, tid):
        url = "https://flash-api.xuangubao.cn/api/plate/plate_set?id=%s" % tid
        self.add_headers({
            "X-Appgo-Token" : self.token
        })
        response = self.do_request(url, method="GET")
        if response is not None:
            rsp = json.loads(response)
            stocks = rsp["data"]['stocks']
            df = pd.DataFrame(stocks)
            return df, ""
        else:
            return None, "获取数据失败"

    def get_theme_kline(self, tid):
        url = "https://flash-api.xuangubao.cn/api/plate/index_history?plate_id=%s&index_type=1&data_count=10000" % tid
        response = self.do_request(url, method="GET")
        if response is not None:
            rsp = json.loads(response)
            data = rsp["data"]
            df = pd.DataFrame(data)
            df["date_time"] = df["date_time"].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d"))
            return df, ""
        else:
            return None, "获取数据失败"

    def get_theme_event_onepage(self, tid, tail):
        url = "https://api.xuangubao.cn/api/pc/bkjMsgs/%d?limit=50&TailMark=%d" % (tid, tail)
        response = self.do_request(url, method="GET")
        if response is not None:
            rsp = json.loads(response)
            data = rsp["Messages"]
            TailMark = int(rsp["TailMark"])
            df = pd.DataFrame(data)
            if len(df) > 0:
                return df, TailMark

        return None, 0

    def get_theme_event(self, tid):
        df_list = []
        tail = 0
        while True:
            df, tail = self.get_theme_event_onepage(tid, tail)
            if df is not None:
                df_list.append(df)
            else:
                break

        if len(df_list)>1:
            df = pd.concat(df_list)
            df["CreatedAt"] = df["CreatedAt"].apply(lambda x : datetime.datetime.fromtimestamp(x))
            df["UpdatedAt"] = df["UpdatedAt"].apply(lambda x : datetime.datetime.fromtimestamp(x))
            df["ManualUpdatedAt"] = df["ManualUpdatedAt"].apply(lambda x : datetime.datetime.fromtimestamp(x))
            df = df.set_index("Id")
            return df, ""

        return None, "获取数据失败"
