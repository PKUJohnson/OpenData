# encoding: utf-8

from .movie_agent import MovieAgent

movie_agent = MovieAgent()

# 总票房排行
def get_boxoffice_rank():
    return movie_agent.get_boxoffice()

# 实时票房排名
def get_realtime_boxoffice():
    return movie_agent.get_realtime_boxoffice()

# 单日票房排行(近7日)
def get_recent_boxoffice(day):
    return movie_agent.get_recent_boxoffice(day)

# 单月票房统计
def get_monthly_boxoffice(date):
    return movie_agent.get_monthly_boxoffice(date)

# 年度票房统计
def get_yearly_boxoffice(year):
    return movie_agent.get_yearly_boxoffice(year)

