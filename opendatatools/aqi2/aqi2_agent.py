# encoding: UTF-8

from opendatatools.aqi2.util import *
import pandas as pd
import time
import json
import hashlib
import base64

from opendatatools.common import RestAgent
from bs4 import BeautifulSoup

class AQIStudyAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    # month format : yyyymm
    def get_hist_daily_aqi(self, city, month):
        url = "https://www.aqistudy.cn/historydata/api/historyapi.php"
        appid = "b73a4aaa989f54997ef7b9c42b6b4b29"
        method = "GETDAYDATA"
        timestamp = int(time.time() * 1000)
        # timestamp = 1563691657836
        clienttype = "WEB"
        object = {"city": city, "month": month}
        secret_key = appid + method + str(timestamp) + clienttype + "{\"city\":\"%s\",\"month\":\"%s\"}" % (
        object["city"], object["month"])
        secret = hashlib.md5(secret_key.encode("utf8")).hexdigest()
        param = {
            "appId": appid,
            "method": method,
            "timestamp": timestamp,
            "clienttype": clienttype,
            "object": object,
            "secret": secret
        }

        param = base64.standard_b64encode(json.dumps(param).encode("utf8")).decode()
        param = aes_encrypt(aes_client_key, aes_client_iv, param)

        response = self.do_request(url, param={"hd" : param}, method="POST")
        if response is None:
            return None, "获取数据失败"

        data = base64.standard_b64decode(response.encode("utf8")).decode()
        data = decrypt_response(des_key, des_iv, aes_server_key, aes_server_iv, data)

        jsonobj = json.loads(data)
        success = jsonobj["success"]
        errcode = jsonobj["errcode"]
        errmsg  = jsonobj["errmsg"]

        if errcode != 0:
            return None, errmsg

        result = jsonobj["result"]["data"]["items"]
        df = pd.DataFrame(result)
        if len(df) > 0:
            df.set_index("time_point", inplace=True)
        return df, ""

    def get_city_list(self):
        url = "https://www.aqistudy.cn/historydata/"
        response = self.do_request(url, method="GET")

        soup = BeautifulSoup(response, "html5lib")
        links = soup.find_all('a')

        data = {}
        for link in links:
            href = link["href"]
            if href.startswith("monthdata.php?city="):
                city = href.replace("monthdata.php?city=", "")
                data[city] = city
        return data

if __name__ == '__main__':
    aqi = AQIStudyAgent()
    city = aqi.get_city_list()
    print(city)
    #df, msg = aqi.get_hist_daily_aqi('北京市','201805')
    #print(df)
    #print(msg)