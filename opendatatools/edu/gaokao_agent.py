# encoding: utf-8

from opendatatools.common import RestAgent
import json
import pandas as pd
from bs4 import BeautifulSoup
import re

province_map = {
	"北京"   : "10003",
	"天津"   : "10006",
	"河北"   : "10016",
	"山西"   : "10010",
	"内蒙古" : "10002",
	"辽宁"   : "10027",
	"吉林"   : "10004",
	"黑龙江" : "10031",
	"上海"   : "10000",
	"江苏"   : "10014",
	"浙江"   : "10018",
	"安徽"   : "10008",
	"福建"   : "10024",
	"江西"   : "10015",
	"山东"   : "10009",
	"河南"   : "10017",
	"湖北"   : "10021",
	"湖南"   : "10022",
	"广东"   : "10011",
	"广西"   : "10012",
	"海南"   : "10019",
	"重庆"   : "10028",
	"四川"   : "10005",
	"贵州"   : "10026",
	"云南"   : "10001",
	"西藏"   : "10025",
	"陕西"   : "10029",
	"甘肃"   : "10023",
	"青海"   : "10030",
	"宁夏"   : "10007",
	"新疆"   : "10013",
	"台湾"   : "10146",
	"香港"   : "10020",
	"澳门"   : "10145",
}

province_map_inv = {v:k for k,v in province_map.items()}

schooltype_map = {
    "本科" : "10032",
    "专科" : "10033",
}

subject_map = {
	"理科" : "10035",
	"文科" : "10034",
    "综合" : "10166",
}
subject_map_inv = {v:k for k,v in subject_map.items()}

batch_map = {
	"本科批"     : "10154",
	"本科一批"   : "10036",
	"本科二批"   : "10037",
	"本科三批"   : "10038",
	"专科批"     : "10155",
	"本科提前批" : "10149",
    "平行第一段" : "10163",
}

batch_map_inv = {v:k for k,v in batch_map.items()}

class EOLAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_score(self, school, province, subject, recruitbatch):
        url = 'https://g.eol.cn/gaokao/school/apitopscorebyyear'
        param = {
            "schoolid" : school,
            "province" : province,
            "type"      : subject,
            "batch"     : recruitbatch,
        }

        response = self.do_request(url, param, method='POST')

        if response is not None:
            rsp = json.loads(response)
            df = pd.DataFrame(rsp)
            print(df)
            return df, ''

        return None, '获取数据失败'

    def get_num_by_page(self, page_no):
        url = 'https://data-gkcx.eol.cn/soudaxue/queryProvinceScore.html'

        param = {
            'messtype' : 'jsonp',
            'lunum' : '1',
            'provinceforschool': '',
            'schooltype' : '',
            'page' : page_no,
            'size' : 10,
            'keyWord' : '',
            'schoolproperty' : '',
            'schoolflag': '',
            'province': '',
            'fstype': '',
            'zhaoshengpici': '',
            'fsyear': '',
        }

        self.add_headers({'Referer' : 'https://gkcx.eol.cn/soudaxue/queryProvinceScoreNum.html'})

        response = self.do_request(url, param=param, method='GET', encoding='utf-8', verify=False)
        if response is not None:
            response = response[5:-2]
            rsp = json.loads(response)
            df = pd.DataFrame(rsp['school'])
            return df, ''

        return None, '获取数据失败'


    def _get_schools(self, province, school_type, subject, page_no):
        url = 'https://g.eol.cn/gaokao/school/listbyareatype/%d?province=%s&schoolType=%s&subject=%s&sort=1'
        url = url % (page_no, province, school_type, subject)

        response = self.do_request(url, None, encoding='utf8')
        data = []

        if response is None:
            return data

        soup = BeautifulSoup(response, "html5lib")
        divs = soup.find_all('div')

        for div in divs:
            if div.has_attr('class') and 'ui-block-a' in div['class'] and 'per45' in div['class']:
                school_id   = div.a['href'].replace('/', '')
                school_name = div.h2.text
                spans = div.p.find_all('span')
                tag_name = ",".join([span.text for span in spans])
                data.append({
                    "school_id"   : school_id,
                    "school_name" : school_name,
                    "tag_name"     : tag_name,
                })

        return data

    def get_schools(self, province, school_type, subject):
        result = []
        page_no = 1
        while True:
            print('getting data from page %d' % page_no)
            data = self._get_schools(province, school_type, subject, page_no)
            page_no = page_no + 1
            result.extend(data)
            if len(data) == 0:
                break

        return result

    def get_school_list(self):

        df_list = []
        for prov_name, province in province_map.items():
            for schooltype_name, school_type in schooltype_map.items():
                for subject_name, subject in subject_map.items():
                    print('working on %s, %s, %s' % (prov_name, schooltype_name, subject_name))
                    data = self.get_schools(province, school_type, subject)
                    if data is not None and len(data) > 0:
                        df = pd.DataFrame(data)
                        df['province']    = prov_name
                        df['school_type'] = schooltype_name
                        df['subject']     =  subject_name
                        df_list.append(df)
                        #print(df)
        result_df = pd.concat(df_list,  ignore_index=True)
        print (result_df)
        return result_df, ''

    def get_score_list_by_school(self, school):
        print ("working on %s" % school)
        df_list = []
        for prov_name, province in province_map.items():
            print ("working on %s" % province_map_inv[province])
            for subject_name, subject in subject_map.items():
                for batch_name, batch in batch_map.items():
                    df, msg = self.get_score(school, province, subject, batch)
                    if df is None:
                        continue
                    #print (df)
                    df['max'] = df['max'].replace('--', 0).replace('', 0)
                    df['min'] = df['min'].replace('--', 0).replace('', 0)
                    df['var'] = df['var'].replace('--', 0).replace('', 0)
                    df['school_id']     = school
                    df['recruit_batch']  = batch_map_inv[batch]
                    df['subject']       = subject_map_inv[subject]
                    df['province']      = province_map_inv[province]
                    df_list.append(df)
        result_df = pd.concat(df_list, ignore_index=True)
        return result_df, ''

    def get_major_list(self):
        url = "http://www.cdgdc.edu.cn/webrms/wwwroot/zgxwyyjsjyxxw/xwyyjsjyxx/xwsytjxx/xk/xkzyml/276559.shtml"
        response = self.do_request(url, None, encoding='gb2312')
        response = response.replace("\n;", '').replace("&nbsp;", '').replace('　', '')
        #print (response)
        data = []

        if response == '':
            return data

        soup = BeautifulSoup(response, "html5lib")
        major_list = []
        for i in range(567):
            result = soup.select("tbody > tr")[i]
            text = result.get_text()
            if text != '':
                major_list.append(text)
        return major_list

    def get_major(self):
        major_list  = self.get_major_list()
        majors      = []
        first_level = []
        category    = []
        for item in major_list:
            if ('学科门类' not in item) & (item[-1] != '类'):
                majors.append(item)
            elif (item[-1] == '类'):
                first_level.append(item)
            else:
                category.append(item)
        return category, first_level, majors

    def get_score_major_by_school_flag_and_page(self, school_flag, page_no):
        url = "https://data-gkcx.eol.cn/soudaxue/querySpecialtyScore.html"
        param = {
            'messtype': 'jsonp',
            'provinceforschool': '',
            'schooltype':'',
            'page': page_no,
            'size': 50,
            'keyWord': '',
            'schoolproperty': '',
            'schoolflag': school_flag,
            'province': '',
            'fstype': '',
            'zhaoshengpici': '',
            'fsyear': '',
        }

        self.add_headers({'Referer': 'https://gkcx.eol.cn/soudaxue/querySpecialtyScore.html'})

        response = self.do_request(url, param=param, method='GET', encoding='utf-8', verify=False)
        if response is not None:
            response = response[5:-2]
            rsp = json.loads(response)
            df = pd.DataFrame(rsp['school'])[['schoolid', 'schoolname', 'specialtyname', 'localprovince', 'studenttype', 'year', 'batch', 'max', 'min', 'var']]
            df['max'] = df['max'].replace('--', 0).replace('', 0)
            df['min'] = df['min'].replace('--', 0).replace('', 0)
            df['var'] = df['var'].replace('--', 0).replace('', 0)
            num = rsp['totalRecord']['num']
            return df, num, ''

        return None, '', '获取数据失败'

    def get_major_rank(self, xid):
        url = 'http://souky.eol.cn/assess_result.php'
        param = {
            'xid': xid,
            'flag': 1,
        }

        response = self.do_request(url, param=param, method='GET', encoding='gbk')
        if response is not None:
            rsp = json.loads(response)
            return rsp, ''

        return None, '获取数据失败'

    def get_batch_scores(self):
        url = 'http://www.eol.cn/html/g/fsx/index.shtml'
        response = self.do_request(url, encoding='gb2312')
        soup = BeautifulSoup(response, "html5lib")

        provinces = soup.find_all("div", class_ = "area-name")
        province_list = []
        for province in provinces:
            province_list.append(province.text)

        score_list = []
        scores = soup.find_all("div", attrs={"class" : 'area-table-item'})
        for score in scores:
            if len(score['class']) == 1:
                temp = []
                for item in score.select("table tbody tr td"):
                    temp.append(item.text)
                score_list.append(temp)
        df = pd.DataFrame(score_list)
        df['province'] = province_list
        df.set_index('province', inplace=True)
        return df, ''

    def get_batch_scores_hist(self):
        url = 'http://www.eol.cn/html/g/fsx/index.shtml'
        response = self.do_request(url, encoding='gb2312')
        soup = BeautifulSoup(response, "html5lib")

        provinces = soup.find_all("div", class_="area-name")
        province_list = []
        for province in provinces:
            province_list.append(province.text)

        score_list = []
        scores = soup.find_all("div", attrs={"class": 'area-table-item'})
        i = 0
        for score in scores:
            if len(score['class']) == 1:
                province = province_list[i]
                j = -1
                i += 1
            else:
                temp = [province, 2017-j % 5]
                for item in score.select("table tbody tr td"):
                    temp.append(item.text)
                score_list.append(temp)
            j += 1
        df = pd.DataFrame(score_list)
        df.set_index(0, inplace=True)
        return df, ''

    def get_batch_score_hist_break(self):
        url = "https://data-gkcx.eol.cn/soudaxue/queryProvince.html"
        param = {
            'messtype': 'jsonp',
            'luqutype3':'',
            'province3':'',
            'year3':'',
            'luqupici3':'',
            'page': 1,
            'size': 10,
        }
        response = self.do_request(url, param=param, method='GET', verify=False)
        print (response)

if __name__ == "__main__":

    '''
    school_list = [
        '102',
        '104',
        '105',
        '107',
        '109',
        '111',
        '114',
        '119',
        '1218',
        '1219',
        '122',
        '123',
        '125',
        '126',
        '127',
        '131',
        '132',
        '134',
        '138',
        '140',
        '143',
        '1457',
        '31',
        '3255',
        '330',
        '332',
        '34',
        '42',
        '44',
        '45',
        '46',
        '47',
        '52',
        '557',
        '59',
        '60',
        '61',
        '66',
        '661',
        '73',
        '939',
        '97',
        '99',
    ]
    '''

    import time
    agent = EOLAgent()
    df_list = []
    for school in  ['31', '52', '99', '661', '939', '1219']:#school_list:
        df, msg = agent.get_score(school, '10018', '10166', '10163')
        df['year'] = df['year'].apply(lambda x : str(x))
        df = df[df['year'] == '2017']
        df['school_id'] = school
        df_list.append(df)
        time.sleep(1)

    df = pd.concat(df_list)
    df.to_csv('1.csv')
