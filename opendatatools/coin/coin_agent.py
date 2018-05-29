
import pandas as pd
import json
import datetime
from opendatatools.common import RestAgent

class CoinAgent(RestAgent):

    def __init__(self):
        RestAgent.__init__(self)
        self.set_url()

    def set_url(self):
        self.COIN_LIST_URL = 'https://www.cryptocompare.com/api/data/coinlist/'
        self.COIN_SNAPSHOT_FULL_BY_ID_URL = 'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id='
        self.COIN_SNAPSHOT_URL = 'https://www.cryptocompare.com/api/data/coinsnapshot/'

        self.PRICE_URL = 'https://min-api.cryptocompare.com/data/price'
        self.PRICE_MULTI_URL = 'https://min-api.cryptocompare.com/data/pricemulti'
        self.PRICE_MULTI_FULL_URL = 'https://min-api.cryptocompare.com/data/pricemultifull'
        self.PRICE_HISTORICAL_URL = 'https://min-api.cryptocompare.com/data/pricehistorical'

        self.GENERATE_AVG_URL = 'https://min-api.cryptocompare.com/data/generateAvg'
        self.DAY_AVG_URL = 'https://min-api.cryptocompare.com/data/dayAvg'

        self.SUBS_WATCH_LIST_URL = 'https://min-api.cryptocompare.com/data/subsWatchlist'
        self.SUBS_URL = 'https://min-api.cryptocompare.com/data/subs'

        self.ALL_EXCHANGES_URL = 'https://min-api.cryptocompare.com/data/all/exchanges'
        self.TOP_EXCHANGES_URL = 'https://min-api.cryptocompare.com/data/top/exchanges'
        self.TOP_VOLUMES_URL = 'https://min-api.cryptocompare.com/data/top/volumes'
        self.TOP_PAIRS_URL = 'https://min-api.cryptocompare.com/data/top/pairs'

        self.HIST_DAY_URL = 'https://min-api.cryptocompare.com/data/histoday'
        self.HIST_HOUR_URL = 'https://min-api.cryptocompare.com/data/histohour'
        self.HIST_MINUTE_URL = 'https://min-api.cryptocompare.com/data/histominute'

        self.SOCIAL_STATS_URL = 'https://www.cryptocompare.com/api/data/socialstats?id='

        self.MINING_CONTRACTS_URL = 'https://www.cryptocompare.com/api/data/miningcontracts/'
        self.MINING_EQUIPMENT_URL = 'https://www.cryptocompare.com/api/data/miningequipment/'

    def format_unix_time(self, df, col='time'):
        if col in df.columns:
            df[col] = df[col].apply(lambda x : datetime.datetime.fromtimestamp(x))

        return df

    def _fetch(self, url):
        rsp = self.do_request(url)
        json_obj = json.loads(rsp)

        if "Response" in json_obj:
            response = json_obj['Response']
            if "Message" in json_obj :
                message  = json_obj['Message']
            else:
                message = ""

            if response == "Success":
                data = json_obj['Data']
                return data, message
            else:
                return None, message
        else:
            return json_obj, ""

    def get_coin_list(self):
        data, message = self._fetch(self.COIN_LIST_URL)
        if data is None:
            return None, message

        df = self.format_unix_time(pd.DataFrame(data).T)
        return df, message

    def get_coin_snapshot(self, fsym, tsym):
        '''
            Keyword arguments:
            fsym - The symbol of the currency you want to get that for
            tsym - The symbol of the currency that data will be in.
        '''
        data, message = self._fetch(self.COIN_SNAPSHOT_URL + '?fsym=' + fsym + '&tsym=' + tsym)
        if data is None:
            return None, None, message

        df = pd.DataFrame(data['Exchanges'])
        df['LASTUPDATE'] = df['LASTUPDATE'].apply(lambda x : int(x))
        df = self.format_unix_time(df, 'LASTUPDATE')
        return data['AggregatedData'], df, message

    def get_coin_price(self, fsym, tsyms, exchange):
        data, message = self._fetch(self.PRICE_URL + '?fsym=' + fsym + '&tsyms=' + tsyms + "&e=" + exchange)
        if data is None:
            return None, message

        return data, message

    def get_his_min(self, fsym, tsym, exchange, limit):
        data, message = self._fetch(self.HIST_MINUTE_URL + '?fsym=' + fsym + '&tsym=' + tsym + "&e=" + exchange + "&limit=" + str(limit))
        if data is None:
            return None, message

        df = self.format_unix_time(pd.DataFrame(data))
        return df, message

    def get_his_hour(self, fsym, tsym, exchange, limit):
        data, message = self._fetch(self.HIST_HOUR_URL + '?fsym=' + fsym + '&tsym=' + tsym + "&e=" + exchange + "&limit=" + str(limit))
        if data is None:
            return None, message

        df = self.format_unix_time(pd.DataFrame(data))
        return df, message

    def get_his_day(self, fsym, tsym, exchange, limit):
        data, message = self._fetch(self.HIST_DAY_URL + '?fsym=' + fsym + '&tsym=' + tsym + "&e=" + exchange + "&limit=" + str(limit))
        if data is None:
            return None, message

        df = self.format_unix_time(pd.DataFrame(data))
        return df, message
