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
        url = "https://wows-api.wallstreetcn.com/v3/aioria/plates/rank?count=10000&is_asc=true&rank_type=core_pcp_rank"
        response = self.do_request(url, method="GET")
        if response is not None:
            rsp = json.loads(response)
            cols = rsp["data"]['fields']
            items = rsp["data"]['items']
            df = pd.DataFrame(items)
            df.columns = cols
            return df, ""
        else:
            return None, "获取数据失败"

    def get_theme_stock(self, tid):
        url = "https://wows-api.wallstreetcn.com/v3/aioria/sset/bankuaiji?id=%d&terminal=pc" % tid
        self.add_headers({
            "X-Appgo-Token" : self.token
        })
        response = self.do_request(url, method="GET")
        if response is not None:
            rsp = json.loads(response)
            login_flag = rsp["data"]["login_flag"]
            if login_flag == True:
                stocks = rsp["data"]['stocks']
                df = pd.DataFrame(stocks)
                return df, ""
            else:
                return None, "请首先登录 login"
        else:
            return None, "获取数据失败"

    def get_theme_kline(self, tid):
        url = "https://wows-api.wallstreetcn.com/v3/aioria/index/kline?prod_code=%s&data_count=10000" % tid
        response = self.do_request(url, method="GET")
        if response is not None:
            rsp = json.loads(response)
            data = rsp["data"]["candle"][str(tid)]
            cols = rsp["data"]["candle"]["fields"]
            df = pd.DataFrame(data)
            df.columns = cols
            df["min_time"] = df["min_time"].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d"))
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
