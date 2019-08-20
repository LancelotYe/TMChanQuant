# import os
# import tushare as ts
# import datetime
# import time
# import pymysql
import pandas as pd
import numpy as np

import TMQ.TMDataRepository.DR_TushareTool as tst
from TMQ.TMDataRepository.DR_MysqlTool import OmsMysqlTool
from TMQ.Tool.TMSlider import percent

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
        start = start_date[0:4] + '-' + start_date[4:6] + '-' + start_date[6:8]
        end = end_date[0:4] + '-' + end_date[4:6] + '-' + end_date[6:8]
        # # （非首次循环 并且 数据为空） 或者 已经没有循环次数
        # if (len(self.loop_date_list) == 0 & self.loop_num > 0) | self.loop_num == loop_num:
        #     return self.ms_tool.get_oms_data_from_db(ts_code, start, end, True)
        # exist_trade_date_index是已经存在在数据库的数据
        exist_trade_date_index = self.ms_tool.get_exist_trade_date_index(ts_code, start, end)
        # 然后从tushare获取交易日开盘的交易日期
        if len(self.need_exist_df) == 0:
            trade_date_index_df = tst.ts_get_trade_date(start_date, end_date)
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
            df = tst.ts_get_oms_price(ts_code, new_start, new_end)
            # 获取的df是从大到小排的
            cut_start_date = df.iloc[len(df)-1].trade_date
            # 获取得到的最小日期索引
            cut_start_date_index = self.loop_date_list.index(cut_start_date)
            # 最小日期索引后面的日期全部去除
            self.loop_date_list = self.loop_date_list[:cut_start_date_index]

            if len(df) == 0:
                print('接口可能出了问题,或者没有数据'+'new_start= {}'.format(new_start)+'\nnew_end={}'.format(new_end))
            elif self.ms_tool.insert_data(ts_code, df):
                # 存入数据成功以后在回去鉴别数据
                # 循环列表有数据， 并且循环次数<loop_num
                if len(self.loop_date_list) > 0 & self.loop_num < self.total_loop_num+1:
                    self.loop_num += 1
                    return self.monitor_oms_data(ts_code, start_date, end_date)
        # 只有最后一次循环都要列出缺少的日期
        print('缺失的日期 = {}'.format(np.array(lost_date_list)))
        # 没有缺少数据，直接从数据库调用
        result_df = self.ms_tool.get_data_from_db(ts_code, start, end, True)
        return result_df


