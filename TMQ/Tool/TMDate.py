import datetime
# import time
import math
import pandas as pd


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

# 获取所有天
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
# print(get_everyday('20160101','20170511'))


# 获取最所有日期中最早的或最晚
def get_early_and_late_date(date_list):
    # date_list = ['20181220', '20181221', '20181212', '20180103','20160202']
    date_list = [datetime.datetime.strptime(d, '%Y%m%d') for d in date_list]
    big_d = max(date_list).strftime('%Y%m%d')
    small_d = min(date_list).strftime('%Y%m%d')
    return [small_d, big_d]


# 将日期数据进行排序
def sort_date_list(date_list):
    # date_list = ['20181220', '20181221', '20181212', '20180103','20160202','2014']
    date_list = [datetime.datetime.strptime(d, '%Y%m%d') for d in date_list]
    date_list.sort()


# 获取最优切割日期
def incise_date_into_block(date_list, max_period):
    date_list = get_everyday('20010101', '20190101')
    # date_list = ['20181220', '20181221', '20181212', '20180103', '20180104', '20180105', '20180106', '20170105', '20190506','20190505', '20010103', '20190507', '20190508', '20190509', '20190510']
    date_list.sort(reverse=True)
    max_period = 24
    sd = [datetime.datetime.strptime(a, '%Y%m%d') for a in date_list]
    l = [[(s - datetime.timedelta(days=a)).strftime("%Y%m%d") for a in range(max_period)] for s in sd]
    date_df = pd.DataFrame(l)
    date_df = date_df[date_df.isin(date_list)]
    df = date_df
    # i记录每次取的索引值
    i = []
    while len(df.index) > len(i):
        i.append(df.index[len(i)])
        # 获取排名靠前日期块需要移除的所有日期列表，loc[i[-1]]代表上一次添加进记录索引的索引值
        block_index = i[-1]
        remove_list = df[range(1, max_period)].loc[block_index]
        # 移除不需要的日期块
        df = df.drop(index=df[df[0].isin(remove_list)].index)





index_list = df[range(1,5)].loc[1458]
df.drop(index=df[df[0].isin(index_list)].index)
df.index[1499]
df[range(1,5)].loc[1458]
    # date_df['happy'] = 1
    #
    # test_df = date_df.shift(1)
    # td = date_df.T








l = {'20180104', '20180106', '20180103', '20180105'}