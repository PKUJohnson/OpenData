
from opendatatools import datayes

if __name__ == '__main__':
    datayes.set_proxies({"https" : "https://127.0.0.1:1080"})

    # 请到https://robo.datayes.com/注册帐号后填入此处
    df, msg = datayes.login('xxxx', 'xxxx')
    print(df, msg)

    top_items = datayes.get_top_items()
    print(top_items)

    sub_items, msg = datayes.get_sub_items("771263")
    print(sub_items, msg)

    sub_items, msg = datayes.get_sub_items("45678")
    print(sub_items, msg)

    sub_items, msg = datayes.get_sub_items("556622")
    print(sub_items, msg)

    sub_items, msg = datayes.get_sub_items("842126")
    print(sub_items, msg)

    sub_items, msg = datayes.get_sub_items("167420")
    print(sub_items, msg)

    df, inc, msg = datayes.get_series('1090000881')
    print(df)
    print(inc)
