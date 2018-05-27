# encoding: UTF-8
import urllib
import requests

class RestAgent():
    def __init__(self):
        # request header
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) " \
                     "AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/57.0.2987.133 Safari/537.36 "

        # simulate http request
        self.session = requests.Session()
        self.session.headers['User-Agent'] = self.user_agent

    def do_request(self, url, param):
        res = self.session.get(url, params=param)
        if res.status_code != 200:
            return None
        else:
            return res.text


