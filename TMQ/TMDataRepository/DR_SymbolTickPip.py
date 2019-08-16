import os
import tushare as ts
import datetime
import time
import pymysql
import pandas as pd

# 打开数据库连接
# host = 'localhost'
# port = 3306
# user = 'root'
# password = '68466296aB'
# DB = 'DR_DataBase'
# symbol_id = '000001.SZ'
class dr_pip_open():
    # 一根管道通一只股票数据流
    def __init__(self, host, port, user, password, db_name, ts_code):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.ts_code = ts_code
        self.columns = ['ts_code','trade_time','open','high','low','close','vol','amount','trade_date','pre_close']
        # 连接数据库
        self.connection = self.connect_mysql_db()
        # 创建股票table
        self.create_symbol_table(ts_code)
        # 数据检测


        # 断开连接
        self.connection.close()

    def connect_mysql_db(self):
        #连接数据库
        connection = pymysql.connect(port=self.port,
                                     host=self.host,
                                     user=self.user,
                                     password=self.password,
                                     # db='demo',
                                     charset='utf8')
        cursor = connection.cursor()
        sql_create_db_cmd = 'CREATE DATABASE IF NOT EXISTS {};'.format(self.db_name)
        sql_use_db = 'USE {};'.format(self.db_name)
        try:
            cursor.execute(sql_create_db_cmd)
            cursor.execute(sql_use_db)
        except Exception as msg:
            print(msg)
        return  connection
        # connection.close()

    def create_symbol_table(self, ts_code):
        # 创建Table
        table_name = self.trans_ts_code_to_table_name(ts_code)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self.connection.cursor()
        element = '''
            {} varchar(255) NOT NULL,
            {} datetime NOT NULL,
            {} decimal(19,4) NULL,
            {} decimal(19,4) NULL,
            {} decimal(19,4) NULL,
            {} decimal(19,4) NULL,
            {} bigint NULL,
            {} bigint NULL,
            {} varchar(255) NOT NULL,
            {} decimal(19,4) NULL,
            PRIMARY KEY (trade_time),
            KEY index_ts_code (ts_code)
        '''.format(*self.columns)
        sql_create_table_cmd ='CREATE TABLE IF NOT EXISTS {} ({}) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8MB4;'.format(table_name, element)

        try:
            cursor.execute(sql_create_table_cmd)
        except Exception as msg:
            print(msg)
        # self.connection.close()
    def monitor_db_data(self, ts_code, start_date, end_date):
        table_name = self.trans_ts_code_to_table_name(ts_code)
        start = start_date[0:4] + '-' + start_date[4:6] + '-' + start_date[6:8]
        end = end_date[0:4] + '-' + end_date[4:6] + '-' + end_date[6:8]
        select = 'SELECT DISTINCT trade_date FROM {} WHERE trade_time>{} and trade_time<{} ORDER BY trade_time  ASC;'.format(table_name, start, end)
        cursor = self.connection.cursor()
        result = []
        try:
            result = cursor.execute(select)
        except Exception as msg:
            print(msg)

        a = ['20180102','20180104']

        res = zip(x for x in a)
        for i in res:
            print(i)
            df = df[df.cal_date!=i]
        df[df == a[0]]
        df[df.is_open == 1]

    def get_price_from_ts(self, ts_code, start_date, end_date):
        #get tick data from tushare
        '''
        :param ts_code: symbol 000000.SZ
        :param start_date: YYYYMMDD
        :param end_date: YYYYMMDD
        :return: df
        '''
        df1 = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, asset='E', freq='1min')
        return df1

    def get_price_from_db(self, ts_code, start_date, end_date):
        #get tick data from database
        '''
        :param ts_code: symbol 000000.SZ
        :param start_date: YYYYMMDD
        :param end_date: YYYYMMDD
        :return: df
        '''
        ts_code = '000001.SZ'
        arr = ts_code.split('.')
        if len(arr) != 2:
            print('Ts_code Type Error')
            return
        table_name = arr[1]+arr[0]
        self.create_code_table(table_name)


    def trans_ts_code_to_table_name(self, ts_code):
        arr = ts_code.split('.')
        if len(arr) != 2:
            print('Ts_code Type Error')
            return
        table_name = arr[1] + arr[0]
        return table_name


    def read_symbol_data(self, table_name, start_date, end_date):
        start = start_date[0:4]+'-'+start_date[4:6]+'-'+start_date[6:8]
        end = end_date[0:4]+'-'+end_date[4:6]+'-'+end_date[6:8]
        select = 'SELECT * FROM {} WHERE trade_time>{} and trade_time<{} ORDER BY trade_time  ASC;'.format(table_name, start, end)

    def insert_data(self, ts_code, start_date, end_date):
        host = 'localhost'
        port = 3306
        user = 'root'
        password = '68466296aB'
        DB = 'DR_DataBase'
        table_name = 'TT'

        df1 = self.get_price_from_ts(ts_code, start_date, end_date)
        print(df1)
        # 将colume的df转换datetime
        # df = df1.head(5)
        # dd = pd.to_datetime(df['trade_time'])
        # dd1 = pd.to_datetime(df['trade_date'])
        # dt = pd.DatetimeIndex(df['trade_time'])
        # dh = df['trade_time']
        # d = df1.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

        # a = df1.iloc[1].trade_date
        # a = df1.trade_date

        # b = df1['trade_date'].slice(start=0, step=4)
        # df = df1.head(2)

        if len(df1) == 0:
            print('No Data')
            return;
        df = df1.fillna(999999)
        # df = df.astype(object).where(pd.notnull(df), None)

        res = zip(df[a] for a in self.columns)
        columns = ['ts_code', 'trade_time', 'open', 'high', 'low', 'close', 'vol', 'amount', 'trade_date', 'pre_close']
        res = zip(df[a] for a in columns)
        table_name = 'tes'
        res = zip(df['ts_code'], df['trade_time'], df['open'], df['high'], df['low'], df['close'], df['vol'],df['amount'], df['trade_date'], df['pre_close'])

        sql = 'INSERT IGNORE INTO {} VALUES '.format(table_name)
        for i in res:
            sql = sql + '{}'.format(i) + ','
        sql = sql.strip(',')

        # connection = pymysql.connect(port=port,
        #                              host=host,
        #                              user=user,
        #                              password=password,
        #                              db=DB,
        #                              charset='utf8')

        # 使用 cursor() 方法创建一个游标对象 cursor
        # 创建DB和Table
        cursor = self.connection.cursor()

        cursor.execute(sql)
        self.connection.commit()
        # try:
        #     cursor.execute(sql)
        # except Exception as msg:
        #     print(msg)
        cursor.close()
        # connection.close()






