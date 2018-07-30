
import json
import pandas as pd
from bs4 import BeautifulSoup
import datetime

from opendatatools.common import RestAgent

class WeiboAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        self.session.headers['User-Agent'] = "Mozilla/5.0 (Linux; Android 6.0; " \
                                               "Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36"
        self.session.headers['Referer'] = 'http://data.weibo.com/index/newindex'

    def _get_items(self, word):
        url = 'http://data.weibo.com/index/ajax/newindex/searchword'
        data = { "word": word }

        response = self.do_request(url, data)
        if response is None:
            return None

        jsonobj = json.loads(response)
        rsp = jsonobj['html']

        soup = BeautifulSoup(rsp, "html5lib")
        lis = soup.find_all('li')

        result = {}
        for li in lis:
            wid = li['wid']
            keyword = li['word']
            result[keyword] = wid

        return result

    # 1hour, 1day, 1month, 3month
    def _get_index_data(self, wid, type):
        url = 'http://data.weibo.com/index/ajax/newindex/getchartdata'
        data = {
            "wid": wid,
            "dateGroup": type,
        }

        response = self.do_request(url, data)
        if response is None:
            return None

        jsonobj = json.loads(response)
        data = {
            'index': jsonobj['data'][0]['trend']['x'],
            'value': jsonobj['data'][0]['trend']['s'],
        }

        df = pd.DataFrame(data)
        return df

    def _process_index(self, index):
        now = datetime.datetime.now()
        curr_year  = now.year
        curr_date = "%04d%02d%02d" % (now.year, now.month, now.day)
        if '月' in index:
            tmp = index.replace('日', '').split('月')
            date = "%04d%02d%02d" % (curr_year, int(tmp[0]), int(tmp[1]))
            if date > curr_date:
                date = "%04d%02d%02d" % (curr_year-1, int(tmp[0]), int(tmp[1]))

            return date

        return index

    # 1hour, 1day, 1month, 3month
    def get_weibo_index(self, word, type):
        dict_keyword = self._get_items(word)
        if dict_keyword is None:
            return None, '获取数据失败'

        df_list = []
        for keyword, wid in dict_keyword.items():
            df = self._get_index_data(wid, type)
            if df is not None:
                df.columns = ['index', keyword]
                df['index'] = df['index'].apply(lambda x : self._process_index(x))
                df.set_index('index', inplace=True)
                df_list.append(df)

        if len(df_list) > 0:
            return pd.concat(df_list, axis=1), ''

        return None, ''

