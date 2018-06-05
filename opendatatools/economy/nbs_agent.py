# encoding: utf-8

from opendatatools.common import RestAgent
import json
import pandas as pd

nbs_city_map = {
    '北京':'110000',
    '天津':'120000',
    '石家庄':'130100',
    '唐山':'130200',
    '秦皇岛':'130300',
    '太原':'140100',
    '呼和浩特':'150100',
    '包头':'150200',
    '沈阳':'210100',
    '大连':'210200',
    '丹东':'210600',
    '锦州':'210700',
    '长春':'220100',
    '吉林':'220200',
    '哈尔滨':'230100',
    '牡丹江':'231000',
    '上海':'310000',
    '南京':'320100',
    '无锡':'320200',
    '徐州':'320300',
    '扬州':'321000',
    '杭州':'330100',
    '宁波':'330200',
    '温州':'330300',
    '金华':'330700',
    '合肥':'340100',
    '蚌埠':'340300',
    '安庆':'340800',
    '福州':'350100',
    '厦门':'350200',
    '泉州':'350500',
    '南昌':'360100',
    '九江':'360400',
    '赣州':'360700',
    '济南':'370100',
    '青岛':'370200',
    '烟台':'370600',
    '济宁':'370800',
    '郑州':'410100',
    '洛阳':'410300',
    '平顶山':'410400',
    '武汉':'420100',
    '宜昌':'420500',
    '襄阳':'420600',
    '长沙':'430100',
    '岳阳':'430600',
    '常德':'430700',
    '广州':'440100',
    '韶关':'440200',
    '深圳':'440300',
    '湛江':'440800',
    '惠州':'441300',
    '南宁':'450100',
    '桂林':'450300',
    '北海':'450500',
    '海口':'460100',
    '三亚':'460200',
    '重庆':'500000',
    '成都':'510100',
    '泸州':'510500',
    '南充':'511300',
    '贵阳':'520100',
    '遵义':'520300',
    '昆明':'530100',
    '大理':'532900',
    '西安':'610100',
    '兰州':'620100',
    '西宁':'630100',
    '银川':'640100',
    '乌鲁木齐':'650100',
}

nbs_region_map = {
    '北京'            : '110000',
    '天津'            : '120000',
    '河北省'          : '130000',
    '山西省'          : '140000',
    '内蒙古自治区'    : '150000',
    '辽宁省'          : '210000',
    '吉林省'          : '220000',
    '黑龙江省'        : '230000',
    '上海'            : '310000',
    '江苏省'          : '320000',
    '浙江省'          : '330000',
    '安徽省'          : '340000',
    '福建省'          : '350000',
    '江西省'          : '360000',
    '山东省'          : '370000',
    '河南省'          : '410000',
    '湖北省'          : '420000',
    '湖南省'          : '430000',
    '广东省'          : '440000',
    '广西壮族自治区'  : '450000',
    '海南省'          : '460000',
    '重庆'            : '500000',
    '四川省'          : '510000',
    '贵州省'          : '520000',
    '云南省'          : '530000',
    '西藏自治区'      : '540000',
    '陕西省'          : '610000',
    '甘肃省'          : '620000',
    '青海省'          : '630000',
    '宁夏回族自治区'  : '640000',
    '新疆维吾尔自治区': '650000',
}

nbs_indicator_map_df = {
    # 地方GDP
    'A010101':'地区生产总值_累计值(亿元)',
    'A010103':'地区生产总值指数(上年=100)_累计值(%)',

}

