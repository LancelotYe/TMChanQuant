# import os
# import tushare as ts
# import datetime
# import time
# import pymysql
import pandas as pd
import numpy as np

from TMQ.TMDataRepository.DR_TushareTool import TsTool
from TMQ.TMDataRepository.DR_MysqlTool import OmsMysqlTool,CheckTradeDateMysqlTool
from TMQ.Tool.TMSlider import percent
import TMQ.Tool.TMDate as tmdt
import TMQ.Tool.TMJson as tmjs

# 打开数据库连接


class dr_oms_pip():
    # 一根管道通一只股票数据流
    def __init__(self):
        # self.table_name = ''
        # 创建数据库连接工具对象
        # 连接数据库
        self.ms_tool = OmsMysqlTool()
        self.loop_num = 0
        self.total_loop_num = 5
        self.loop_date_list = []
        self.need_exist_df = pd.DataFrame()

    def pip_start(self, ts_code, start_date, end_date):
        # 创建股票table
        self.ms_tool.create_table(ts_code)
        # 数据检测
        # df = pd.DataFrame()
        df = self.monitor_oms_data(ts_code, start_date, end_date)
        # 断开连接
        self.ms_tool.disconnect_db()
        return df

    def monitor_oms_data(self, ts_code, start_date, end_date):
        # # （非首次循环 并且 数据为空） 或者 已经没有循环次数
        # if (len(self.loop_date_list) == 0 & self.loop_num > 0) | self.loop_num == loop_num:
        #     return self.ms_tool.get_oms_data_from_db(ts_code, start, end, True)
        # exist_trade_date_index是已经存在在数据库的数据
        exist_trade_date_index = self.ms_tool.get_exist_trade_date_index(ts_code, start_date, end_date)
        # 然后从tushare获取交易日开盘的交易日期
        if len(self.need_exist_df) == 0:
            trade_date_index_df = TsTool().ts_get_trade_date(start_date, end_date)
            # 清理未开盘的数据
            self.need_exist_df = trade_date_index_df[trade_date_index_df.is_open == 1]
            self.need_exist_df = trade_date_index_df
        trade_date_index_df = self.need_exist_df
        # 打印已完成数据
        complete_num = len(exist_trade_date_index)
        total_num = len(trade_date_index_df)
        f = round(complete_num / total_num, 4)
        percent(f)

        # 获取缺少的所有交易日期
        for i in range(len(exist_trade_date_index)):
            trade_date_index_df = trade_date_index_df[trade_date_index_df.cal_date != exist_trade_date_index[i]]

        # 得出缺少的日期列表
        lost_date_list = list(self.need_exist_df.cal_date)

        # 如果是第一次循环，给循环列表=缺少的日期列表
        if self.loop_num == 0:
            self.loop_date_list = lost_date_list

        # 循环逻辑
        # 还存在没有循环的日期
        if len(self.loop_date_list) > 0:
            # 缺损数据先从tushare获取数据
            new_start = self.loop_date_list[0]
            # if len(self.loop_date_list) > 15:
            #     # 拿倒数第15个交易日
            #     new_start = self.loop_date_list[-15]
            new_end = self.loop_date_list[-1]
            df = TsTool().ts_get_oms_price(ts_code, new_start, new_end)
            if len(df) > 0:
                # 获取的df是从大到小排的
                cut_start_date = df.iloc[len(df) - 1].trade_date
                # 获取得到的最小日期索引
                cut_start_date_index = self.loop_date_list.index(cut_start_date)
                # 最小日期索引后面的日期全部去除
                self.loop_date_list = self.loop_date_list[:cut_start_date_index]
                if self.ms_tool.insert_data(ts_code, df):
                    # 存入数据成功以后在回去鉴别数据
                    # 循环列表有数据， 并且循环次数<loop_num
                    if len(self.loop_date_list) > 0 & self.loop_num < self.total_loop_num + 1:
                        self.loop_num += 1
                        return self.monitor_oms_data(ts_code, start_date, end_date)
            else:
                print('接口可能出了问题,或者没有数据' + 'new_start= {}'.format(new_start) + '\nnew_end={}'.format(new_end))
        # # 只有最后一次循环都要列出缺少的日期
        # print('缺失的日期 = {}'.format(np.array(lost_date_list)))
        # 没有缺少数据，直接从数据库调用
        result_df = self.ms_tool.get_data_from_db(ts_code, start_date, end_date, True)
        return result_df




    # 获取ts_code在oms数据库中，start和end期间缺少的数据
    def get_lost_data_from_oms_db(self, start, end, ts_code):
        '''
        :param start: YYYYMMDD
        :param end: YYYYMMDD
        :param ts_code: str
        :return: list
        '''
        self.omsMysqlTool = OmsMysqlTool()
        self.omsMysqlTool.create_table(ts_code)
        has_data_day = self.omsMysqlTool.get_exist_trade_date_index(ts_code, start, end)
        everyday = tmdt.get_everyday(start, end)
        lost_day = list(set(everyday)-set(has_data_day))
        self.omsMysqlTool.disconnect_db()
        return lost_day

    # 获取1.数据库没有经过验证过需要验证的日期，2.交易日期数据，3.本地check数据库存在但是需要下载的数据
    def get_need_check_dates(self, lost_day, ts_code):
        # 数据库缺少日期
        check_dates = [d.strftime('%Y%m%d') for d in list(lost_day)]
        # 获取最长时间段
        se = tmdt.get_early_and_late_date(check_dates)
        # 缺少的最长时间段交易日期数据
        ts_trade_df = TsTool().ts_get_trade_date(se[0], se[1])
        # # 保存交易日期数据，等验证完数据以后，需要保存到数据库
        # self.ts_trade_df = ts_trade_df
        # 获取check_data数据库
        self.checkMysqlTool = CheckTradeDateMysqlTool()
        check_db_df = self.checkMysqlTool.get_data_from_db_by_date_list(ts_code, lost_day)
        ts_trade_df_dates = list(ts_trade_df.cal_date)
        check_db_df_dates = list(check_db_df.cal_date)
        # need_check_dates 是checks数据库没有验证过的数据
        self.need_check_dates = list(set(ts_trade_df_dates) - set(check_db_df_dates))

        # 需要验证的时间段的基础数据在ts_trade_df中,其中包含is_opne==0的数据
        self.basic_merge_trade_date_df = ts_trade_df[ts_trade_df['cal_date'].isin(self.need_check_dates)]
        self.basic_merge_trade_date_df['ts_code'] = ts_code

        # check_db_df中包含已经验证有数据的内容，这部分内容还有保存到oms数据库,需要添加到下载列表
        need_download_dates = list(check_db_df[check_db_df.has_data == 1].cal_date)
        # 本地check存在需要下载的数据
        self.need_download_dates = need_download_dates
        return (self.basic_merge_trade_date_df, self.need_check_dates, self.need_download_dates)

    # 加下去分两步，第一步下载不需要记录到checkDB的数据，第二步下载需要记录到checkDB的数据
    # 需要进行切片分块下载
    # 下载数据的顺序是新数据靠前下载
    # 下载期间用需要将need_check和need_download合并，并且排序
    #
    def step_repeat_download(self, ts_code, need_check_dates, need_download_dates):
        # new_download_list = tmdt.sort_date_list(need_check_dates + need_download_dates)
        new_download_list = need_check_dates + need_download_dates
        download_task_list = tmdt.incise_date_into_block(new_download_list, 25)
        tmjs.saveTasksJsonFile(ts_code, download_task_list)
        return download_task_list

    def start_download(self, ts_code, download_task_list, need_check_dates, basic_merge_trade_date_df, need_download_dates):
        need_donwload_count = len(download_task_list)
        # tushare账号只能使用五次一分钟
        for task in download_task_list:
            start = task[0]
            end = task[1]
            # step1
            df = TsTool().ts_get_oms_price(ts_code, start, end)
            # 筛选需要保存的数据
            need_save_df = df[df.trade_date.isin(need_check_dates+need_download_dates)]
            self.omsMysqlTool.insert_data(ts_code, need_save_df)
            # step2
            # 保存到checkDB的数据
            # all_dates = tmdt.get_everyday(start, end)
            download_data_days = need_save_df.drop_duplicates(subset='trade_date', keep='first').trade_date
            wait_for_check_days = list(set(download_data_days)-set(need_download_dates))
            basic_merge_trade_date_df['has_data'] = 0
            # basic_merge_trade_date_df.cal_date.isin(wait_for_check_days)
            basic_merge_trade_date_df.loc[basic_merge_trade_date_df.cal_date.isin(wait_for_check_days), 'has_data'] = 1
            # 保存到数据check数据库
            self.checkMysqlTool.insert_data(basic_merge_trade_date_df)
            # step3
            # json文件修改
            tmjs.finishTaskTellJsonFile(ts_code, task)



    def main_go(self):
        start = '20110103'
        end = '20190103'
        ts_code = '000001.SZ'
        lost_days = self.get_lost_data_from_oms_db(ts_code, start, end)
        task_tuple = self.get_need_check_dates(lost_days, ts_code)
        basic_merge_trade_date_df = task_tuple[0]
        need_check_dates = task_tuple[1]
        need_download_dates = task_tuple[2]

        download_task_list = self.step_repeat_download(ts_code, need_check_dates, need_download_dates)

        self.start_download(ts_code, download_task_list, need_check_dates, basic_merge_trade_date_df, need_download_dates)








#
# ts_code = '000001.SZ'
# lost_day = ['20181220','20181221','20181212','20180103']
# # test_day = ['20181220','20170101']
# import TMQ.TMDataRepository.DR_TushareTool as tst
# start = '20190101'
# end = '20190115'
# df = tst.ts_get_trade_date(start, end)
#
# tdf = df[df['cal_date'].isin(['20190103','20190105'])]
# # l = list(set(lost_day)-set(test_day))
#
# df = checkMysqlTool.get_data_from_db_by_date_list(ts_code, lost_day)
# check_dates = [d.strftime('%Y%m%d') for d in list(df.cal_date)]
# db_lost_day = list(set(lost_day)-set(check_dates))

# pip = dr_oms_pip()
# xx = pip.get_lost_data_from_oms_db(start, end ,ts_code)
#
# b= [1,2,3]
# a = [1,2,3,4,5,6]
# list(set(a)-set(b))
#
#
# c = a.remove(b)
#
#
# a = [2,4,0,8,9,10,100,0,9,7]
# a = list(filter(100, a))