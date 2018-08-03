# encoding: utf-8

import json
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from opendatatools.common import RestAgent

index_weight_2018 = \
'''
<html>
 <head></head>
 <body>
  <div class="detail-content">
   <table cellpadding="0" cellspacing="0">
    <colgroup>
     <col width="64" span="9" style="width:64px" />
    </colgroup>
    <tbody>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="72">品种名称</td>
      <td width="92">南华商品指数</td>
      <td width="90">南华工业品指数</td>
      <td width="79">南华金属指数</td>
      <td width="78">南华能化指数</td>
      <td width="77">南华农产品指数</td>
      <td width="85">南华贵金属指数</td>
      <td width="79">南华黑色指数</td>
      <td width="80">南华有色金属指数</td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">螺纹钢</td>
      <td width="90">11.26%</td>
      <td width="87">14.50%</td>
      <td width="78">25.00%</td>
      <td width="78"><br /></td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79" style="word-break: break-all;">38.11%</td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">铜</td>
      <td width="90">10.57%</td>
      <td width="87">13.71%</td>
      <td width="78">25.00%</td>
      <td width="78"><br /></td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80">51.56%</td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">原油</td>
      <td width="90">9.52%</td>
      <td width="87">10.73%</td>
      <td width="78"><br /></td>
      <td width="78">14.75%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">铁矿石</td>
      <td width="90">8.45%</td>
      <td width="87">10.53%</td>
      <td width="78">23.23%</td>
      <td width="78"><br /></td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79" style="word-break: break-all;">27.26%</td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">焦炭</td>
      <td width="90">7.23%</td>
      <td width="87">8.98%</td>
      <td width="78"><br /></td>
      <td width="78">15.96%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79" style="word-break: break-all;">23.24%</td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">天然橡胶</td>
      <td width="90">6.74%</td>
      <td width="87">9.15%</td>
      <td width="78"><br /></td>
      <td width="78">19.32%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">豆粕</td>
      <td width="90">4.88%</td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">20.54%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">黄金</td>
      <td width="90">4.66%</td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77"><br /></td>
      <td width="85">55.80%</td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">白银</td>
      <td width="90">4.32%</td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77"><br /></td>
      <td width="85">44.20%</td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">焦煤</td>
      <td width="90">3.93%</td>
      <td width="87">4.56%</td>
      <td width="78"><br /></td>
      <td width="78">6.78%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79" style="word-break: break-all;">11.39%</td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">镍</td>
      <td width="90">3.65%</td>
      <td width="87">4.89%</td>
      <td width="78">9.84%</td>
      <td width="78"><br /></td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80">17.25%</td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">白糖</td>
      <td width="90">3.30%</td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">13.91%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">聚乙烯</td>
      <td width="90">3.18%</td>
      <td width="87">4.02%</td>
      <td width="78"><br /></td>
      <td width="78">7.42%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">豆油</td>
      <td width="90">3.12%</td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">13.16%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">锌</td>
      <td width="90">3.04%</td>
      <td width="87">4.00%</td>
      <td width="78">8.25%</td>
      <td width="78"><br /></td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80">14.66%</td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">PTA</td>
      <td width="90">3.01%</td>
      <td width="87">3.85%</td>
      <td width="78"><br /></td>
      <td width="78">7.25%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">棕榈油</td>
      <td width="90">2.76%</td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">11.62%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">聚丙烯</td>
      <td width="90">2.38%</td>
      <td width="87">3.01%</td>
      <td width="78"><br /></td>
      <td width="78">5.51%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">甲醇</td>
      <td width="90">2.00%</td>
      <td width="87">2.42%</td>
      <td width="78"><br /></td>
      <td width="78">4.59%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">一号棉</td>
      <td width="90">2.00%</td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">7.30%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">玻璃</td>
      <td width="90"><br /></td>
      <td width="87">2.00%</td>
      <td width="78"><br /></td>
      <td width="78">3.31%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">铝</td>
      <td width="90"><br /></td>
      <td width="87">3.65%</td>
      <td width="78">8.68%</td>
      <td width="78"><br /></td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80">16.53%</td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">石油沥青</td>
      <td width="90"><br /></td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78">2.98%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">动力煤</td>
      <td width="90"><br /></td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78">12.13%</td>
      <td width="77"><br /></td>
      <td width="85"><br /></td>
      <td width="79" style="word-break: break-all;"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" colspan="2" style="" width="68">黄大豆一号</td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">11.01%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">玉米</td>
      <td width="90"><br /></td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">10.63%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">菜籽油</td>
      <td width="90"><br /></td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">4.75%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">鸡蛋</td>
      <td width="90"><br /></td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">4.45%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
     <tr height="19" style="height:19px">
      <td height="19" style="" width="38">玉米淀粉</td>
      <td width="90"><br /></td>
      <td width="87"><br /></td>
      <td width="78"><br /></td>
      <td width="78"><br /></td>
      <td width="77">2.63%</td>
      <td width="85"><br /></td>
      <td width="79"><br /></td>
      <td width="80"><br /></td>
     </tr>
    </tbody>
   </table>
  </div> 
 </body>
</html>
'''

class NHIndexAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_index_list(self):
        url = 'http://www.nanhua.net/ianalysis/plate-variety.json'
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'
        data = json.loads(response)
        df = pd.DataFrame(data)
        return df, ''

    def get_index_daily(self, index_code):
        url = 'http://www.nanhua.net/ianalysis/varietyindex/index/%s.json' % index_code
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'
        data = json.loads(response)
        df = pd.DataFrame(data)
        df.columns = ['date', 'close']
        df['date'] = df['date'].apply(lambda x : datetime.datetime.fromtimestamp(int(x)/1000))
        return df, ''

    def get_index_snapshot(self):
        url = 'http://www.nanhua.net/index/jsons/latestindex.json'
        response = self.do_request(url)
        if response is None:
            return None, '获取数据失败'
        data = json.loads(response)
        df = pd.DataFrame(data)
        df['lastUpdate'] = df['lastUpdate'].apply(lambda x : datetime.datetime.strptime(x, '%Y%m%d%H%M%S'))
        return df, ''

    def _convert_percent(self, text):
        text = text.strip()
        if len(text) == 0:
            return 0.0

        return float(float(text.strip('%')))/100

    def get_index_weight(self):
        soup = BeautifulSoup(index_weight_2018, "html5lib")
        divs = soup.find_all('div')
        table = divs[0].table
        rows = table.findAll('tr')

        head = []
        data = []
        for row in rows:
            cols = row.findAll('td')
            if len(cols) == 9:

                if cols[0].text == '品种名称':
                    for i in range(1, 9):
                        head.append(cols[i].text)
                    continue

                item = {}
                item["product"] = cols[0].text
                for i in range(1, 9):
                    item['weight' + str(i)] = self._convert_percent(cols[i].text)
                data.append(item)

        df = pd.DataFrame(data)
        df.set_index('product', inplace=True)
        df.columns = head

        return df, ''

