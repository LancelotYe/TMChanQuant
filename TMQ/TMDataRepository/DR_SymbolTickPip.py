# import os
# import tushare as ts
# import datetime
# import time
# import pymysql
import pandas as pd
import numpy as np
import TMQ.TMDataRepository.DR_Config as drc
import TMQ.TMDataRepository.DR_TushareTool as tst
from TMQ.TMDataRepository.DR_MysqlTool import dr_mysql_tool
from TMQ.Tool.TMSlider import percent

# 打开数据库连接


class dr_oms_pip():
    # 一根管道通一只股票数据流
    def __init__(self):
        conf_dict = drc.get_mysql_config_dict()
        # self.table_name = ''
        # 创建数据库连接工具对象
        # 连接数据库
        self.ms_tool = dr_mysql_tool(conf_dict)

    def pip_start(self, ts_code, start_date, end_date):
        # self.table_name = self.ms_tool.trans_oms_ts_code_to_table_name(ts_code)
        # 创建股票table
        self.ms_tool.create_oms_table(ts_code)
        # 数据检测
        df = pd.DataFrame()
        df = self.monitor_oms_data(ts_code, start_date, end_date)
        # 断开连接
        self.ms_tool.disconnect_mysql()
        return df

    def monitor_oms_data(self, ts_code, start_date, end_date):
        start = start_date[0:4] + '-' + start_date[4:6] + '-' + start_date[6:8]
        end = end_date[0:4] + '-' + end_date[4:6] + '-' + end_date[6:8]
        result = self.ms_tool.get_oms_exist_trade_date_index(ts_code, start, end)
        # result是已经存在在数据库的数据，然后从tushare获取交易日开盘的交易日期
        trade_date_df = tst.ts_get_trade_date(start_date, end_date)
        # 数据处理
        # 清理未开盘的数据
        trade_date_df = trade_date_df[trade_date_df.is_open == 1]
        # 打印已完成数据
        complete_num = len(result)
        total_num = len(trade_date_df)
        f = round(complete_num / total_num, 4)
        percent(f)
        # 获取缺少的所有交易日期
        for i in range(len(result)):
            trade_date_df = trade_date_df[trade_date_df.cal_date!=result[i]]
        lost_dates = list(trade_date_df.cal_date)

        # 循环逻辑
        result_df = pd.DataFrame()
        if len(lost_dates)>0:
            # 缺损的数据大于1，就要先从tushare获取数据
            print('缺失的日期 = {}'.format(np.array(lost_dates)))
            new_start = lost_dates[0]
            if len(lost_dates) > 15:
                # 拿倒数第15个交易日
                new_start = lost_dates[-15]
            new_end = lost_dates[-1]
            df = tst.ts_get_oms_price(ts_code, new_start, new_end)
            if len(df) == 0:
                print('接口可能出了问题,或者没有数据'+'new_start= {}'.format(new_start)+'\nnew_end={}'.format(new_end))
                result_df = self.ms_tool.get_oms_data_from_db(ts_code, start, end, True)
                return result_df
            if self.ms_tool.insert_oms_data(ts_code ,df):
                # 存入数据成功以后在回去鉴别数据
                self.monitor_oms_data(ts_code, start_date, end_date)
            else:
                print('数据库错误')
                result_df = self.ms_tool.get_oms_data_from_db(ts_code, start, end, True)
        else:
            # 没有缺少数据，直接从数据库调用
            result_df = self.ms_tool.get_oms_data_from_db(ts_code, start, end, True)
        return result_df


    # df[df == a[0]]
    # df[df.is_open == 1]
    # def get_price_from_db(self, start, end):
    #     #get tick data from database
    #     '''
    #     :param start_date: YYYY-MM-DD
    #     :param end_date: YYYY-MM-DD
    #     :return: df
    #     '''
    #     select = 'SELECT * FROM {} WHERE trade_time>\'{}\' and trade_time<\'{}\' ORDER BY trade_time ASC;'.format(self.table_name,start, end)
    #     # result = ['20130102', '20130104']
    #     # start = '2013-01-02'
    #     # end = '2013-01-08'
    #     # select = 'SELECT * FROM {} WHERE trade_time>\'{}\' and trade_time<\'{}\' ORDER BY trade_time ASC;'.format(
    #     #     table_name,
    #     #     start, end)
    #     cursor = self.connection.cursor()
    #     # 使用 cursor() 方法创建一个游标对象 cursor
    #     # 创建DB和Table
    #     df = []
    #     try:
    #         cursor.execute(select)
    #         result = cursor.fetchall()
    #         df = pd.DataFrame(list(result))
    #     except Exception as msg:
    #         print(msg)
    #     return df


    # def create_symbol_table(self):
    #     # # 创建Table
    #     cursor = self.connection.cursor()
    #     element = '''
    #         {} varchar(255) NOT NULL,
    #         {} datetime NOT NULL,
    #         {} decimal(19,4) NULL,
    #         {} decimal(19,4) NULL,
    #         {} decimal(19,4) NULL,
    #         {} decimal(19,4) NULL,
    #         {} bigint NULL,
    #         {} bigint NULL,
    #         {} varchar(255) NOT NULL,
    #         {} decimal(19,4) NULL,
    #         PRIMARY KEY (trade_time),
    #         KEY index_ts_code (ts_code)
    #     '''.format(*self.columns)
    #     sql_create_table_cmd ='CREATE TABLE IF NOT EXISTS {} ({}) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8MB4;'.format(self.table_name, element)
    #     try:
    #         cursor.execute(sql_create_table_cmd)
    #     except Exception as msg:
    #         print(msg)
    #     # self.connection.close()



    # def insert_data(self, df):
    #     if len(df) == 0:
    #         print('No Data')
    #         return;
    #     df = df.fillna(999999)
    #
    #     res = zip(*(df[a] for a in self.columns))
    #     table_name = 'tes'
    #     # res = zip(*[df['ts_code'], df['trade_time'], df['open'], df['high'], df['low'], df['close'], df['vol'], df['amount'], df['trade_date'], df['pre_close']])
    #     sql = 'INSERT IGNORE INTO {} VALUES '.format(table_name)
    #     for i in res:
    #         sql = sql + '{}'.format(i) + ','
    #     sql = sql.strip(',')
    #     cursor = self.connection.cursor()
    #     try:
    #         cursor.execute(sql)
    #         self.connection.commit()
    #     except Exception as msg:
    #         print(msg)
    #         return False
    #     cursor.close()
    #     return True
    #     # connection.close()
    # def read_symbol_data(self, table_name, start_date, end_date):
    #     start = start_date[0:4]+'-'+start_date[4:6]+'-'+start_date[6:8]
    #     end = end_date[0:4]+'-'+end_date[4:6]+'-'+end_date[6:8]
    #     select = 'SELECT * FROM {} WHERE trade_time>{} and trade_time<{} ORDER BY trade_time  ASC;'.format(table_name, start, end)








