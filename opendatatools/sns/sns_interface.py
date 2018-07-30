# encoding: utf-8

from .weibo_agent import WeiboAgent

weibo_agent = WeiboAgent()

# 1hour, 1day, 1month, 3month
def get_weibo_index(word, type):
    return weibo_agent.get_weibo_index(word, type)
