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
    date_list = get_everyday('20010103','20090101')
    # date_list = ['20181220','20181221','20181212','20180103','20180104','20180105','20180106','20170105','20190506','20010103','20190507','20190508','20190509','20190510']
    date_list.sort(reverse=True)
    max_period = 25
    sd = [datetime.datetime.strptime(a, '%Y%m%d') for a in date_list]
    l = [[(s + datetime.timedelta(days=a)).strftime("%Y%m%d")for a in range(max_period)] for s in sd]
    date_df = pd.DataFrame(l)
    block_list = []
    # 连续日期最大排最前
    while(len(date_df) > 0):
        dl_list = [set(date_df.iloc[a]) & set(date_list) for a in range(len(date_df))]
        count_list = [len(a) for a in dl_list]
        index = count_list.index(max(count_list))
        collect = dl_list[index]
        date_list = list(set(date_list)-collect)
        collect = list(collect)
        collect.sort(reverse=True)
        block_list.append(collect)
        print(len(date_list))
        date_df = date_df[date_df[0].isin(date_list)]
    # 越晚排越前
    block_list.sort(reverse=True)




    # date_list = get_everyday('20010103', '20090101')
    date_list = ['20181220','20181221','20181212','20180103','20180104','20180105','20180106','20170105','20190506','20010103','20190507','20190508','20190509','20190510']
    date_list.sort(reverse=True)
    max_period = 5
    sd = [datetime.datetime.strptime(a, '%Y%m%d') for a in date_list]
    l = [[(s - datetime.timedelta(days=a)).strftime("%Y%m%d") for a in range(max_period)] for s in sd]
    date_df = pd.DataFrame(l)
    block_list = []
    # 连续日期最大排最前
    dl_list = [set(date_df.iloc[a]) & set(date_list) for a in range(len(date_df))]
    dl_list.sort(key=lambda dl_list:len(dl_list), reverse=True)
    li = dl_list.copy()
    newl = []
    i = 0
    while len(li) > 0:
        if len(newl) == 0:
            newl.append(li[0])
            li.remove(li[0])
        else:
            target = newl[-1]
            li_cp = li.copy()
            for a in li:
                print(len(li))
                if len(target & a) > 0:
                    li_cp.remove(a)
            li = li_cp
            if len(li_cp) > 0:
                newl.append(li_cp[0])










        count_list = [len(a) for a in dl_list]
        index = count_list.index(max(count_list))
        collect = dl_list[index]
        date_list = list(set(date_list) - collect)
        collect = list(collect)
        collect.sort(reverse=True)
        block_list.append(collect)
        print(len(date_list))
        date_df = date_df[date_df[0].isin(date_list)]
    # 越晚排越前
    block_list.sort(reverse=True)






    return block_list

    date_list = get_everyday('20010101', '20090101')
    # date_list = ['20181220', '20181221', '20181212', '20180103', '20180104', '20180105', '20180106', '20170105', '20190506','20190505', '20010103', '20190507', '20190508', '20190509', '20190510']
    date_list.sort(reverse=True)
    max_period = 5
    sd = [datetime.datetime.strptime(a, '%Y%m%d') for a in date_list]
    l = [[(s - datetime.timedelta(days=a)).strftime("%Y%m%d") for a in range(max_period)] for s in sd]
    date_df = pd.DataFrame(l)
    date_df = date_df[date_df.isin(date_list)]

    # for row in date_df.iterrows():
    #     print(row)
    # df = date_df

    # date_df[1:]
    # df = date_df[range(1,max_period)].loc[0]
    # df.loc[0]
    # while(len(date_df)>0):
    #     date_df.drop(index= date_df[date_df[0].isin(date_df.loc[0])].index)

    df = date_df
    i = [0]
    while len(set(df.index)-set(i)) > 0:
        # print(i[len(i)-1])
        # print(df.index[len(i)-1])

        index_list = df[range(1, max_period)].loc[i[-1]]
        df = df.drop(index=df[df[0].isin(index_list)].index)
        # print(df.index[len(i)])
        # print(df.index[len(i)])
        if len(df.index) != len(i):
            i.append(df.index[len(i)])
            # try:
            #     i.append(df.index[len(i)])
            # except Exception as e:
            #     print('error')




index_list = df[range(1,5)].loc[1458]
df.drop(index=df[df[0].isin(index_list)].index)
df.index[1499]
df[range(1,5)].loc[1458]
    # date_df['happy'] = 1
    #
    # test_df = date_df.shift(1)
    # td = date_df.T








l = {'20180104', '20180106', '20180103', '20180105'}