nbs_indicator_map = {

    # 年度GDP
    'A020101':'国民总收入(亿元)',
    'A020102':'国内生产总值(亿元)',
    'A020103':'第一产业增加值(亿元)',
    'A020104':'第二产业增加值(亿元)',
    'A020105':'第三产业增加值(亿元)',
    'A020106':'人均国内生产总值(元)',

    # 人口数量
    'A030101':'年末总人口(万人)',
    'A030102':'男性人口(万人)',
    'A030103':'女性人口(万人)',
    'A030104':'城镇人口(万人)',
    'A030105':'乡村人口(万人)',

    # 人口结构
    'A030301':'年末总人口(万人)',
    'A030302':'0-14岁人口(万人)',
    'A030303':'15-64岁人口(万人)',
    'A030304':'65岁及以上人口(万人)',
    'A030305':'总抚养比(%)',
    'A030306':'少儿抚养比(%)',
    'A030307':'老年抚养比(%)',

    # 70 个大中城市商品房价格情况
    'A010801':'新建住宅销售价格指数(上月=100)',
    'A010802':'新建住宅销售价格指数(上年=100)',
    'A010803':'新建住宅销售价格指数(2015=100)',
    'A010804':'新建商品住宅销售价格指数(上月=100)',
    'A010805':'新建商品住宅销售价格指数(上年=100)',
    'A010806':'新建商品住宅销售价格指数(2015=100)',
    'A010807':'二手住宅销售价格指数(上月=100)',
    'A010808':'二手住宅销售价格指数(上年=100)',
    'A010809':'二手住宅销售价格指数(2015=100)',
    'A01080A':'90平米及以下新建商品住宅销售价格指数(上月=100)',
    'A01080B':'90平米及以下新建商品住宅销售价格指数(上年=100)',
    'A01080C':'90平米及以下新建商品住宅销售价格指数(2015=100)',
    'A01080D':'90-144平米新建商品住宅销售价格指数(上月=100)',
    'A01080E':'90-144平米新建商品住宅销售价格指数(上年=100)',
    'A01080F':'90-144平米新建商品住宅销售价格指数(2015=100)',
    'A01080G':'144平米以上新建商品住宅销售价格指数(上月=100)',
    'A01080H':'144平米以上新建商品住宅销售价格指数(上年=100)',
    'A01080I':'144平米以上新建商品住宅销售价格指数(2015=100)',
    'A01080J':'90平米及以下二手住宅销售价格指数(上月=100)',
    'A01080K':'90平米及以下二手住宅销售价格指数(上年=100)',
    'A01080L':'90平米及以下二手住宅销售价格指数(2015=100)',
    'A01080M':'90-144平米二手住宅销售价格指数(上月=100)',
    'A01080N':'90-144平米二手住宅销售价格指数(上年=100)',
    'A01080O':'90-144平米二手住宅销售价格指数(2015=100)',
    'A01080P':'144平米以上二手住宅销售价格指数(上月=100)',
    'A01080Q':'144平米以上二手住宅销售价格指数(上年=100)',
    'A01080R':'144平米以上二手住宅销售价格指数(2015=100)',

    #CPI 相关
    'A01010101':'居民消费价格指数(上年同月=100)',
    'A01010102':'食品烟酒类居民消费价格指数(上年同月=100)',
    'A01010103':'衣着类居民消费价格指数(上年同月=100)',
    'A01010104':'居住类居民消费价格指数(上年同月=100)',
    'A01010105':'生活用品及服务类居民消费价格指数(上年同月=100)',
    'A01010106':'交通和通信类居民消费价格指数(上年同月=100)',
    'A01010107':'教育文化和娱乐类居民消费价格指数(上年同月=100)',
    'A01010108':'医疗保健类居民消费价格指数(上年同月=100)',
    'A01010109':'其他用品和服务类居民消费价格指数(上年同月=100)',

    # PPI相关
    'A01080101':'工业生产者出厂价格指数(上年同月=100)',
    'A01080102':'生产资料工业生产者出厂价格指数(上年同月=100)',
    'A01080103':'生活资料工业生产者出厂价格指数(上年同月=100)',

    'A010301': '工业生产者购进价格指数(上年同月=100)',
    'A010302': '工业生产者出厂价格指数(上年同月=100)',

    # GDP相关
    'A010101':'国内生产总值_当季值(亿元)',
    'A010102':'国内生产总值_累计值(亿元)',
    'A010103':'第一产业增加值_当季值(亿元)',
    'A010104':'第一产业增加值_累计值(亿元)',
    'A010105':'第二产业增加值_当季值(亿元)',
    'A010106':'第二产业增加值_累计值(亿元)',
    'A010107':'第三产业增加值_当季值(亿元)',
    'A010108':'第三产业增加值_累计值(亿元)',
    'A010109':'农林牧渔业增加值_当季值(亿元)',
    'A01010A':'农林牧渔业增加值_累计值(亿元)',
    'A01010B':'工业增加值_当季值(亿元)',
    'A01010C':'工业增加值_累计值(亿元)',
    'A01010D':'制造业增加值_当季值(亿元)',
    'A01010E':'制造业增加值_累计值(亿元)',
    'A01011D':'建筑业增加值_当季值(亿元)',
    'A01011E':'建筑业增加值_累计值(亿元)',
    'A01011F':'批发和零售业增加值_当季值(亿元)',
    'A01011G':'批发和零售业增加值_累计值(亿元)',
    'A01011H':'交通运输、仓储和邮政业增加值_当季值(亿元)',
    'A01011I':'交通运输、仓储和邮政业增加值_累计值(亿元)',
    'A01011J':'住宿和餐饮业增加值_当季值(亿元)',
    'A01011K':'住宿和餐饮业增加值_累计值(亿元)',
    'A01011L':'金融业增加值_当季值(亿元)',
    'A01011M':'金融业增加值_累计值(亿元)',
    'A01011N':'房地产业增加值_当季值(亿元)',
    'A01011O':'房地产业增加值_累计值(亿元)',
    'A01011P':'信息传输、软件和信息技术服务业增加值_当季值(亿元)',
    'A01011Q':'信息传输、软件和信息技术服务业增加值_累计值(亿元)',
    'A01011R':'租赁和商务服务业增加值_当季值(亿元)',
    'A01011S':'租赁和商务服务业增加值_累计值(亿元)',
    'A01012P':'其他行业增加值_当季值(亿元)',
    'A01012Q':'其他行业增加值_累计值(亿元)',

    # GDP 增速有关
    'A010401':'国内生产总值环比增长速度(%)',

    # M0M1M2相关
    'A1B0101':'货币和准货币(M2)供应量_期末值(亿元)',
    'A1B0102':'货币和准货币(M2)供应量_同比增长(%)',
    'A1B0103':'货币(M1)供应量_期末值(亿元)',
    'A1B0104':'货币(M1)供应量_同比增长(%)',
    'A1B0105':'流通中现金(M0)供应量_期末值(亿元)',
    'A1B0106':'流通中现金(M0)供应量_同比增长(%)',

    # 财政收入
    'A1A0101':'国家财政收入_当期值(亿元)',
    'A1A0102':'国家财政收入_累计值(亿元)',
    'A1A0103':'国家财政收入_累计增长(%)',

    # 财政支出
    'A1A0201':'国家财政支出(不含债务还本)_当期值(亿元)',
    'A1A0202':'国家财政支出(不含债务还本)_累计值(亿元)',
    'A1A0203':'国家财政支出(不含债务还本)_累计增长(%)',

    # 制造业 PMI 相关
    'A190101':'制造业采购经理指数(%)',
    'A190102':'生产指数(%)',
    'A190103':'新订单指数(%)',
    'A190104':'新出口订单指数(%)',
    'A190105':'在手订单指数(%)',
    'A190106':'产成品库存指数(%)',
    'A190107':'采购量指数(%)',
    'A190108':'进口指数(%)',
    'A190109':'出厂价格指数(%)',
    'A190119':'主要原材料购进价格指数(%)',
    'A19011A':'原材料库存指数(%)',
    'A19011B':'从业人员指数(%)',
    'A19011C':'供应商配送时间指数(%)',
    'A19011D':'生产经营活动预期指数(%)',

    # 非织造业PMI
    'A190201':'非制造业商务活动指数(%)',
    'A190202':'新订单指数(%)',
    'A190203':'新出口订单指数(%)',
    'A190204':'在手订单指数(%)',
    'A190205':'存货指数(%)',
    'A190206':'投入品价格指数(%)',
    'A190207':'销售价格指数(%)',
    'A190208':'从业人员指数(%)',
    'A190209':'供应商配送时间指数(%)',
    'A19020A':'业务活动预期指数(%)',

    # 综合PMI
    'A190301':'综合PMI产出指数(%)',

    # 进出口情况
    'A160101':'进出口总值_当期值(千美元)',
    'A160102':'进出口总值_同比增长(%)',
    'A160103':'进出口总值_累计值(千美元)',
    'A160104':'进出口总值_累计增长(%)',
    'A160105':'出口总值_当期值(千美元)',
    'A160106':'出口总值_同比增长(%)',
    'A160107':'出口总值_累计值(千美元)',
    'A160108':'出口总值_累计增长(%)',
    'A160109':'进口总值_当期值(千美元)',
    'A16010A':'进口总值_同比增长(%)',
    'A16010B':'进口总值_累计值(千美元)',
    'A16010C':'进口总值_累计增长(%)',
    'A16010D':'进出口差额_当期值(千美元)',
    'A16010E':'进出口差额_累计值(千美元)',

    # FDI相关
    'A160201':'外商直接投资合同项目数_累计值(个)',
    'A160202':'外商直接投资合同项目数_累计增长(%)',
    'A160203':'合资经营企业外商直接投资合同项目数_累计值(个)',
    'A160204':'合资经营企业外商直接投资合同项目数_累计增长(%)',
    'A160205':'合作经营企业外商直接投资合同项目数_累计值(个)',
    'A160206':'合作经营企业外商直接投资合同项目数_累计增长(%)',
    'A160207':'外资企业外商直接投资合同项目数_累计值(个)',
    'A160208':'外资企业外商直接投资合同项目数_累计增长(%)',
    'A160209':'外商投资股份制企业外商直接投资合同项目数_累计值(个)',
    'A16020A':'外商投资股份制企业外商直接投资合同项目数_累计增长(%)',
    'A16020B':'实际利用外商直接投资金额_累计值(百万美元)',
    'A16020C':'实际利用外商直接投资金额_累计增长(%)',
    'A16020D':'合资经营企业实际利用外商直接投资金额_累计值(百万美元)',
    'A16020E':'合资经营企业实际利用外商直接投资金额_累计增长(%)',
    'A16020F':'合作经营企业实际利用外商直接投资金额_累计值(百万美元)',
    'A16020G':'合作经营企业实际利用外商直接投资金额_累计增长(%)',
    'A16020H':'外资企业实际利用外商直接投资金额_累计值(百万美元)',
    'A16020I':'外资企业实际利用外商直接投资金额_累计增长(%)',
    'A16020J':'外商投资股份制企业实际利用外商直接投资金额_累计值(百万美元)',
    'A16020K':'外商投资股份制企业实际利用外商直接投资金额_累计增长(%)',

    # 社会消费品零售总额
    'A150101':'社会消费品零售总额_当期值(亿元)',
    'A150102':'社会消费品零售总额_累计值(亿元)',
    'A150103':'社会消费品零售总额_同比增长(%)',
    'A150104':'社会消费品零售总额_累计增长(%)',
    'A150105':'限上单位消费品零售额_当期值(亿元)',
    'A150106':'限上单位消费品零售额_累计值(亿元)',
    'A150107':'限上单位消费品零售额_同比增长(%)',
    'A150108':'限上单位消费品零售额_累计增长(%)',

    # 网上零售额
    'A150801':'网上零售额_累计值(亿元)',
    'A150802':'网上零售额_累计增长(%)',
    'A150803':'实物商品网上零售额_累计值(亿元)',
    'A150804':'实物商品网上零售额_累计增长(%)',
    'A150805':'吃类实物商品网上零售额_累计值(亿元)',
    'A150806':'吃类实物商品网上零售额_累计增长(%)',
    'A150807':'穿类实物商品网上零售额_累计值(亿元)',
    'A150808':'穿类实物商品网上零售额_累计增长(%)',
    'A150809':'用类实物商品网上零售额_累计值(亿元)',
    'A150810':'用类实物商品网上零售额_累计增长(%)',

    # 房地产开发投资
    'A140101':'房地产投资_累计值(亿元)',
    'A140102':'房地产投资_累计增长(%)',
    'A140103':'房地产配套工程投资_累计值(亿元)',
    'A140104':'房地产配套工程投资_累计增长(%)',
    'A140105':'房地产住宅投资_累计值(亿元)',
    'A140106':'房地产住宅投资_累计增长(%)',
    'A140107':'90平方米及以下住房投资_累计值(亿元)',
    'A140108':'90平方米及以下住房投资_累计增长(%)',
    'A140109':'144平方米以上住房投资_累计值(亿元)',
    'A14010A':'144平方米以上住房投资_累计增长(%)',
    'A14010B':'别墅、高档公寓投资_累计值(亿元)',
    'A14010C':'别墅、高档公寓投资_累计增长(%)',
    'A14010D':'房地产办公楼投资_累计值(亿元)',
    'A14010E':'房地产办公楼投资_累计增长(%)',
    'A14010F':'房地产商业营业用房投资_累计值(亿元)',
    'A14010G':'房地产商业营业用房投资_累计增长(%)',
    'A14010H':'其它房地产投资_累计值(亿元)',
    'A14010I':'其它房地产投资_累计增长(%)',
    'A14010J':'房地产开发建筑工程投资_累计值(亿元)',
    'A14010K':'房地产开发建筑工程投资_累计增长(%)',
    'A14010L':'房地产开发安装工程投资_累计值(亿元)',
    'A14010M':'房地产开发安装工程投资_累计增长(%)',
    'A14010N':'房地产设备工器具购置投资_累计值(亿元)',
    'A14010O':'房地产设备工器具购置投资_累计增长(%)',
    'A14010P':'房地产其它费用投资_累计值(亿元)',
    'A14010Q':'房地产其它费用投资_累计增长(%)',
    'A14010R':'房地产土地购置费_累计值(亿元)',
    'A14010S':'房地产土地购置费_累计增长(%)',
    'A14010T':'房地产开发计划总投资_累计值(亿元)',
    'A14010U':'房地产开发计划总投资_累计增长(%)',
    'A14010V':'房地产开发新增固定资产投资_累计值(亿元)',
    'A14010W':'房地产开发新增固定资产投资_累计增长(%)',

    # 固定资产投资类
    'A130101':'固定资产投资完成额_累计值(亿元)',
    'A130102':'固定资产投资完成额_累计增长(%)',
    'A130103':'国有及国有控股固定资产投资额_累计值(亿元)',
    'A130104':'国有及国有控股固定资产投资额_累计增长(%)',
    'A130105':'房地产开发投资额_累计值(亿元)',
    'A130106':'房地产开发投资额_累计增长(%)',
    'A130107':'第一产业固定资产投资完成额_累计值(亿元)',
    'A130108':'第一产业固定资产投资完成额_累计增长(%)',
    'A130109':'第二产业固定资产投资完成额_累计值(亿元)',
    'A13010A':'第二产业固定资产投资完成额_累计增长(%)',
    'A13010B':'第三产业固定资产投资完成额_累计值(亿元)',
    'A13010C':'第三产业固定资产投资完成额_累计增长(%)',
    'A13010D':'中央项目固定资产投资完成额_累计值(亿元)',
    'A13010E':'中央项目固定资产投资完成额_累计增长(%)',
    'A13010F':'地方项目固定资产投资完成额_累计值(亿元)',
    'A13010G':'地方项目固定资产投资完成额_累计增长(%)',
    'A13010H':'新建固定资产投资完成额_累计值(亿元)',
    'A13010I':'新建固定资产投资完成额_累计增长(%)',
    'A13010J':'扩建固定资产投资完成额_累计值(亿元)',
    'A13010K':'扩建固定资产投资完成额_累计增长(%)',
    'A13010L':'改建固定资产投资完成额_累计值(亿元)',
    'A13010M':'改建固定资产投资完成额_累计增长(%)',
    'A13010N':'建筑安装工程固定资产投资完成额_累计值(亿元)',
    'A13010O':'建筑安装工程固定资产投资完成额_累计增长(%)',
    'A13010P':'设备工器具购置固定资产投资完成额_累计值(亿元)',
    'A13010Q':'设备工器具购置固定资产投资完成额_累计增长(%)',
    'A13010R':'其他费用固定资产投资完成额_累计值(亿元)',
    'A13010S':'其他费用固定资产投资完成额_累计增长(%)',
    'A13010T':'房屋施工面积_累计值(万平方米)',
    'A13010U':'房屋施工面积_累计增长(%)',
    'A13010V':'房屋竣工面积_累计值(万平方米)',
    'A13010W':'房屋竣工面积_累计增长(%)',
    'A13010X':'新增固定资产_累计值(亿元)',
    'A13010Y':'新增固定资产_累计增长(%)',

}

class NBSAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def prepare_cookies(self, url):
        response = self.do_request(url, None)
        if response is not None:
            cookies = self.get_cookies()
            return cookies
        else:
            return None

    def get_indicator_map(self):
        return pd.DataFrame(list(nbs_indicator_map.items()), columns=['indicator', 'name'])

    def get_region_map(self):
        return pd.DataFrame(list(nbs_region_map.items()), columns=['region', 'name'])

    def get_city_map(self):
        return pd.DataFrame(list(nbs_city_map.items()), columns=['city', 'name'])

    # 获取全国指标
    def _get_qg_indicator(self, cn, category, dbcode = 'hgyd'):
        url = 'http://data.stats.gov.cn/easyquery.htm'
        param = {
            "m": "QueryData",
            "dbcode": dbcode,
            "rowcode": "zb",
            "colcode": "sj",
            "wds" : '[]',
            "dfwds": '[{"wdcode":"sj","valuecode":"LAST36"}, {"wdcode": "zb", "valuecode": "%s"}]' % (category),
        }

        url = 'http://data.stats.gov.cn/easyquery.htm?cn=%s&zb=%s' % (cn, category)
        cookies = self.prepare_cookies(url)

        response = self.do_request(url, param, cookies=cookies)
        rsp = json.loads(response)
        code = rsp['returncode']
        data = rsp['returndata']

        records = data['datanodes']
        result_list = []
        for record in records:
            value = record['data']['data']
            strvalue = record['data']['strdata']
            date  = record['wds'][1]['valuecode']
            indicator = record['wds'][0]['valuecode']

            if indicator in nbs_indicator_map:
                indicator_name = nbs_indicator_map[indicator]
            else:
                indicator_name = ""

            result_list.append({
                "indicator" : indicator,
                "indicator_name" : indicator_name,
                "date"       : date,
                "value"     : value,
                "strvalue"  : strvalue,

            })

        return pd.DataFrame(result_list), ""

    def _get_df_indicator(self, region, cn, category, dbcode = 'fsyd'):
        if region not in nbs_region_map:
            return None, '不合法的省份名称, 请通过get_region_map接口获取正确的省份名称'

        region_code = nbs_region_map[region]
        url = 'http://data.stats.gov.cn/easyquery.htm'

        param = {
            "m": "QueryData",
            "dbcode": dbcode,
            "rowcode": "zb",
            "colcode": "sj",
            "wds" : '[{"wdcode": "region", "valuecode": "%s"}]' % (region_code),
            "dfwds": '[{"wdcode":"zb","valuecode":"%s"}, {"wdcode":"sj","valuecode":"LAST36"}]' % (category),
        }

        url = 'http://data.stats.gov.cn/easyquery.htm?cn=%s&zb=%s&reg=%s' % (cn, category,region_code)
        cookies = self.prepare_cookies(url)

        response = self.do_request(
            url, param,
            cookies=cookies
        )
        rsp = json.loads(response)
        code = rsp['returncode']
        data = rsp['returndata']

        records = data['datanodes']
        result_list = []
        for record in records:
            value = record['data']['data']
            strvalue = record['data']['strdata']
            date  = record['wds'][2]['valuecode']
            indicator = record['wds'][0]['valuecode']

            if indicator in nbs_indicator_map_df:
                indicator_name = nbs_indicator_map_df[indicator]
            elif indicator in nbs_indicator_map:
                indicator_name = nbs_indicator_map[indicator]
            else:
                indicator_name = ""

            result_list.append({
                "region"       : region,
                "indicator" : indicator,
                "indicator_name" : indicator_name,
                "date"       : date,
                "value"     : value,
                "strvalue"  : strvalue,

            })

        return pd.DataFrame(result_list), ""

    def _get_city_indicator(self, city, cn, category, dbcode = 'csyd'):
        if city not in nbs_city_map:
            return None, '不合法的城市名称，请通过get_city_map获取正确的城市名称'

        region_code = nbs_city_map[city]
        url = 'http://data.stats.gov.cn/easyquery.htm'

        param = {
            "m": "QueryData",
            "dbcode": dbcode,
            "rowcode": "zb",
            "colcode": "sj",
            "wds" : '[{"wdcode": "region", "valuecode": %s}]' % (region_code),
            "dfwds": '[{"wdcode":"sj","valuecode":"LAST36"}]',
        }

        url = 'http://data.stats.gov.cn/easyquery.htm?cn=%s&zb=%s&reg=%s' % (cn, category,region_code)
        cookies = self.prepare_cookies(url)

        response = self.do_request(
            url, param,
            cookies=cookies
        )
        rsp = json.loads(response)
        code = rsp['returncode']
        data = rsp['returndata']

        records = data['datanodes']
        result_list = []
        for record in records:
            value = record['data']['data']
            strvalue = record['data']['strdata']
            date  = record['wds'][2]['valuecode']
            indicator = record['wds'][0]['valuecode']

            if indicator in nbs_indicator_map:
                indicator_name = nbs_indicator_map[indicator]
            else:
                indicator_name = ""

            result_list.append({
                "city"       : city,
                "indicator" : indicator,
                "indicator_name" : indicator_name,
                "date"       : date,
                "value"     : value,
                "strvalue"  : strvalue,

            })

        return pd.DataFrame(result_list), ""

    '''
    年度数据
    '''

    # 年度GDP
    def get_gdp_y(self):
        return self._get_qg_indicator('C01', 'A0201', dbcode='hgnd')

    def get_region_gdp_y(self, region):
        return self._get_fs_indicator('E0103', 'A0201', dbcode='fsnd')

    def get_population_size_y(self):
        return self._get_qg_indicator('C01', 'A0301', dbcode='hgnd')

    def get_population_structure_y(self):
        return self._get_qg_indicator('C01', 'A0303', dbcode='hgnd')

    # 70 个大中城市住宅销售价格指数
    def get_house_price_index(self, city):
        return self._get_city_indicator(city, 'E0104', 'A0108', 'csyd')

    def get_cpi(self):
        return self._get_qg_indicator('A01', 'A010101', dbcode = 'hgyd')

    def get_region_cpi(self, region):
        return self._get_df_indicator(region, 'E0101', 'A010101', dbcode = 'fsyd')

    def get_ppi(self):
        return self._get_qg_indicator('A01', 'A010801', dbcode = 'hgyd')

    def get_region_ppi(self, region):
        return self._get_df_indicator(region, 'E0101', 'A0103', dbcode = 'fsyd')

    def get_gdp(self):
        return self._get_qg_indicator('B01', 'A0101', dbcode='hgjd')

    def get_region_gdp(self, region):
        return self._get_df_indicator(region, 'E0102', 'A0101', dbcode='fsjd')

    def get_gdp_q2q(self):
        return self._get_qg_indicator('B01', 'A0104', dbcode = 'hgjd')

    def get_M0_M1_M2(self):
        return self._get_qg_indicator('A01', 'A1B01', dbcode = 'hgyd')

    def get_fiscal_revenue(self):
        return self._get_qg_indicator('A01', 'A1A01', dbcode = 'hgyd')

    def get_fiscal_expend(self):
        return self._get_qg_indicator('A01', 'A1A02', dbcode = 'hgyd')

    def get_manufacturing_pmi(self):
        return self._get_qg_indicator('A01', 'A1901', dbcode = 'hgyd')

    def get_non_manufacturing_pmi(self):
        return self._get_qg_indicator('A01', 'A1902', dbcode = 'hgyd')

    def get_pmi(self):
        return self._get_qg_indicator('A01', 'A1903', dbcode = 'hgyd')

    def get_import_export(self):
        return self._get_qg_indicator('A01', 'A1601', dbcode = 'hgyd')

    def get_fdi(self):
        return self._get_qg_indicator('A01', 'A1602', dbcode = 'hgyd')

    def get_retail_sales(self):
        return self._get_qg_indicator('A01', 'A1501', dbcode = 'hgyd')

    def get_online_retail_sales(self):
        return self._get_qg_indicator('A01', 'A1508', dbcode='hgyd')

    def get_online_retail_sales(self):
        return self._get_qg_indicator('A01', 'A1508', dbcode='hgyd')

    def get_realestate_investment(self):
        return self._get_qg_indicator('A01', 'A1401', dbcode='hgyd')

    def get_region_realestate_investment(self, region):
        return self._get_df_indicator(region, 'E0101', 'A1401', dbcode='fsyd')

    def get_fixed_asset_investment(self):
        return self._get_qg_indicator('A01', 'A1301', dbcode='hgyd')

    def get_region_fixed_asset_investment(self, region):
        return self._get_df_indicator(region, 'E0101', 'A1301', dbcode='fsyd')
