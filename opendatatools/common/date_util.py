#-*- coding:utf-8 -*-

import datetime
import calendar

lastday_map = {}

def get_current_day(format = "%Y-%m-%d"):
    curr_date = datetime.datetime.now()
    return datetime.datetime.strftime(curr_date, format)

def date_convert(date, format, target_format):
    return datetime.datetime.strftime(datetime.datetime.strptime(date, format), target_format)

def get_month_firstday_and_lastday(year=None, month=None):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 当月的第一天，datetime.date类型
              lastDay: 当月的最后一天，datetime.date类型
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    # 获取当月的第一天
    firstDay = datetime.date(year=year, month=month, day=1)
    lastDay = datetime.date(year=year, month=month, day=monthRange)

    return firstDay, lastDay

def get_month_lastday(datestr, format = "%Y-%m-%d"):
    
    if datestr in lastday_map:
        return lastday_map[datestr]
    
    date  = datetime.datetime.strptime(datestr, format)
    year  = date.year
    month = date.month
    firstDay, lastDay = get_month_firstday_and_lastday(year, month)
    result = datetime.datetime.strftime(lastDay, format)
    lastday_map[datestr] = result
    return result

def get_target_date(span, format="%Y-%m-%d"):
    today = datetime.date.today() 
    span_days = datetime.timedelta(days=span) 
    target = today + span_days  
    return datetime.datetime.strftime(target, format)

def split_date(datestr, format = "%Y-%m-%d"):
    date = datetime.datetime.strptime(datestr, format)
    return date.year, date.month, date.day

if __name__ == '__main__':
    print(get_target_date(0))
    print(get_target_date(10))
    print(get_target_date(-1))
    
    