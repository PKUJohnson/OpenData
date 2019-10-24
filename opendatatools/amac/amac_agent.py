# encoding: UTF-8

from urllib.parse import urlencode
from bs4 import BeautifulSoup
import datetime
import time
from opendatatools.common import RestAgent
import pandas as pd
import json
import math
import random


class AMACAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        self.add_headers({  # 请求头
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '2',
            'Content-Type': 'application/json',
            'Host': 'gs.amac.org.cn',
            'Origin': 'http://gs.amac.org.cn',
            'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        })

        self.fund_list_url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/fund?'
        self.fund_base_url = 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/'

        self.manager_list_url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?'  # 请求 url 所携带参数的前面部分
        self.manager_base_url = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/'  # 基金 url 前面的部分

        self.company_title_list = [
                '私募基金管理人名称',
                '管理人详细信息网址',
                '管理人类型',
                '成立时间',
                '备案时间',
                '机构诚信信息',
                '基金管理人全称(中文)',
                '基金管理人全称(英文)',
                '登记编号',
                '组织机构代码',
                '登记时间',
                '成立时间',
                '注册地址',
                '办公地址',
                '注册资本(万元)(人民币)',
                '实缴资本(万元)(人民币)',
                '企业性质',
                '注册资本实缴比例',
                '机构类型',
                '业务类型',
                '全职员工人数',
                '取得基金从业人数',
                '机构网址',
            ]
        self.fund_title_list = [
            '基金名称',
            '基金编号',
            '成立时间',
            '备案时间',
            '基金备案阶段',
            '基金类型',
            '币种',
            '基金管理人名称',
            '管理类型',
            '托管人名称',
            '运作状态',
            '基金信息最后更新时间',
            '基金协会特别提示（针对基金）'
        ]

    def get_total_record(self, list_url):
        params = {
            'rand': random.random(),
            'page': 1,
            'size': 10,
        }
        url = list_url + urlencode(params)
        resp = self.do_request(url, json={}, method="POST")
        result = json.loads(resp)
        return result['totalElements']

    def get_page(self, list_url, page):
        '''爬取第xx页信息'''
        # url 携带参数，设置了每页显示 100 条信息
        params = {
            'rand': 0.3248183083707361,
            'page': page,
            'size': 1000,
        }
        url = list_url + urlencode(params)
        resp = self.do_request(url, json={}, method="POST")
        return json.loads(resp)

    def parse_fund_page(self, r_json):
        if r_json:
            items = r_json.get('content')
            for item in items:
                info = {}
                info['id'] = item.get('id')
                info['基金名称'] = item.get('fundName')
                info['基金详细信息网址'] = self.fund_base_url + item.get('id') + ".html"
                info['基金状态'] = item.get('workingState')
                info['私募基金管理人名称'] = item.get('managerName')
                info['管理人类型'] = item.get('managerType')
                establishDate = item.get('establishDate')
                info['成立时间'] = str(datetime.datetime.fromtimestamp(
                    establishDate / 1000).date()) if establishDate else ''  # 成立时间有可能为空，防止这种情况而报错
                putOnRecordDate = item.get('putOnRecordDate')
                info['备案时间'] = str(
                    datetime.datetime.fromtimestamp(putOnRecordDate / 1000).date()) if putOnRecordDate else ''
                yield info

    def parse_manager_page(self, r_json):
        if r_json:
            items = r_json.get('content')
            for item in items:
                info = {}
                info['id'] = item.get('id')
                info['私募基金管理人名称'] = item.get('managerName')
                info['管理人详细信息网址'] = self.manager_base_url + item.get('id') + ".html"
                info['管理人类型'] = item.get('primaryInvestType')
                establishDate = item.get('establishDate')
                info['成立时间'] = str(datetime.datetime.fromtimestamp(
                    establishDate / 1000).date()) if establishDate else ''  # 成立时间有可能为空，防止这种情况而报错
                registerDate = item.get('registerDate')
                info['备案时间'] = str(
                    datetime.datetime.fromtimestamp(registerDate / 1000).date()) if registerDate else ''
                yield info

    def get_detail(self, url):
        resp = self.do_request(url, method="GET", encoding="utf-8")
        return resp

    def parse_manager_detail(self, html):
        soup = BeautifulSoup(html, "html5lib")
        tables = soup.find_all('table')
        info = {}
        for table in tables:
            if table.has_attr("class") and "table-info" in table['class']:
                rows = table.findAll('tr')
                for row in rows:
                    cols = row.findAll('td')
                    if len(cols) >= 2:
                        title = cols[0].text
                        content = cols[1].text
                        title = title.replace(":", "")
                        content = content.replace("\n", "")
                        content = content.strip()
                        if title in self.company_title_list:
                            info[title] = content

                    if len(cols) >= 4:
                        title = cols[2].text
                        content = cols[3].text
                        title = title.replace(":", "")
                        content = content.replace("\n", "")
                        content = content.strip()
                        if title in self.company_title_list:
                            info[title] = content

        return info

    def parse_fund_detail(self, html):
        soup = BeautifulSoup(html, "html5lib")
        tables = soup.find_all('table')
        info = {}
        for table in tables:
            if table.has_attr("class") and "table-info" in table['class']:
                rows = table.findAll('tr')
                for row in rows:
                    cols = row.findAll('td')
                    if len(cols) >= 2:
                        title = cols[0].text
                        content = cols[1].text
                        title = title.replace(":", "")
                        content = content.replace("\n", "")
                        content = content.strip()
                        if title in self.fund_title_list:
                            info[title] = content

                    if len(cols) >= 4:
                        title = cols[2].text
                        content = cols[3].text
                        title = title.replace(":", "")
                        content = content.replace("\n", "")
                        content = content.strip()
                        if title in self.fund_title_list:
                            info[title] = content

        return info

    def get_company_list(self):
        total_record = self.get_total_record(self.manager_list_url)
        total_page = math.ceil(total_record / 1000)
        print(total_record, total_page)
        lis_json = []
        for page in range(1, total_page):
            print("page=", page)
            r_json = self.get_page(self.manager_list_url, page)
            results = self.parse_manager_page(r_json)
            for result in results:
                lis_json.append(result)

        return pd.DataFrame(lis_json)

    def get_company_detail(self, company_id):
        url = self.manager_base_url + company_id + ".html"
        html = self.get_detail(url)
        info = self.parse_manager_detail(html)
        return info

    def get_fund_list(self):
        total_record = self.get_total_record(self.fund_list_url)
        total_page = math.ceil(total_record / 1000)
        print(total_record, total_page)
        lis_json = []
        for page in range(1, total_page):
            print("page=", page)
            r_json = self.get_page(self.fund_list_url, page)
            results = self.parse_fund_page(r_json)
            for result in results:
                lis_json.append(result)

        return pd.DataFrame(lis_json)

    def get_fund_detail(self, fund_id):
        url = self.fund_base_url + fund_id + ".html"
        html = self.get_detail(url)
        info = self.parse_fund_detail(html)
        return info


if __name__ == '__main__':
    agent = AMACAgent()
    #df = agent.get_company_list()
    #print(df)

    #result = agent.get_company_detail("101000004390")
    #print(result)

    #df = agent.get_fund_list()
    #print(df)

    result = agent.get_fund_detail('351000130305')
    print(result)