# def connect_MySQL():
#     # 打开数据库连接
#     host = 'localhost'
#     port = 3306
#     user = 'root'
#     password = '68466296aB'
#     DB = 'DR_DataBase'
#     table_name = 'TT'
#     symbol_id = '000001.SZ'
#     # create_database_table(host, port, user, password)
#     # df = get_1min_price(symbol_id=symbol_id, start = '20180701', end = '20180718')
#     connection = pymysql.connect(port=port,
#                                  host=host,
#                                  user=user,
#                                  password=password,
#                                  # db='demo',
#                                  charset='utf8')
#     # 使用 cursor() 方法创建一个游标对象 cursor
#     # 创建DB和Table
#     cursor = connection.cursor()
#     sql_createDB_cmd = 'CREATE DATABASE IF NOT EXISTS DR_DataBase;'
#     sql_use_DB =  'USE DR_DataBase;'
#     sql_createTable_cmd = '''
#         CREATE TABLE IF NOT EXISTS {} (
#               ts_code varchar(255) NOT NULL,
#               trade_time datetime NOT NULL,
#               open_price decimal(19,4) NULL,
#               high_price decimal(19,4) NULL,
#               low_price decimal(19,4) NULL,
#               close_price decimal(19,4) NULL,
#               volume bigint NULL,
#               amount bigint NULL,
#               trade_date varchar(255) NOT NULL,
#               pre_close_price decimal(19,4) NULL,
#               PRIMARY KEY (trade_time),
#               KEY index_ts_code (ts_code)
#             ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8MB4;
#         '''.format(table_name)
#
#     try:
#         cursor.execute(sql_createDB_cmd)
#         cursor.execute(sql_use_DB)
#         cursor.execute(sql_createTable_cmd)
#     except Exception as msg:
#         print(msg)
#     connection.close()
#     # insertData()
#
# def get_price_df(ts_code, start_date, end_date):
#     df1 = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, asset='E', freq='1min')
#     return df1
#
# def insertData(ts_code, start_date, end_date):
#     host = 'localhost'
#     port = 3306
#     user = 'root'
#     password = '68466296aB'
#     DB = 'DR_DataBase'
#     table_name = 'TT'
#
#     df1 = get_price_df(ts_code, start_date, end_date)
#     print(df1)
#     # 将colume的df转换datetime
#     # df = df1.head(5)
#     # dd = pd.to_datetime(df['trade_time'])
#     # dd1 = pd.to_datetime(df['trade_date'])
#     # dt = pd.DatetimeIndex(df['trade_time'])
#     # dh = df['trade_time']
#     # d = df1.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
#
#     # a = df1.iloc[1].trade_date
#     # a = df1.trade_date
#
#     # b = df1['trade_date'].slice(start=0, step=4)
#     # df = df1.head(2)
#
#     if len(df1)==0:
#         print('No Data')
#         return;
#     df = df1.fillna(999999)
#     # df = df.astype(object).where(pd.notnull(df), None)
#
#     res = zip(df['ts_code'], df['trade_time'], df['open'],df['high'],df['low'],df['close'],df['vol'],df['amount'],df['trade_date'],df['pre_close'])
#
#
#
#     sql = 'INSERT IGNORE INTO {} VALUES '.format(table_name)
#     for i in res:
#         sql = sql+'{}'.format(i)+','
#     sql = sql.strip(',')
#
#     connection = pymysql.connect(port=port,
#                                  host=host,
#                                  user=user,
#                                  password=password,
#                                  db=DB,
#                                  charset='utf8')
#     # 使用 cursor() 方法创建一个游标对象 cursor
#     # 创建DB和Table
#     cursor = connection.cursor()
#
#     cursor.execute(sql)
#     connection.commit()
#     # try:
#     #     cursor.execute(sql)
#     # except Exception as msg:
#     #     print(msg)
#     cursor.close()
#     connection.close()
#
# def insert_data(self, ts_code, start_date, end_date):
#     host = 'localhost'
#     port = 3306
#     user = 'root'
#     password = '68466296aB'
#     DB = 'DR_DataBase'
#     table_name = 'TT'
#
#     df1 = self.get_price_from_ts(ts_code, start_date, end_date)
#     print(df1)
#     # 将colume的df转换datetime
#     # df = df1.head(5)
#     # dd = pd.to_datetime(df['trade_time'])
#     # dd1 = pd.to_datetime(df['trade_date'])
#     # dt = pd.DatetimeIndex(df['trade_time'])
#     # dh = df['trade_time']
#     # d = df1.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
#
#     # a = df1.iloc[1].trade_date
#     # a = df1.trade_date
#
#     # b = df1['trade_date'].slice(start=0, step=4)
#     # df = df1.head(2)
#
#
#
#
#
#
#
#     if len(df1) == 0:
#         print('No Data')
#         return;
#     df = df1.fillna(999999)
#     # df = df.astype(object).where(pd.notnull(df), None)
#
#     res = zip(df[a] for a in self.columns)
#     columns = ['ts_code', 'trade_time', 'open', 'high', 'low', 'close', 'vol', 'amount', 'trade_date', 'pre_close']
#     res = zip(df[a] for a in columns)
#     table_name = 'tes'
#     res = zip(df['ts_code'], df['trade_time'], df['open'], df['high'], df['low'], df['close'], df['vol'],
#               df['amount'], df['trade_date'], df['pre_close'])
#
#     sql = 'INSERT IGNORE INTO {} VALUES '.format(table_name)
#     for i in res:
#         sql = sql + '{}'.format(i) + ','
#     sql = sql.strip(',')
#
#     # connection = pymysql.connect(port=port,
#     #                              host=host,
#     #                              user=user,
#     #                              password=password,
#     #                              db=DB,
#     #                              charset='utf8')
#
#     # 使用 cursor() 方法创建一个游标对象 cursor
#     # 创建DB和Table
#     cursor = self.connection.cursor()
#
#     cursor.execute(sql)
#     self.connection.commit()
#     # try:
#     #     cursor.execute(sql)
#     # except Exception as msg:
#     #     print(msg)
#     cursor.close()
#     # connection.close()
#
# def get_tick_from_pip(ts_code, start_date, end_date):
#     # df =
#
# # connect_MySQL()
# # insertData(ts_code='000001.SZ', start_date='20120301', end_date='20120304')
#
# # dfx = get_price_df(ts_code='000001.SZ', start_date='20130111', end_date='20130112')
# # import os
# #
# # path = os.path.join(os.getcwd(),'QuantData','testDF.csv')
# # df.to_csv(path)