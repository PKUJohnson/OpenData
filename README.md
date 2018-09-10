# OpenDataTools
开源的数据提取工具，专注在各类网站上爬取数据，并通过简单易用的API方式使用

![](https://github.com/PKUJohnson/OpenData/blob/master/image/logo.png)

## install

声明：本工具只支持 **python3**，请安装python3.6以上版本。没有支持python2的计划。

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


## qq群讨论

![](https://github.com/quantOS-org/quantOSUserGuide/blob/master/assets/quantos-qq.jpg?raw=true)
