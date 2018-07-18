from .gaokao_agent import GaokaoAgent

gaokao_agent = GaokaoAgent()


def set_proxies(proxies):
    gaokao_agent.set_proxies(proxies)

def get_school_list(text):
    return gaokao_agent.get_school_list(text)

def get_school_baseinfo(school):
    return gaokao_agent.get_school_baseinfo(school)

def get_school_major(school):
    return gaokao_agent.get_school_major(school)

def get_school_score(school):
    return gaokao_agent.get_school_score(school)

def get_batch_score(province, subject):
    return gaokao_agent.get_batch_score(province, subject)
