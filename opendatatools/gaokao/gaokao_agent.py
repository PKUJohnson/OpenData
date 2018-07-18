# encoding: utf-8

from opendatatools.common import RestAgent
import json
import pandas as pd

class GaokaoAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def _get_data(self, url):
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        jsonobj = json.loads(response)
        df = pd.DataFrame(jsonobj)
        return df, ''

    def get_school_list(self, text):
        url = 'https://tu.quantos.org/api/search/%s' % text
        return self._get_data(url)

    def get_school_baseinfo(self, school):
        url = 'https://tu.quantos.org/api/schoolinfo/baseinfo/%s' % school
        return self._get_data(url)

    def get_school_major(self, school):
        url = 'https://tu.quantos.org/api/schoolinfo/major/%s' % school
        return self._get_data(url)

    def get_school_score(self, school):
        url = 'https://tu.quantos.org/api/schoolinfo/score/%s/%%25/%%25' % school
        return self._get_data(url)

    def get_batch_score(self, province, subject):
        url = 'https://tu.quantos.org/api/batchscore/%s/%s/' % (province, subject)
        df, msg = self._get_data(url)
        return df, msg

if __name__ == "__main__":

    agent = GaokaoAgent()
    df, msg = agent.get_batch_score('北京', '理科')
    print(df)