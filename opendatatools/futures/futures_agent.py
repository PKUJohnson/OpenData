# encoding: utf-8

from opendatatools.common import RestAgent, split_date, date_convert, remove_chinese
import pandas as pd
import json
import zipfile
import io
import re
from xml.etree import ElementTree

SHF_name_map = {"CJ1": "成交量",
                   "CJ1_CHG": "成交量增减",
                   "PARTICIPANTABBR1": "成交量期货公司",
                   "CJ2": "持买仓量",
                   "CJ2_CHG": "持买仓量增减",
                   "PARTICIPANTABBR2": "持买仓量期货公司",
                   "CJ3": "持卖仓量",
                   "CJ3_CHG": "持卖仓量增减",
                   "PARTICIPANTABBR3": "持卖仓量期货公司",
                   "RANK": "名次",
                   "INSTRUMENTID": "symbol",
                   }

def format_field(x):
    if type(x) == str:
        return x.replace('\n', '').strip()
    else:
        return x

def _merge_df(df_list):
    df_result = None
    for df in df_list:
        if df_result is None:
            df_result = df
        else:
            df_result = pd.merge(df_result, df, left_index=True, right_index=True)
    return df_result

def _concat_df(df_list):
    return pd.concat(df_list)

def _rename_df(df):
    name_map = {
        "会员简称" : "期货公司",
        "（手）"   : "",
    }
    for col in df.columns:
        for name, value in name_map.items():
            if name in col:
                col_new = col.replace(name, value)
                df.rename(columns={col: col_new}, inplace=True)

class SHFAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    # date : %Y%m%d
    def get_trade_rank(self, date):
        url = 'http://www.shfe.com.cn/data/dailydata/kx/pm%s.dat' % date_convert(date, '%Y-%m-%d', '%Y%m%d')
        response = self.do_request(url, None)
        rsp = json.loads(response)

        code = rsp['o_code']
        msg  = rsp['o_msg']

        if code != 0:
            return None, msg
        if 'report_date' in rsp.keys():
            date = rsp['report_date']
        else:
            date = date_convert(date, '%Y-%m-%d', "%Y%m%d")
        records = rsp['o_cursor']

        df = pd.DataFrame(records)
        df['date'] = date

        for col in df.columns:
            df[col] = df[col].apply(lambda x : format_field(x))

        df['RANK'] = df['RANK'].apply(lambda x: int(x))
        df = df[(df['RANK']>0) & (df['RANK']<=20)]
        df.rename(columns=SHF_name_map, inplace=True)
        df = df[list(SHF_name_map.values())]

        return df, ""

class DCEAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    '''
    名次		会员简称	成交量		增减		
    1		海通期货	24,326		9,991		
    2		中信期货	12,926		5,960		
    3		兴证期货	12,835		4,405		
    4		西南期货	11,054		6,614		
    '''
    def _parse_trade_file(self, file, date):
        filename = file.name.encode('cp437').decode('gbk')
        name_items = filename.split("_")
        symbol = name_items[1]

        lines = file.readlines()
        df_list = []

        if date >'2015-12-31':
            charset = 'utf-8'
        else:
            charset = 'gbk'

        for i in range(len(lines)):
            items = lines[i].decode(charset).split()
            if len(items) == 4 and items[0] == '名次':
                head = items
                head[1] = head[2] + head[1]
                head[3] = head[2] + head[3]
                data = []
                for j in range(20):
                    i = i + 1
                    items = lines[i].decode(charset).split()
                    if items[0] == '总计':
                        break
                    data.append(items)
                if data == []:
                    data.append(['', '', '', ''])
                df = pd.DataFrame(data)
                df.columns = head
                df.set_index('名次', inplace=True)
                df_list.append(df)

        df_result = _merge_df(df_list)
        df_result['symbol'] = symbol
        return df_result


    def get_trade_rank(self, date):
        url = 'http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesBatchData.html'
        year, month, day = split_date(date, '%Y-%m-%d')
        data = {
            "year": year,
            "month": month - 1,  # 脑残程序员的设计
            "day": day,
            "batchExportFlag": 'batch',
        }

        response = self.do_request(url, data, "POST", type='binary')
        zip_ref = zipfile.ZipFile(io.BytesIO(response))
        df_list = []
        for finfo in zip_ref.infolist():
            file = zip_ref.open(finfo, 'r')
            df = self._parse_trade_file(file, date)
            df_list.append(df)

        df_result = _concat_df(df_list)
        df_result['date'] = date
        df_result.reset_index(level=['名次'], inplace=True)

        _rename_df(df_result)

        return df_result, ""

class CZCAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    '''
    品种：苹果AP              日期： 2018-05-30
    名次  |会员简称      |成交量（手）|增减量    |会员简称      |持买仓量  |增减量    |会员简称      |持卖仓量  |增减量
    1     |海通期货      |157,955     |-2,663    |海通期货      |42,771    |3,342     |海通期货      |43,889    |1,843     
    2     |招商期货      |67,527      |-12,527   |华泰期货      |21,091    |-1,093    |华泰期货      |20,927    |-1,991    
    3     |徽商期货      |66,887      |-29,680   |招商期货      |17,302    |-3,063    |招商期货      |20,519    |-2,788    
    4     |光大期货      |66,322      |-10,134   |永安期货      |17,193    |784       |中信期货      |15,779    |716       
    '''
    def _get_url_by_date(self, date):
        year, month, day = split_date(date, '%Y-%m-%d')
        date_int = int(date_convert(date, '%Y-%m-%d', "%Y%m%d"))
        url = 'http://old.czce.com.cn/portal/DFSStaticFiles/Future/%d/%d/FutureDataHolding.txt'
        url_old = 'http://old.czce.com.cn/portal/exchange/%d/datatradeholding/%d.txt'

        if date < '2015-10-01':
            return url_old % (year, date_int)
        else:
            return url % (year, date_int)

    def _get_code(self, text):
        items = re.split("：| |\t|\r\n|", text)
        return items[1]

    def _get_head(self, text):
        items = self._split_field(text)
        items[1] = '成交量'   + items[1]
        items[3] = '成交量增减'
        items[4] = '持买仓量' + items[4]
        items[6] = '持买仓量增减'
        items[7] = '持卖仓量' + items[7]
        items[9] = '持卖仓量增减'
        return items

    def _get_head_old(self, text):
        items = ['名次', '成交量期货公司', '成交量', '成交量增减', '持买仓量期货公司', '持买仓量', '持买仓量增减', '持卖仓量期货公司', '持卖仓量', '持卖仓量增减']
        return items

    def get_head(self, text, old):
        if old == True:
            return self._get_head_old(text)
        else:
            return self._get_head(text)

    def _get_data(self, lines, old):
        if old == True:
            sep = ','
        else:
            sep = '|'

        data = []
        for line in lines:
            items = self._split_field(line, splitter=sep)
            data.append(items)
        return data

    def _split_field(self, text, splitter = "|"):
        items = text.split(splitter)
        result = [str(x).strip().replace('\r\n', '') for x in items]
        return result

    def _parse_trade_file_old(self, file):
        lines = file.readlines()
        df_list = []
        for i in range(len(lines)):
            items = self._split_field(lines[i], splitter = ',')
            if items[0][0:2] == '合约':
                code = self._get_code(lines[i])
                heads = self.get_head(lines[i], old=True)
                a = i
                while True:
                    a += 1
                    items = self._split_field(lines[a], splitter=',')
                    # print(items)
                    if items[0] == '合计':
                        data = self._get_data(lines[i + 1:a + 1], old=True)
                        break
                df = pd.DataFrame(data)
                df.columns = heads
                df['symbol'] = remove_chinese(code)
                df_list.append(df)
        df_result = _concat_df(df_list)
        return df_result


    def _parse_trade_file(self, file):
        lines = file.readlines()
        df_list = []
        for i in range(len(lines)):
            items = self._split_field(lines[i], splitter='|')
            if len(items) == 10 and items[0] == '名次':
                code = self._get_code(lines[i-1])
                heads = self.get_head(lines[i], old=False)
                a = i
                while True:
                    a += 1
                    items = self._split_field(lines[a], splitter='|')
                    # print(items)
                    if items[0] == '合计':
                        data = self._get_data(lines[i + 1:a + 1], old=False)
                        break
                df = pd.DataFrame(data)
                df.columns = heads
                df['symbol'] = remove_chinese(code)
                df_list.append(df)
        df_result = _concat_df(df_list)
        return df_result

    def parse_trade_file(self, file, date):
        if date < '2015-10-01':
            return  self._parse_trade_file_old(file)
        else:
            return self._parse_trade_file(file)


    def get_trade_rank(self, date):
        url = self._get_url_by_date(date)
        response = self.do_request(url, None, "GET", type='binary')
        df = self.parse_trade_file(io.StringIO(response.decode('gbk')), date)
        df['date'] = date
        _rename_df(df)

        return df, ""

