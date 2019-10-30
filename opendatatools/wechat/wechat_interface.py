from .wechat_agent import *

agent = WechatMPAgent()


def login(mp_username, mp_password):
    return agent.login(mp_username, mp_password)

def search_pub(pubaccount):
    return agent.search_pub(pubaccount)

def get_total_msg_count(fakeid):
    msg_cnt, df = agent.get_article_list(fakeid, 0)
    return msg_cnt

def get_all_articles(fakeid, app_msg_cnt):
    count = 0
    df_list = []
    while count < app_msg_cnt:
        cnt, df = agent.get_article_list(fakeid, count)
        df_list.append(df)
        count = count + 5
        print(count)
        time.sleep(5)

    result = pd.concat(df_list)
    return result
