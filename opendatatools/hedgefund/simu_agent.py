from opendatatools.common import RestAgent, md5
from progressbar import ProgressBar
import json
import pandas as pd
import time
import hashlib

class SimuAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        self.user_info = None
        self.df_fundlist = None
        self.cookies = None

    def login(self, username, password):
        url = 'https://passport.simuwang.com/index.php?m=Passport&c=auth&a=login&type=login&name=%s&pass=%s&reme=1&rn=1' % (username, password)
        self.add_headers({'Referer': 'https://dc.simuwang.com/'})
        response = self.do_request(url)
        if response is None:
            return None, '登录失败'

        jsonobj = json.loads(response)
        suc = jsonobj['suc']
        msg = jsonobj['msg']

        if suc != 1:
            return None, msg

        self.cookies = self.get_cookies()

        self.user_info = jsonobj['data']
        return self.user_info, msg

    def prepare_cookies(self, url):
        response = self.do_request(url, None)
        if response is not None:
            cookies = self.get_cookies()
            return cookies
        else:
            return None

    def _get_rz_token(self, time):
        mk = time * 158995555893
        mtoken = md5(md5(str(mk))) + '.' + str(time)
        return mtoken

    def _get_fund_list_page(self, page_no):
        url = 'https://dc.simuwang.com/ranking/get?page=%s&condition=fund_type:1,6,4,3,8,2;ret:9;rating_year:1;istiered:0;company_type:1;sort_name:profit_col2;sort_asc:desc;' % page_no
        response = self.do_request(url)

        if response is None:
            return None, '获取数据失败', None

        jsonobj = json.loads(response)

        code = jsonobj['code']
        msg  = jsonobj['msg']

        if code != 1000:
            return None, msg, None

        df = pd.DataFrame(jsonobj['data'])
        pageinfo = jsonobj['pager']
        return df, '', pageinfo

    def load_data(self):
        page_no = 1
        df_list = []
        df, msg, pageinfo = self._get_fund_list_page(page_no)
        if df is None:
            return None, msg

        df_list.append(df)
        page_count = pageinfo['pagecount']
        process_bar = ProgressBar().start(max_value=page_count)

        page_no = page_no + 1
        while page_no < page_count:
            df, msg, pageinfo = self._get_fund_list_page(page_no)
            if df is None:
                return None, msg
            df_list.append(df)
            process_bar.update(page_no)
            page_no = page_no + 1

        self.df_fundlist = pd.concat(df_list)
        return self.df_fundlist, ''

    def get_fund_list(self):
        if self.df_fundlist is None:
            return None, '请先加载数据 load_data'

        return self.df_fundlist, ''

    def _get_sign(self, url, params):
        str = url
        for k,v in params.items():
            str = str + k + params[k]

        sha1 = hashlib.sha1()
        sha1.update(str.encode('utf8'))
        sign = sha1.hexdigest()

        return sign

    def _get_token(self, fund_id):
        sign = self._get_sign('https://dc.simuwang.com/Api/getToken', {'id' : fund_id})
        url = 'https://dc.simuwang.com/Api/getToken?id=%s&sign=%s' % (fund_id, sign)
        self.add_headers({'Referer': 'https://dc.simuwang.com/'})
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        jsonobj = json.loads(response)
        code = jsonobj['code']
        msg  = jsonobj['message']

        if code != 1000 :
            return code, msg

        self.cookies.update(self.get_cookies())

        salt = jsonobj['data']

        muid = self.user_info['userid']
        #str = 'id%smuid%spage%s%s' % (fund_id, muid, page_no, salt)
        str = '%s%s' % (fund_id, salt)
        sha1 = hashlib.sha1()
        sha1.update(str.encode('utf8'))
        token = sha1.hexdigest()

        return token, ''

    def _get_fund_nav_page(self, fund_id, page_no):
        muid = self.user_info['userid']
        token, msg = self._get_token(fund_id)
        if token is None:
            return None, '获取token失败: ' + msg

        url = 'https://dc.simuwang.com/fund/getNavList.html'
        self.add_headers({'Referer': 'https://dc.simuwang.com/product/%s' % fund_id})
        data = {
            'id'   : fund_id,
            'muid' : muid,
            'page' : str(page_no),
            'token': token,
        }
        response = self.do_request(url, param=data, cookies=self.cookies)
        if response is None:
            return None, '获取数据失败', ''

        jsonobj = json.loads(response)
        code = jsonobj['code']
        msg  = jsonobj['msg']

        if code != 1000 :
            return code, msg, ''

        df = pd.DataFrame(jsonobj['data'])
        pageinfo = jsonobj['pager']
        return df, '', pageinfo

    def _bit_encrypt(self, str, key):
        cryText = ''
        keyLen = len(key)
        strLen = len(str)
        for i in range(strLen):
            k = i % keyLen
            cryText = cryText + chr(ord(str[i]) - k)

        return cryText

    def _decrypt_data(self, str):
        return self._bit_encrypt(str, 'cd0a8bee4c6b2f8a91ad5538dde2eb34')

    def get_fund_nav(self, fund_id):

        if self.user_info is None:
            return None, '请先登录'

        page_no = 1
        df_list = []
        df, msg, pageinfo = self._get_fund_nav_page(fund_id, page_no)
        if df is None:
            return None, msg

        df_list.append(df)
        page_count = pageinfo['pagecount']

        page_no = page_no + 1
        while page_no < page_count:
            try_times = 1
            while try_times <= 3:
                df, msg, pageinfo = self._get_fund_nav_page(fund_id, page_no)
                if df is None:
                    if  try_times > 3:
                        return None, msg
                    else:
                        try_times = try_times + 1
                        continue
                else:
                    df_list.append(df)
                    break
            page_no = page_no + 1

        df_nav = pd.concat(df_list)
        df_nav.drop('c', axis=1, inplace=True)
        df_nav.rename(columns={'d': 'date', 'n': 'nav', 'cn' : 'accu_nav', 'cnw' : 'accu_nav_w'}, inplace=True)

        # 这个网站搞了太多的小坑
        df_nav['nav']         = df_nav['nav'].apply(lambda x : self._decrypt_data(x))
        df_nav['accu_nav']   = df_nav['accu_nav'].apply(lambda x : self._decrypt_data(x))
        df_nav['accu_nav_w'] = df_nav['accu_nav_w'].apply(lambda x : self._decrypt_data(x))
        #df_nav['nav'] = df_nav['nav'] - df_nav.index * 0.01 - 0.01
        #df_nav['accu_nav'] = df_nav['accu_nav'].apply(lambda x: float(x) - 0.01)
        #df_nav['accu_nav_w'] = df_nav['accu_nav_w'].apply(lambda x: float(x) - 0.02)

        return df_nav, ''