class CFEAgent(RestAgent):

    def __init__(self):
        RestAgent.__init__(self)

    def get_trade_rank(self, date):
        if date < '2018-01-01':
            print("CFE网站改版，暂不兼容旧版，目前此接口仅支持2018年以后数据获取")
            return None, '网站改版，暂不兼容'
        products = ['T', 'IF', 'IC', 'IH', 'TF']
        df_list = []
        for product in products:
            df = self._get_trade_rank_by_product(date, product)
            df_list.append(df)

        df = _concat_df(df_list)
        df['date'] = date
        df.reset_index(level=[0, 1], inplace=True)
        return df, ""

    def _get_trade_rank_by_product(self, date, product):
        url = 'http://www.cffex.com.cn/sj/ccpm/%04d%02d/%02d/%s.xml'
        year, month, day = split_date(date, '%Y-%m-%d')
        url = url % (year, month, day, product)
        response = self.do_request(url, None, "GET")
        root = ElementTree.fromstring(response)
        data_list = []
        for dataElements in root:
            if dataElements.tag != 'data':
                continue

            data = {}
            for subElement in dataElements:
                key   = subElement.tag
                value = subElement.text
                if key in ['instrumentid', 'datatypeid', 'rank', 'shortname', 'volume', 'varvolume']:
                    data[key] = value
            data_list.append(data)

        df = pd.DataFrame(data_list)

        datatype_map = {
            "0" : "成交量",
            "1" : "持买单量",
            "2" : "持卖单量",
        }

        df_list = []
        for type, name in datatype_map.items():
            df_tmp = df[df['datatypeid'] == type].copy()
            df_tmp['rank'] = df_tmp['rank'].apply(lambda x: int(x))
            df_tmp.rename(columns={"instrumentid" : "symbol"}, inplace=True)
            df_tmp.rename(columns={"rank" : "名次"}, inplace=True)
            df_tmp.rename(columns={"shortname" : name + "期货公司"}, inplace=True)
            df_tmp.rename(columns={"volume": name}, inplace=True)
            df_tmp.rename(columns={"varvolume": name + "增减"}, inplace=True)
            df_tmp.drop(['datatypeid'], axis=1, inplace=True)
            df_tmp.set_index(['symbol','名次'], inplace=True)
            df_list.append(df_tmp)

        return _merge_df(df_list)

class SinaFuturesAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        self.dict_market_map = {
            '沪' : 'SHF',
            '连' : 'DCE',
            '郑' : 'CZC',
            '油' : 'INE',
        }

    def convert_market(self, market, product=''):
        if product == '原油':
            return 'INE'
        else:
            return self.dict_market_map[market]

    def _parse_quote_rsp(self, rsp):
        lines = rsp.split('\n')
        list_quotes = []
        for line in lines:
            quote = self._parse_quote_str(line)
            if quote is not None:
                list_quotes.append(quote)

        return pd.DataFrame(list_quotes)

    def _is_cfe_code(self, code):
        code2 = code
        for i in range(10):
            code2 = code2.replace(str(i), '')

        if code2 in ['IF', 'IC', 'IH', 'T', 'TF']:
            return True
        else:
            return False

    def _parse_quote_str(self, line):
        line = line.replace('var hq_str_', '')
        line = line.replace('CFF_RE_', '')

        items = line.split('=')

        if len(items) < 2:
            return None

        code = items[0]
        quote_str = items[1].replace('"', '').replace(';', '')

        fields = quote_str.split(',')

        if self._is_cfe_code(code):
            pass
        else:
            if len(fields) < 18 :
                return None

            quote = {
                'code'     : code,
                'instname' : fields[0],
                'time'     : fields[1],
                'open'     : fields[2],
                'high'     : fields[3],
                'low'      : fields[4],
                'preclose' : fields[5],
                'bidprice1': fields[6],
                'askprice1': fields[7],
                'last'      : fields[8],
                'settle'    : fields[9],
                'presettle' : fields[10],
                'askvol1'   : fields[11],
                'bidvol1'   : fields[12],
                'oi'        : fields[13],
                'volume'   : fields[14],
                'exchange' : self.convert_market(fields[15]),
                'product'  : fields[16],
                'date'     : fields[17],
            }

            return quote

    def get_quote(self, codes):
        url = 'http://hq.sinajs.cn/list=%s' % codes
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        df = self._parse_quote_rsp(response)
        return df, ''

    # 1m, 5m, 15m, 30m, 60m, 1d
    def get_kline(self, type, code):

        if self._is_cfe_code(code):

            if type not in ['5m', '15m', '60m', '1d']:
                return None, '不支持的K线类型'

            if type == '1d':
                url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesDailyKLine?symbol=%s' % (code)
            else:
                url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine%s?symbol=%s' % (type, code)
        else:
            if type not in ['5m', '15m', '30m', '60m', '1d']:
                return None, '不支持的K线类型'

            if type == '1d':
                url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=%s' % (code)
            else:
                url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine%s?symbol=%s' % (type, code)

        response = self.do_request(url)
        if response is None or response == 'null':
            return None, '获取数据失败'

        jsonobj = json.loads(response)
        df = pd.DataFrame(jsonobj)
        df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']

        return df, ''

