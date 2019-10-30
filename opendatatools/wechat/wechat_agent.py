from opendatatools.common import RestAgent
import hashlib
import json
from PIL import Image
from io import BytesIO
import random
import time
import urllib
import pandas as pd
import math
import datetime
import threading
import functools


Host = "mp.weixin.qq.com"
agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
refer = "https://mp.weixin.qq.com"
xrw = "XMLHttpRequest"

loginUrl = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin"
qrcodeUrl = "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300&rd=120"
checkLogin = "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&f=json&ajax=1&random="
doLogin = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login"
searchUrl = "https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&needToken&lang=zh_CN&f=json&ajax=1&needRandom&needQuery&begin=0&count=5"
appmsg = "https://mp.weixin.qq.com/cgi-bin/appmsg?needToken&lang=zh_CN&f=json&ajax=1&needRandom&action=list_ex&needBegin&needCount&query=&needFakeid&type=9" # 原9,改为1后条数变多

def md5(data):
    m = hashlib.md5()
    m.update(data.encode(encoding='UTF-8'))
    return m.hexdigest()


def ReqRandom():
    ll = random.random() * 100000000000000000
    result = "0." + str(ll)
    return result

class WechatMPAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def login(self, username, password):
        param = {
            "username": username,
            "pwd": md5(password),
            "imgcode": "",
            "f": "json"
        }

        self.add_headers({
            "Referer" : "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=validate&lang=zh_CN&account=PKUJohnson@163.com",
            "Host" : Host,
            "X-Requested-With" : xrw
        })

        resp = self.do_request(loginUrl, method="POST", param=param)
        print(resp)
        redirect_url = json.loads(resp)["redirect_url"]

        response = self.do_request(qrcodeUrl, method="GET", type="binary")
        qrcode = Image.open(BytesIO(response))
        qrcode.show()

        # Check if qrcode is verified
        while True:
            response = self.do_request(checkLogin+ReqRandom(), method="GET")
            rsp = json.loads(response)

            if rsp["status"] == 1:
                qrcode.close()
                break
            else:
                time.sleep(2)

        param = {
            "userlang": "zh_CN",
            "token": "",
            "lang": "zh_CN",
            "f" : "json",
            "ajax" : "1",

        }

        response = self.do_request(doLogin, method="POST", param=param)
        rsp = json.loads(response)
        print(rsp)
        token_url = rsp["redirect_url"]
        pos = token_url.find("token=")
        token = token_url[pos+6:]
        self.token = token
        return True

    def get_retcode(self, rsp):
        if "base_resp" in rsp and "ret" in rsp["base_resp"] and "err_msg" in rsp["base_resp"]:
            return rsp["base_resp"]["ret"], rsp["base_resp"]["err_msg"]
        return 0, "ok"

    def search_pub(self, pubno):
        _searchUrl = searchUrl.replace("needToken", "token=" + self.token).replace("needRandom", "random=" + ReqRandom()).replace("needQuery", "query=" + pubno)
        response = self.do_request(_searchUrl, method="GET")
        rsp = json.loads(response)
        ret, err_msg = self.get_retcode(rsp)
        if ret != 0:
            return None, err_msg
        df = pd.DataFrame(rsp["list"])
        return df, ""

    def get_article_list(self, fakeid, begin):
        count = 5
        _appmsg = appmsg.replace("needToken", "token=" + self.token).replace("needRandom", "random=" + ReqRandom()).replace("needFakeid", "fakeid=" + fakeid)
        appmsgTemp = _appmsg.replace("needBegin", "begin=" + str(begin)).replace("needCount", "count=" + str(count))

        response = self.do_request(appmsgTemp, method="GET")
        rsp = json.loads(response)
        ret, msg = self.get_retcode(rsp)
        # 失败后60秒再试一次
        while msg != "ok":
            print(response.text)
            time.sleep(60)
            response = self.do_request(appmsgTemp, method="GET")
            rsp = json.loads(response.text)
            ret, msg = self.get_retcode(rsp)

        app_msg_cnt = rsp["app_msg_cnt"]
        app_msg_list = rsp["app_msg_list"]
        df = pd.DataFrame(app_msg_list)
        return app_msg_cnt, df

