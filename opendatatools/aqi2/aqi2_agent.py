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

    # date format : yyyy-mm-dd
    def get_daily_hour_aqi(self, city, date):
        startTime = "%s 00:00:00" % date
        endTime   = "%s 23:59:59" % date
        return self.get_server_data(city, "HOUR", startTime, endTime)

    def get_hist_daily_aqi(self, city, begindate, enddate):
        startTime = "%s 00:00:00" % begindate
        endTime   = "%s 23:59:59" % enddate
        return self.get_server_data(city, "DAY", startTime, endTime)

    def get_server_data(self, city, type, startTime, endTime):
        url = "https://www.aqistudy.cn/apinew/aqistudyapi.php"
        appid = "1a45f75b824b2dc628d5955356b5ef18"
        method = "GETDETAIL"
        timestamp = int(time.time() * 1000)
        clienttype = "WEB"
        object = {"city": city, "type": type, "startTime" : startTime, "endTime" : endTime }
        secret_key = appid + method + str(timestamp) + clienttype + "{\"city\":\"%s\",\"endTime\":\"%s\",\"startTime\":\"%s\",\"type\":\"%s\"}" % (
            object["city"], object["endTime"], object["startTime"], object["type"]
        )
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
        param = aes_encrypt(real_aes_client_key, real_aes_client_iv, param)

        response = self.do_request(url, param={"d" : param}, method="POST")
        if response is None:
            return None, "获取数据失败"

        #data = base64.standard_b64decode(response.encode("utf8")).decode()
        data = decrypt_response(real_des_key, real_des_iv, real_aes_server_key, real_aes_server_iv, response)

        jsonobj = json.loads(data)
        success = jsonobj["success"]
        errcode = jsonobj["errcode"]
        errmsg  = jsonobj["errmsg"]

        if errcode != 0:
            return None, errmsg

        result = jsonobj["result"]["data"]["rows"]
        df = pd.DataFrame(result)
        if len(df) > 0:
            df.set_index("time", inplace=True)
        return df, ""

    # type : "DAY", "HOUR
    def get_api_map(self, type, timepoint):
        url = "https://www.aqistudy.cn/apinew/aqistudyapi.php"
        appid = "1a45f75b824b2dc628d5955356b5ef18"
        method = "GETMAPDATA"
        timestamp = int(time.time() * 1000)
        clienttype = "WEB"
        object = {"type": type, "timepoint" : timepoint  }
        secret_key = appid + method + str(timestamp) + clienttype + "{\"timepoint\":\"%s\",\"type\":\"%s\"}" % (
            object["timepoint"], object["type"]
        )
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
        param = aes_encrypt(real_aes_client_key, real_aes_client_iv, param)

        response = self.do_request(url, param={"d" : param}, method="POST")
        if response is None:
            return None, "获取数据失败"

        #data = base64.standard_b64decode(response.encode("utf8")).decode()
        data = decrypt_response(real_des_key, real_des_iv, real_aes_server_key, real_aes_server_iv, response)

        jsonobj = json.loads(data)
        success = jsonobj["success"]
        errcode = jsonobj["errcode"]
        errmsg  = jsonobj["errmsg"]

        if errcode != 0:
            return None, errmsg

        result = jsonobj["result"]["data"]["rows"]
        df = pd.DataFrame(result)
        if len(df) > 0:
            df.set_index("time", inplace=True)
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
    #city = aqi.get_city_list()
    #print(city)

    #df, msg = aqi.get_daily_hour_aqi('北京', '2019-07-22')
    #print(df)
    #print(msg)

    #df, msg = aqi.get_hist_daily_aqi('北京','2018-05-01', '2019-05-01')
    #print(df)
    #print(msg)

    param = "tdgHOYxwKdDSgYXe+RLPzYCgLvrddahasI5XXklB4gVLYqab+XRPpMD/oSqnJ/aEmFwzVEUhLnPzRy03+X1BI7EP40t1A25axHw6XgQEwrMCA8LPhIJdpk3JqlHQwF/0lHvOCRXiksQ2gxlp8zXTAHX2NeaTAHQeAHVjfS2WSo59EEsCNxnpiBc9JH6WSot2V5FpFF1Z0ElMw4F5ts9OERUzyzCtS80roZmhfEN2sQMsQdt+8keJnsk56MDt1HG9THFJI56TYqd+cFcfcjv5UXDQqjBrttIwXzTYLmMVW0ALdQH4MsmIyMsxiHPYMsto6FJWs/7Jh3L3giRN0yVlF8mW73XSkAsiW/aCRcua8psHxI4f5lyG1a2owB5CZS/FMCM3OHeSvmebXVLrPfOeWA=="
    result = aes_decrypt(real_aes_client_key, real_aes_client_iv, param)
    result = base64.standard_b64decode(result).decode()
    print(result)

    #df, msg = aqi.get_real_aqi_map("HOUR", "2019-07-22 08:00:00")
    #print(df)

    df, msg = aqi.get_api_map("DAY", "2019-07-21")
    print(df)
