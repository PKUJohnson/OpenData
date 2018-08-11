from opendatatools.common import RestAgent
import pandas as pd
import json

top_items_map = {
    '中国宏观' : "402273",
    '行业经济' : "771263",
    '国际宏观' : "1138921",
    '特色数据' : "632815",
    '市场行情' : 'RRP1349982',
    '公司数据' : 'RRP1',
}

class RoboAgent(RestAgent):

    def __init__(self):
        RestAgent.__init__(self)
        self.token = ""

    def _extract_result(self, response):
        jsonobj = json.loads(response)
        code = None
        message = None
        if "code" in jsonobj:
            code = jsonobj['code']

        if "message" in jsonobj:
            message = jsonobj['message']

        return code, message

    def _extract_content(self, response, key='content'):
        jsonobj = json.loads(response)

        if key in jsonobj:
            return jsonobj[key]

        return None

    def login(self, username, password):
        url = "https://app.datayes.com/server/usermaster/authenticate/v1.json"
        param = {
            'x-requested-with': 'XMLHttpRequest',
            'username' : username,
            'password' : password,
        }
        '''
        {"code":0,"message":"Success","content":{"result":"FAIL","userId":0,"principalName":"9957@wmcloud.com","tenantId":0,"accountId":0}}
        {"code":0,"message":"Success","content":{"result":"SUCCESS","userId":9957,"principalName":"9957@wmcloud.com","tenantId":0,"token":{"tokenString":"09FB012D0072D5E368F5BAB8B54C51B1","type":"WEB","expiry":1533996916631,"expired":false},"redirectUrl":"https://app.wmcloud.com/cloud-portal/#/portal","accountId":18975}}
       '''
        response = self.do_request(url, param=param, method='POST')
        if response is None:
            return None, '获取数据失败'

        code, message = self._extract_result(response)
        if code is None or code != 0:
            return False, "登录失败:" + message

        content = self._extract_content(response)
        if content is None:
            return False, "登录失败，没有返回content"

        result = content['result']
        if result == "FAIL":
            return False, "登录失败"

        tokenString = content['token']['tokenString']
        self.token = tokenString

        return True, "登录成功"

    def get_top_items(self):
        return top_items_map

    def get_sub_items(self, itemid):
        url = 'https://gw.datayes.com/rrp/web/supervisor/macro/%s' % itemid
        response = self.do_request(url)

        if response is None:
            return None, "获取数据失败"

        code, message = self._extract_result(response)
        if code is None or code != 1:
            return False, "获取数据失败:" + message

        data = self._extract_content(response, 'data')
        if data is None:
            return False, "获取数据失败，没有返回data"

        df = pd.DataFrame(data['childData'])
        return df, ""

    def get_series(self, seriesid):
        url = "https://gw.datayes.com/rrp/web/dataCenter/indic/%s?compare=false" % seriesid
        response = self.do_request(url, method='GET', encoding='gzip')
        if response is None:
            return None, None, "获取数据失败"

        code, message = self._extract_result(response)
        if code is None or code != 1:
            return None, None, "获取数据失败:" + message

        data = self._extract_content(response, 'data')
        if data is None:
            return None, None, "获取数据失败，没有返回data"

        df_data = pd.DataFrame(data['data'])
        info   = data['indic']
        return df_data, info, ""

