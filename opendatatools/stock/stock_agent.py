# encoding: utf-8

from opendatatools.common import RestAgent
from opendatatools.common import date_convert, remove_non_numerical
from bs4 import BeautifulSoup
import datetime
import json
import pandas as pd
import io
from opendatatools.futures.futures_agent import _concat_df
import zipfile

class SHExAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        headers = {
            "Accept": '*/*',
            'Referer': 'http://www.sse.com.cn/market/sseindex/indexlist/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        }
        self.add_headers(headers)

    def get_index_list(self):
        url = 'http://query.sse.com.cn/commonSoaQuery.do'
        data = {
            'sqlId': 'DB_SZZSLB_ZSLB',
        }

        response = self.do_request(url, data)
        rsp = json.loads(response)

        if 'pageHelp' in rsp:
            data = rsp['pageHelp']['data']
            return pd.DataFrame(data)
        else:
            return None

    def get_index_component(self, index):
        url = 'http://query.sse.com.cn/commonSoaQuery.do'
        data = {
            'sqlId': 'DB_SZZSLB_CFGLB',
            'indexCode' : index,
        }

        response = self.do_request(url, data)
        rsp = json.loads(response)

        if 'pageHelp' in rsp:
            data = rsp['pageHelp']['data']
            return pd.DataFrame(data)
        else:
            return None

    def get_dividend(self, code):
        url = 'http://query.sse.com.cn/commonQuery.do'
        data = {
            'sqlId' : 'COMMON_SSE_GP_SJTJ_FHSG_AGFH_L_NEW',
            'security_code_a' : code,
        }

        response = self.do_request(url, data)
        rsp = json.loads(response)

        if 'result' in rsp:
            data = rsp['result']
            return pd.DataFrame(data)
        else:
            return None

    def get_rzrq_info(self, date):
        date2 = date_convert(date, '%Y-%m-%d', '%Y%m%d')
        url = 'http://www.sse.com.cn/market/dealingdata/overview/margin/a/rzrqjygk%s.xls' % (date2)
        response = self.do_request(url, None, method='GET', type='binary')
        if response is not None:
            excel = pd.ExcelFile(io.BytesIO(response))
            df_total = excel.parse('汇总信息').dropna()
            df_detail = excel.parse('明细信息').dropna()
            df_total['date'] = date
            df_detail['date'] = date
            return df_total, df_detail
        else:
            return None, None

    def get_pledge_info(self, date):
        date2 = date_convert(date, '%Y-%m-%d', '%Y%m%d')
        url = 'http://query.sse.com.cn/exportExcel/exportStockPledgeExcle.do?tradeDate=%s' % (date2)
        response = self.do_request(url, None, method='GET', type='binary')
        if response is not None:
            excel = pd.ExcelFile(io.BytesIO(response))
            df_total = excel.parse('交易金额汇总').dropna()
            df_detail = excel.parse('交易数量明细').dropna()
            df_total['date'] = date
            df_detail['date'] = date
            return df_total, df_detail
        else:
            return None, None


class SZExAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_index_list(self):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE'  : 'xls',
            'CATALOGID' : '1812',
        }

        response = self.do_request(url, data, method='GET', type='binary')
        df = pd.read_excel(io.BytesIO(response))
        return df

    def get_index_component(self, index):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE': 'xls',
            'CATALOGID': '1747',
            'ZSDM' : index
        }

        response = self.do_request(url, data, method='GET', type='binary')
        if response is not None:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None

    def get_rzrq_info(self, date):
        df_total  = self._get_rzrq_total(date)
        df_detail = self._get_rzrq_detail(date)
        if df_total is not None:
            df_total['date'] = date
        if df_detail is not None:
            df_detail['date'] = date
        return df_total, df_detail

    def _get_rzrq_total(self, date):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE': 'xls',
            'CATALOGID': '1837_xxpl',
            'TABKEY' : 'tab1',
            "txtDate": date,
        }

        response = self.do_request(url, data, method='GET', type='binary')
        if response is not None and len(response) > 0:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None

    def _get_rzrq_detail(self, date):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE': 'xls',
            'CATALOGID': '1837_xxpl',
            'TABKEY': 'tab2',
            "txtDate" : date,
        }

        response = self.do_request(url, data, method='GET', type='binary')
        if response is not None and len(response) > 0:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None

    def get_pledge_info(self, date):
        df_total  = self._get_pledge_info_total(date)
        df_detail = self._get_pledge_info_detail(date)
        if df_total is not None:
            df_total['date'] = date
        if df_detail is not None:
            df_detail['date'] = date
            df_detail['证券代码'] = df_detail['证券代码'].apply(lambda x: str(x).zfill(6))
        return df_total, df_detail

    def _get_pledge_info_total(self, date):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE': 'xls',
            'CATALOGID': '1837_gpzyhgxx',
            'TABKEY': 'tab1',
            "txtDate" : date,
            'ENCODE'  : 1,
        }

        response = self.do_request(url, data, method='GET', type='binary')
        if response is not None and len(response) > 0:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None


    def _get_pledge_info_detail(self, date):
        url = 'http://www.szse.cn/szseWeb/ShowReport.szse'
        data = {
            'SHOWTYPE': 'xls',
            'CATALOGID': '1837_gpzyhgxx',
            'TABKEY': 'tab2',
            "txtDate" : date,
            'ENCODE'  : 1,
        }

        response = self.do_request(url, data, method='GET', type='binary')
        if response is not None and len(response) > 0:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None

class CSIAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_index_list(self):
        url = 'http://www.csindex.com.cn/zh-CN/indices/index'

        page = 1
        result_data = []
        while True:
            data = {
                "data_type" : "json",
                "page"       : page,
            }
            response = self.do_request(url, data, method='GET')
            rsp = json.loads(response)

            page = page + 1
            print("fetching data at page %d" % (page) )
            if "list" in rsp:
                result_data.extend(rsp['list'])
                if len(rsp['list']) == 0:
                    break
            else:
                return None

        return pd.DataFrame(result_data)

    def get_index_component(self, index):
        url = 'http://www.csindex.com.cn/uploads/file/autofile/cons/%scons.xls' % (index)

        response = self.do_request(url, None, method='GET', type='binary')
        if response is not None:
            df = pd.read_excel(io.BytesIO(response))
            return df
        else:
            return None

class XueqiuAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    # 600000.SH -> SH600000
    def convert_to_xq_symbol(self, symbol):
        temp = symbol.split(".")
        return temp[1] + temp[0]

    def convert_to_xq_symbols(self, symbols):
        result = ''
        for symbol in symbols.split(','):
            result = result + self.convert_to_xq_symbol(symbol) + ','
        return result

    # SH600000 -> 600000.SH
    def convert_from_xq_symbol(self, symbol):
        market = symbol[0:2]
        code   = symbol[2:]
        return code + '.' + market

    def prepare_cookies(self, url):
        response = self.do_request(url, None)
        if response is not None:
            cookies = self.get_cookies()
            return cookies
        else:
            return None

    def get_quote(self, symbols):
        url = 'https://stock.xueqiu.com/v5/stock/realtime/quotec.json'
        data = {
            'symbol' : self.convert_to_xq_symbols(symbols)
        }

        # {"data":[{"symbol":"SH000001","current":3073.8321,"percent":-1.15,"chg":-35.67,"timestamp":1528427643770,"volume":6670380300,"amount":8.03515860132E10,"market_capital":1.393367880255658E13,"float_market_capital":1.254120000811718E13,"turnover_rate":0.64,"amplitude":0.91,"high":3100.6848,"low":3072.5418,"avg_price":3073.832,"trade_volume":5190400,"side":0,"is_trade":true,"level":1,"trade_session":null,"trade_type":null}],"error_code":0,"error_description":null}
        response = self.do_request(url, data, method='GET')

        if response is not None:
            jsonobj = json.loads(response)
            if jsonobj['error_code'] == 0:
                result = []
                for rsp in jsonobj['data']:
                    result.append( {
                        'time'   : datetime.datetime.fromtimestamp(rsp['timestamp']/1000),
                        'symbol' : self.convert_from_xq_symbol(rsp['symbol']),
                        'high'   : rsp['high'],
                        'low'    : rsp['low'],
                        'last'   : rsp['current'],
                        'change' : rsp['chg'],
                        'percent': rsp['percent'],
                        'volume' : rsp['volume'],
                        'amount' : rsp['amount'],
                        'turnover_rate'         : rsp['turnover_rate'],
                        'market_capital'        : rsp['market_capital'],
                        'float_market_capital' : rsp['float_market_capital'],
                        'is_trading'            : rsp['is_trade'],
                    } )

                return pd.DataFrame(result), ''
            else:
                return None, jsonobj['error_description']
        else:
            return None, '请求数据失败'

    def get_kline(self, symbol, timestamp, period, count):
        url = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'
        data = {
            'symbol' : self.convert_to_xq_symbol(symbol),
            'begin'  : timestamp,
            'period' : period,
            'type'   : 'before',
            'count'  : count,
            'indicator' : 'kline',
        }

        cookies = self.prepare_cookies('https://xueqiu.com/hq')

        response = self.do_request(url, data, cookies=cookies, method='GET')

        if response is not None:
            jsonobj = json.loads(response)
            if jsonobj['error_code'] == 0:
                result = []
                for rsp in jsonobj['data']['item']:
                    result.append( {
                        'symbol' : symbol,
                        'time'   : datetime.datetime.fromtimestamp(rsp[0]/1000),
                        'volume' : rsp[1],
                        'open'   : rsp[2],
                        'high'   : rsp[3],
                        'low'    : rsp[4],
                        'last'   : rsp[5],
                        'change' : rsp[6],
                        'percent': rsp[7],
                        'turnover_rate'         : rsp[8],
                    } )

                return pd.DataFrame(result), ''
            else:
                return None, jsonobj['error_description']
        else:
            return None, '请求数据失败'


    def get_kline_multisymbol(self, symbols, timestamp, period, count):

        cookies = self.prepare_cookies('https://xueqiu.com/hq')
        url = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'

        result = []
        for symbol in symbols:

            data = {
                'symbol' : self.convert_to_xq_symbol(symbol),
                'begin'  : timestamp,
                'period' : period,
                'type'   : 'before',
                'count'  : count,
                'indicator' : 'kline',
            }

            response = self.do_request(url, data, cookies=cookies, method='GET')

            if response is not None:
                jsonobj = json.loads(response)
                if jsonobj['error_code'] == 0:
                    for rsp in jsonobj['data']['item']:
                        result.append( {
                            'symbol' : symbol,
                            'time'   : datetime.datetime.fromtimestamp(rsp[0]/1000),
                            'volume' : rsp[1],
                            'open'   : rsp[2],
                            'high'   : rsp[3],
                            'low'    : rsp[4],
                            'last'   : rsp[5],
                            'change' : rsp[6],
                            'percent': rsp[7],
                            'turnover_rate': rsp[8],
                        } )

        return pd.DataFrame(result), ''

    def get_kline_multitimestamp(self, symbol, timestamps, period, count):

        cookies = self.prepare_cookies('https://xueqiu.com/hq')
        url = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'

        result = []
        for timestamp in timestamps:
            data = {
                'symbol' : self.convert_to_xq_symbol(symbol),
                'begin'  : timestamp,
                'period' : period,
                'type'   : 'before',
                'count'  : count,
                'indicator' : 'kline',
            }

            response = self.do_request(url, data, cookies=cookies, method='GET')

            if response is not None:
                jsonobj = json.loads(response)
                if jsonobj['error_code'] == 0:
                    for rsp in jsonobj['data']['item']:
                        result.append( {
                            'symbol' : symbol,
                            'time'   : datetime.datetime.fromtimestamp(rsp[0]/1000),
                            'volume' : rsp[1],
                            'open'   : rsp[2],
                            'high'   : rsp[3],
                            'low'    : rsp[4],
                            'last'   : rsp[5],
                            'change' : rsp[6],
                            'percent': rsp[7],
                            'turnover_rate': rsp[8],
                        } )

        return pd.DataFrame(result), ''

class SinaAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    @staticmethod
    def clear_text(text):
        return text.replace('\n', '').strip()

    def get_adj_factor(self, symbol):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        if month < 4 :
            quarter = 1
        elif month < 7:
            quarter = 2
        elif month < 10:
            quarter = 3
        else:
            quarter = 4

        temp = symbol.split(".")
        url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/%s.phtml' % temp[0]

        curr_year = year
        curr_quarter = quarter
        result_list = []
        no_data_cnt = 0
        while True:
            print('getting data for year = %d, quarter = %d' % (curr_year, curr_quarter))
            param = {
                'year' : curr_year,
                'jidu' : curr_quarter,
            }
            response = self.do_request(url, param, method='GET', encoding='gb18030')
            soup = BeautifulSoup(response, "html5lib")
            divs = soup.find_all('div')

            data = []
            for div in divs:
                if div.has_attr('class') and 'tagmain' in div['class']:
                    tables = div.find_all('table')

                    for table in tables:
                        if table.has_attr('id') and table['id'] == 'FundHoldSharesTable':
                            rows = table.findAll('tr')
                            for row in rows:
                                cols = row.findAll('td')
                                if len(cols) == 8:
                                    date = SinaAgent.clear_text(cols[0].text)
                                    adjust_factor = SinaAgent.clear_text(cols[7].text)

                                    if date == '日期':
                                        continue

                                    data.append({
                                        "date": date,
                                        "adjust_factor": adjust_factor,
                                    })

            result_list.extend(data)
            if len(data) == 0:
                no_data_cnt = no_data_cnt + 1
                if no_data_cnt >= 3:
                    break

            # prepare for next round
            if curr_quarter == 1:
                curr_year = curr_year - 1
                curr_quarter = 4
            else:
                curr_quarter = curr_quarter - 1

        return pd.DataFrame(result_list), ""

    # 600000.SH -> SH600000
    def convert_to_sina_symbol(self, symbol):
        temp = symbol.split(".")
        return temp[1].lower() + temp[0]

    def get_trade_detail(self, symbol, trade_date):
        url = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s' % (trade_date, self.convert_to_sina_symbol(symbol))

        response = self.do_request(url, None, method='GET', type='text', encoding='gb18030')
        if response is not None:
            rsp = io.StringIO(response)
            line = rsp.readline()  # skip first line
            line = rsp.readline()
            result = []
            while line is not None and len(line) > 10:
                items = line.split('\t')
                if len(items) == 6:
                    result.append({
                        'time'    : SinaAgent.clear_text(items[0]),
                        'price'   : SinaAgent.clear_text(items[1]),
                        'change'  : SinaAgent.clear_text(items[2]),
                        'volume'   : SinaAgent.clear_text(items[3]),
                        'turnover': SinaAgent.clear_text(items[4]),
                        'bs'       : SinaAgent.clear_text(items[5]),
                    })
                line = rsp.readline()

            df = pd.DataFrame(result)
            df['date'] = trade_date
            df['symbol'] = symbol
            return df, ''

        return None, '获取数据失败'

class CNInfoAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    @staticmethod
    def clear_text(text):
        return text.replace('\n', '').strip()

    def _parse_report_file(self, file):
        lines = file.readlines()
        data_list = []
        for i in range(len(lines)):
            items = lines[i].decode('gbk').split()
            if items[0][:2] == '机构':
                head = items[0].split(sep=',')
            else:
                items    = lines[i].decode('gbk')[1:]
                data     = items.split(sep=',')
                data[0]  = data[0][1:-1]
                data[-1] = remove_non_numerical(data[-1])
                data_list.append(data)
        df = pd.DataFrame(data_list)
        df.columns = head
        return df


    def get_report_data(self, market, symbol, type):

        url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
        data = {
            'market'   : market,
            'type'     : type,
            'code'     : symbol,
            'orgid'    : 'gs%s%s' % (market, symbol),
            'minYear'  : '1990',
            'maxYear'  : '2018',
        }

        response = self.do_request(url, param=data, method='POST', type='binary')
        '''if response is None:
            return None, '没有获取到数据'
        else:
        '''
        try:
            zip_ref = zipfile.ZipFile(io.BytesIO(response))
            df_list = []
            for finfo in zip_ref.infolist():
                file = zip_ref.open(finfo, 'r')
                df = self._parse_report_file(file)
                df_list.append(df)
            df_result = _concat_df(df_list)
            df_result.reset_index(inplace=True, drop=True)

            return df_result, ''
        except:
            return None, '获取数据失败'

    def get_shareholder_structure(self, market, symbol):

        if symbol.startswith('002'):
            board = 'sme'
        elif symbol.startswith('3'):
            board = 'cn'
        else:
            board = 'mb'

        url = 'http://www.cninfo.com.cn/information/lastest/%s%s%s.html' % (market, board, symbol)
        response = self.do_request(url, encoding='gb18030')
        if response is None:
            return None, '获取数据失败'

        soup = BeautifulSoup(response, "html5lib")
        divs = soup.find_all('div')

        data = []
        for div in divs:
            if div.has_attr('class') and 'clear' in div['class']:
                tables = div.find_all('table')

                for table in tables:
                    rows = table.findAll('tr')
                    for row in rows:
                        cols = row.findAll('td')
                        if len(cols) == 2:
                            indicator = CNInfoAgent.clear_text(cols[0].text).replace('：', '')
                            value     = CNInfoAgent.clear_text(cols[1].text)

                            data.append({
                                "indicator": indicator,
                                "value"    : value,
                            })
                break

        return pd.DataFrame(data), ""

class EastMoneyAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def _parse_hist_money_flow(self, response):
        jsonobj = json.loads(response)
        result = []
        for data in jsonobj['data']:
            items = data.split(',')
            result.append({
                'Time': items[0],
                'ZLJLRJE': items[1],
                'ZLJLRZB': items[2],
                'CDDJLRJE': items[3],
                'CDDJLRZB': items[4],
                'DDLRJE': items[5],
                'DDLRZB': items[6],
                'ZDLRJE': items[7],
                'ZDLRZB': items[8],
                'XDLRJE': items[9],
                'XDLRZB': items[10],
            })
        return pd.DataFrame(result)

    def _get_hist_money_flow(self, url):
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        df = self._parse_hist_money_flow(response)
        return df, ''

    def get_hist_money_flow(self, symbol):
        url = 'http://ff.eastmoney.com//EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&js={"data":(x)}&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id=%s' % symbol
        return self._get_hist_money_flow(url)

    def get_hist_money_flow_market(self):
        url = 'http://data.eastmoney.com/zjlx/dpzjlx.html'
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        # get data from html
        idx  = response.find('var DefaultJson=')
        idx1 = response.find('[', idx)
        idx2 = response.find(']', idx)
        json_rsp = '{ "data": ' + response[idx1:idx2+1] + '}'

        df = self._parse_hist_money_flow(json_rsp)
        return df, ''

    def _get_realtime_money_flow(self, url):
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'

        jsonobj = json.loads(response)
        result = {}
        result['Time'] = jsonobj['xa'].split(',')
        result['ZLJLRJE']  = list()
        result['CDDJLRJE'] = list()
        result['DDJLRJE']  = list()
        result['ZDJLRJE']  = list()
        result['XDJLRJE']  = list()
        for data in jsonobj['ya']:
            items = data.split(',')
            result['ZLJLRJE'].append(items[0])
            result['CDDJLRJE'].append(items[1])
            result['DDJLRJE'].append(items[2])
            result['ZDJLRJE'].append(items[3])
            result['XDJLRJE'].append(items[4])

        df = pd.DataFrame().from_dict(result, orient='index').T
        df.dropna(inplace=True)
        return df, ''

    def get_realtime_money_flow(self, symbol):
        url = 'http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?id=%s&type=ff&check=MLBMS&js={(x)}&rtntype=3&acces_token=1942f5da9b46b069953c873404aad4b5' % symbol
        return self._get_realtime_money_flow(url)

    def get_realtime_money_flow_market(self):
        url = 'http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?id=ls&type=ff&check=MLBMS&js={(x)}&rtntype=3&acces_token=1942f5da9b46b069953c873404aad4b5'
        return self._get_realtime_money_flow(url)
#==============================================================================
#一次性获取所有股票的实时资金流，并按照主力净流入净额排序
## 指标定义
# 超大单：大于等于50万股或者100万元的成交单;
# 大单：大于等于10万股或者20万元且小于50万股和100万元的成交单;
# 中单：大于等于2万股或者4万元且小于10万股和20万元的成交单;
# 小单：小于2万股和4万元的成交单;
# 流入：买入成交额;
# 流出：卖出成交额;
# 主力流入：超大单加大单买入成交额之和;
# 主力流出：超大单加大单卖出成交额之和;
# 净额：流入-流出;
# 净比：(流入-流出)/总成交额;
# 单位：亿元
#==============================================================================
    def toDataFrame(self,ll):
        dataframe = []
        for l in ll:
            l = l.replace('-','0')
            temp = l.split(",")[1:]
            temp[2:-2] = map(eval, temp[2:-2])
            dataframe.append(temp)
        dataframe = pd.DataFrame(dataframe)
        dataframe.columns = [u'代码',u'名称',u'最新价',u'今日涨跌幅',u'今日主力净流入净额',u'今日主力净流入净占比',u'今日超大单净流入净额',u'今日超大单净流入净占比',u'今日大单净流入净额',u'今日大单净流入净占比',u'今日中单净流入净额',u'今日中单净流入净占比',u'今日小单净流入净额',u'今日小单净流入净占比',u'time',u'未知']
        return dataframe

    def _get_realtime_allstock_flow(self, url):
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'
        pages = 'pages'
        date = 'date'
        data = 'data'
        data = eval(response[13:])
        flashflow = data['data']
        df = self.toDataFrame(flashflow)
        df.index = df.ix[:,0]
        df.dropna(inplace=True)
        return df, ''

    def get_allstock_flow(self):
        url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=3700&js=var%20ucjEIgIa={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=1942f5da9b46b069953c873404aad4b5&cmd=C._AB&sty=DCFFITA&rt=50984894'
        return self._get_realtime_allstock_flow(url)

