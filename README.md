# OpenDataTools
开源的数据提取工具，专注在各类网站上爬取数据，并通过简单易用的API方式使用

![](https://github.com/PKUJohnson/OpenData/blob/master/image/logo.png)

## install

声明：本工具只支持 **** python3 ****，请安装python3.6以上版本。没有支持python2的计划。

1. 直接从pypi上安装：pip install opendatatools

![](https://github.com/PKUJohnson/OpenData/blob/master/image/install_pip.jpg)

2. 下载源代码，运行下面的命令：

python setup.py install

## 快速使用

本工具包括若干模块，基本使用方法如下：

1. 导入模块：from opendatatools import XXXXXX（XXXXXX代表模块名）

2. 调用模块方法： df, msg = XXXXXX.function(param)

3. 处理结果：df is None，代表失败，可以从msg中查看失败原因。

一个样例：

```python
from opendatatools import stock
df, msg = stock.get_quote('600000.SH,000002.SZ')
print(df)
```

## demo

please see [wiki](https://github.com/PKUJohnson/OpenData/wiki)

## Release Notes
+ 2018-07-03 : 0.4.7 add hsgt interface, remove hkex interface, add stock interface (股票接口增加资金流信息、沪深港通接口扩展)
+ 2018-06-24 : 0.4.3 add usstock interface, fix some bugs
+ 2018-06-22 : 0.3.8 add pledge and financial report data for stock, add shareholder structure for stock (增加股权质押，财务报表，股本数据)
+ 2018-06-21 : 0.3.7 add spot interface (黑色商品现货指标)
+ 2018-06-20 : 0.3.6 fix some bug for realestate Interface
+ 2018-06-20 : 0.3.5 add worldcup Interface（增加世界杯数据接口）
+ 2018-06-19 : 0.3.0 add fund Interface（增加开放式基金接口）
+ 2018-06-04 : 0.2.0 add real estate Interface（支持查询lianjia.com网站上的二手房销售信息（支持北京上海））
+ 2018-06-04 : 0.2.0 add economy Interface（支持中国宏观经济的各类指标）
+ 2018-05-31 : 0.1.3 add fx Interface（支持查询人民币汇率信息/Shibor隔夜利率信息）
+ 2018-05-31 : 0.1.3 add futures Interface（支持查询国内期货交易所的持仓交易排名信息）
+ 2018-05-30 : 0.1.2 update Stock Interface（增加支持中证指数，指数成份股，融资融券数据）
+ 2018-05-30 : 0.1.1 add Stock Interface（股票接口，目前支持获取沪深指数列表）
+ 2018-05-30 : 0.1.0 add Coin Interface（数字货币接口）
+ 2018-05-29 : 0.0.9 add HKEx Interface（港交所陆港通数据）
+ 2018-05-28 : 0.0.8 add AQI Interface （空气质量数据）

