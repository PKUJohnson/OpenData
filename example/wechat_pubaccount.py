
from opendatatools import wechat

if __name__ == "__main__":
    result = wechat.login("PKUJohnson@163.com", "密码")
    if result == True:
        df, msg = wechat.search_pub("饭桶戴老板")
        if df is not None:
            for index, row in df.iterrows():
                fakeid = row["fakeid"]
                total_msg_cnt = wechat.get_total_msg_count(fakeid)
                result = wechat.get_all_articles(fakeid, total_msg_cnt)
                print(result)


