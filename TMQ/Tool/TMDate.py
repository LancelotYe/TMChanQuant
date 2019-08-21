import datetime
# import time
import math


# 日期差
def minus_date(bigDate, smallDate):
    '''
    :param bigDate: YYYYMMDD
    :param smallDate: YYYYMMDD
    :return: Int
    '''
    d1 = datetime.datetime.strptime(bigDate, '%Y%m%d')
    d2 = datetime.datetime.strptime(smallDate, '%Y%m%d')
    delta = d1 - d2
    return delta.days

# 一共有几天
def get_days_in_all(start, end):
    '''
    :param start: YYYYMMDD
    :param end: YYYYMMDD
    :return: Int
    '''
    return minus_date(end, start) + 1

# 日期切片
def clip_days_to_parts(start, end, period):
    # 可以切成几片
    count = math.ceil(get_days_in_all(start, end)/period)
    list = []
    st = start
    for i in range(count):
        if i == count-1:
            list.append((st, end))
        else:
            list.append((st, date_add_days(st, period-1)))
            st = date_add_days(st, period)
    return list


def date_add_days(date, days):
    d1 = datetime.datetime.strptime(date, '%Y%m%d')
    d = d1 + datetime.timedelta(days=days)
    return d.strftime('%Y%m%d')


# start = '20180101'
# end = '20180114'
#
# list  = clip_days_to_parts(start, end, 5)


def get_everyday(begin_date,end_date):
    # 前闭后闭
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date,"%Y%m%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list
# print(getEveryDay('20160101','20170511'))
