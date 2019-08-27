import pandas as pd
import numpy as np

import TMQ.TMDataRepository.DR_TushareTool as tst
from TMQ.TMDataRepository.DR_MysqlTool import OmsMysqlTool,CheckTradeDateMysqlTool
from TMQ.Tool.TMSlider import percent
import TMQ.Tool.TMDate as tmdt
import TMQ.Tool.TMJson as tmjs
import TMQ.Tool.TMObserver as tmob


def main_go():
    start = '20110103'
    end = '20190103'
    ts_code = '000001.SZ'
    pip = Pip()
    lost_days = pip.get_lost_data_from_oms_db(ts_code, start, end)
    basic_merge_trade_date_df, need_check_dates, need_download_dates= pip.check_trade_dates(lost_days, ts_code)

    download_task_list = pip.step_repeat_download(ts_code, need_check_dates, need_download_dates)
    pip.start_download(ts_code, download_task_list, need_check_dates, basic_merge_trade_date_df, need_download_dates)


class Pip():
    def __init__(self):
        # self.table_name = ''
        # 创建数据库连接工具对象
        # 连接数据库
        self.omsMysqlTool = None
        self.checkMysqlTool = None
        # self.loop_num = 0
        # self.total_loop_num = 5
        # self.loop_date_list = []
        # self.need_exist_df = pd.DataFrame()







    def start_download(self, ts_code, download_task_list, need_check_dates, basic_merge_trade_date_df, need_download_dates):
        need_donwload_count = len(download_task_list)
        # tushare账号只能使用五次一分钟
        if need_donwload_count == 0:
            print('No Task')
            return
        for task in download_task_list:
            start = task[0]
            end = task[1]
            # step1
            df = tst.ts_get_oms_price(ts_code, start, end)
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



class PipTask():
    def __init__(self, start, end, ts_code):
        # self.table_name = ''
        # 创建数据库连接工具对象
        # 连接数据库
        # self.omsMysqlTool = None
        # self.checkMysqlTool = None
        lost_day = self.get_lost_data_from_oms_db(start, end, ts_code)
        a,b,c = self.check_trade_dates(lost_day, ts_code)
        get_download_task_list = self.get_download_task_list(ts_code, b, c)

    # 获取ts_code在oms数据库中，start和end期间缺少的数据
    def get_lost_data_from_oms_db(self, start, end, ts_code):
        # checked
        '''
        :param start: YYYYMMDD
        :param end: YYYYMMDD
        :param ts_code: str
        :return: list
        '''
        OmsMysqlTool().create_table(ts_code)
        has_data_day = OmsMysqlTool().get_exist_trade_date_index(ts_code, start, end)
        everyday = tmdt.get_everyday(start, end)
        lost_day = list(set(everyday) - set(has_data_day))
        OmsMysqlTool().disconnect_db()
        lost_day.sort()
        return lost_day

    # 获取1.数据库没有经过验证过需要验证的日期，2.交易日期数据，3.本地check数据库存在但是需要下载的数据
    def check_trade_dates(self, lost_day, ts_code):
        # 数据库缺少日期
        check_dates = lost_day
        # 获取最长时间段
        start, end = tmdt.get_early_and_late_date(check_dates)
        # 缺少的最长时间段交易日期数据
        ts_trade_df = tst.ts_get_trade_date(start, end)
        # # 保存交易日期数据，等验证完数据以后，需要保存到数据库
        # self.ts_trade_df = ts_trade_df
        # 获取check_data数据库
        # checkMysqlTool = CheckTradeDateMysqlTool()
        check_db_df = CheckTradeDateMysqlTool().get_data_from_db_by_date_list(ts_code, lost_day)
        CheckTradeDateMysqlTool().disconnect_db()

        ts_trade_df_dates = list(ts_trade_df.cal_date)
        check_db_df_dates = list(check_db_df.cal_date)

        # need_check_dates 是checks数据库没有验证过的数据
        need_check_dates = list(set(ts_trade_df_dates) - set(check_db_df_dates))
        # 需要验证的时间段的基础数据在ts_trade_df中,其中包含is_opne==0的数据
        basic_merge_trade_date_df = ts_trade_df[ts_trade_df['cal_date'].isin(need_check_dates)]
        basic_merge_trade_date_df['ts_code'] = ts_code

        # check_db_df中包含已经验证有数据的内容，这部分内容还有保存到oms数据库,需要添加到下载列表
        # 本地check存在需要下载的数据
        check_box_need_download_dates = list(check_db_df[check_db_df.has_data == 1].cal_date)
        return basic_merge_trade_date_df, need_check_dates, check_box_need_download_dates

    # 加下去分两步，第一步下载不需要记录到checkDB的数据，第二步下载需要记录到checkDB的数据
    # 需要进行切片分块下载
    # 下载数据的顺序是新数据靠前下载
    # 下载期间用需要将need_check和need_download合并，并且排序
    #
    def get_download_task_list(self, ts_code, need_check_dates, check_box_need_download_dates):
        # new_download_list = tmdt.sort_date_list(need_check_dates + need_download_dates)
        new_download_list = need_check_dates + check_box_need_download_dates
        download_task_list = tmdt.incise_date_into_block(new_download_list, 25)
        tmjs.saveTasksJsonFile(ts_code, download_task_list)
        return download_task_list


class PipControl(tmob.Publisher):
    def __init__(self):
        super(PipControl, self).__init__()
        self._listOfUsers = []
        self.postname = None

    def register(self, userObj):
        if userObj not in self._listOfUsers:
            self._listOfUsers.append(userObj)

    def unregister(self, userObj):
        self._listOfUsers.remove(userObj)

    def notifyAll(self):
        for objects in self._listOfUsers:
            objects.notify(self.postname)

    def writeNewPost(self , postname):
        self.postname = postname
        self.notifyAll()