def connect_MySQL():
    # 打开数据库连接
    host = 'localhost'
    port = 3306
    user = 'root'
    password = '68466296aB'
    DB = 'DR_DataBase'
    table_name = 'TT'
    symbol_id = '000001.SZ'
    # create_database_table(host, port, user, password)
    # df = get_1min_price(symbol_id=symbol_id, start = '20180701', end = '20180718')
    connection = pymysql.connect(port=port,
                                 host=host,
                                 user=user,
                                 password=password,
                                 # db='demo',
                                 charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    # 创建DB和Table
    cursor = connection.cursor()
    sql_createDB_cmd = 'CREATE DATABASE IF NOT EXISTS DR_DataBase;'
    sql_use_DB =  'USE DR_DataBase;'
    sql_createTable_cmd = '''
        CREATE TABLE IF NOT EXISTS {} (
              ts_code varchar(255) NOT NULL,
              trade_time datetime NOT NULL,
              open_price decimal(19,4) NULL,
              high_price decimal(19,4) NULL,
              low_price decimal(19,4) NULL,
              close_price decimal(19,4) NULL,
              volume bigint NULL,
              amount bigint NULL,
              trade_date varchar(255) NOT NULL,
              pre_close_price decimal(19,4) NULL,
              PRIMARY KEY (trade_time),
              KEY index_ts_code (ts_code)
            ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8MB4;
        '''.format(table_name)

    try:
        cursor.execute(sql_createDB_cmd)
        cursor.execute(sql_use_DB)
        cursor.execute(sql_createTable_cmd)
    except Exception as msg:
        print(msg)
    connection.close()
    # insertData()

def get_price_df(ts_code, start_date, end_date):
    df1 = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, asset='E', freq='1min')
    return df1

def insertData(ts_code, start_date, end_date):
    host = 'localhost'
    port = 3306
    user = 'root'
    password = '68466296aB'
    DB = 'DR_DataBase'
    table_name = 'TT'

    df1 = get_price_df(ts_code, start_date, end_date)
    print(df1)
    # 将colume的df转换datetime
    # df = df1.head(5)
    # dd = pd.to_datetime(df['trade_time'])
    # dd1 = pd.to_datetime(df['trade_date'])
    # dt = pd.DatetimeIndex(df['trade_time'])
    # dh = df['trade_time']
    # d = df1.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    # a = df1.iloc[1].trade_date
    # a = df1.trade_date

    # b = df1['trade_date'].slice(start=0, step=4)
    # df = df1.head(2)

    if len(df1)==0:
        print('No Data')
        return;
    df = df1.fillna(999999)
    # df = df.astype(object).where(pd.notnull(df), None)

    res = zip(df['ts_code'], df['trade_time'], df['open'],df['high'],df['low'],df['close'],df['vol'],df['amount'],df['trade_date'],df['pre_close'])



    sql = 'INSERT IGNORE INTO {} VALUES '.format(table_name)
    for i in res:
        sql = sql+'{}'.format(i)+','
    sql = sql.strip(',')

    connection = pymysql.connect(port=port,
                                 host=host,
                                 user=user,
                                 password=password,
                                 db=DB,
                                 charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    # 创建DB和Table
    cursor = connection.cursor()

    cursor.execute(sql)
    connection.commit()
    # try:
    #     cursor.execute(sql)
    # except Exception as msg:
    #     print(msg)
    cursor.close()
    connection.close()



def get_tick_from_pip(ts_code, start_date, end_date):
    # df =

# connect_MySQL()
# insertData(ts_code='000001.SZ', start_date='20120301', end_date='20120304')

# dfx = get_price_df(ts_code='000001.SZ', start_date='20130111', end_date='20130112')
# import os
#
# path = os.path.join(os.getcwd(),'QuantData','testDF.csv')
# df.to_csv(path)