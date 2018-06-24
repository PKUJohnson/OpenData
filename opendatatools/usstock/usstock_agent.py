# encoding: utf-8

from opendatatools.common import RestAgent
import pandas as pd
import io
import datetime

class USStockAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def prepare_cookies(self, url):
        response = self.do_request(url, None)
        if response is not None:
            cookies = self.get_cookies()

            # "CrumbStore":{"crumb":"JSkGHd8NKBu"}
            key = "CrumbStore"
            pos = response.find(key)
            if pos != -1:
                idx1 = response.find('{', pos)
                idx2 = response.find('}', pos)
                crumb = response[idx1+1 : idx2].split(':')[1].replace('"', '')
                return cookies, crumb
        else:
            return None, ''

    def _get_symbols(self, market):
        url = 'https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=%s&render=download' % market
        response = self.do_request(url, None, method='GET', type='binary')
        if response is not None:
            df = pd.read_csv(io.BytesIO(response))
            return df
        return None

    def get_symbols(self):
        df_nasdaq = self._get_symbols('nasdaq')
        df_nyse   = self._get_symbols('nyse')
        df_amex   = self._get_symbols('amex')

        return pd.concat([df_nasdaq, df_nyse, df_amex]), ''

    def _get_data(self, symbol, events):

        url_cookies = 'https://finance.yahoo.com/quote/%s/history?p=%s' % (symbol, symbol)
        cookies, crumb = self.prepare_cookies(url_cookies)

        now = datetime.datetime.now().timestamp()
        url = 'https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%d&period2=%d&interval=1d&events=%s&crumb=%s' % (symbol, 0, int(now), events, crumb)
        self.add_headers({'referer' : url_cookies})
        response = self.do_request(url, None, method='GET', type='binary', cookies=cookies)
        if response is not None:
            df = pd.read_csv(io.BytesIO(response))
            return df, ''
        return None, '获取数据失败'

    def get_daily(self, symbol):
        return self._get_data(symbol, 'history')

    def get_dividend(self, symbol):
        return self._get_data(symbol, 'div')

    def get_split(self, symbol):
        return self._get_data(symbol, 'split')
