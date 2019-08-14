#  数据传输管道
import os
import tushare as ts
import datetime
import time
import pymysql
import sqlalchemy
import pandas as pd


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
        CREATE TABLE {} (
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



def insertData():
    host = 'localhost'
    port = 3306
    user = 'root'
    password = '68466296aB'
    DB = 'DR_DataBase'
    table_name = 'TT'
    connection = pymysql.connect(port=port,
                                 host=host,
                                 user=user,
                                 password=password,
                                 db=DB,
                                 charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    # 创建DB和Table
    cursor = connection.cursor()
    df1 = ts.pro_bar(ts_code='000001.SZ', start_date='20130103', end_date='20130105', asset='E', freq='1min')
    # 将colume的df转换datetime
    df = df1.head(5)
    dd = pd.to_datetime(df['trade_time'])
    dd1 = pd.to_datetime(df['trade_date'])
    dt = pd.DatetimeIndex(df['trade_time'])
    dh = df['trade_time']
    d = df1.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    a = df1.iloc[1].trade_date
    a = df1.trade_date

    b = df1['trade_date'].slice(start=0, step=4)

    res = zip(df['ts_code'], dh, df['open'],df['high'],df['low'],df['close'],df['vol'],df['amount'],dd1,df['pre_close'])
    sql = 'INSERT INTO {} (ts_code, trade_time, open_price, high_price, low_price, close_price, volume, amount, trade_date, pre_close_price) VALUES '.format(table_name)
    for i in res:
        sql = sql+'{}'.format(i)+','
    sql = sql.strip(',')
    try:
        cursor.execute(sql)
    except Exception as msg:
        print(msg)
    connection.close()





connect_MySQL()
insertData()



def string_toDatetime(st):
    # 把字符串转成datetime
    print(datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S"))
    return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")
def string_toTimestamp(st):
    # 把字符串转成时间戳形式
    print("3.把字符串转成时间戳形式:", time.mktime(time.strptime(st, "%Y-%m-%d %H:%M:%S")))
    return time.mktime(time.strptime(st, "%Y-%m-%d %H:%M:%S"))
















def get_1min_price(symbol_id, start, end):
    pro = ts.pro_api()
    # 日线数据
    # df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
    df = pro.daily(ts_code=symbol_id, start_date=start, end_date=end)
    return df




def read_from_db():
    host = 'localhost'
    port = 3306
    user = 'root'
    password = '68466296aB'
    DB = 'DR_DataBase'
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(user, password, host, port, DB))

    with engine.connect() as con, con.begin():
        df = pd.read_sql_table(
            'test_table',con
        )



def create_database_table(host, port, user, password):
    connection = pymysql.connect(port=port,
                                 host=host,
                                 user=user,
                                 password=password,
                                 # db='demo',
                                 charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = connection.cursor()
    sqlFileName = get_sql_files()
    # execute_scripts_from_file(sqlFileName, cursor)

    sql_createDB_cmd = 'CREATE DATABASE IF NOT EXISTS DR_DataBase'
    str = 'table_name'
    sql_createTable_cmd ='''
    CREATE TABLE {} (
          id int NOT NULL AUTO_INCREMENT,
          ts_code int NOT NULL,
          trade_time datetime NOT NULL,
          open_price decimal(19,4) NULL,
          high_price decimal(19,4) NULL,
          low_price decimal(19,4) NULL,
          close_price decimal(19,4) NULL,
          volume bigint NULL,
          amount bigint NULL,
          trade_date datetime NOT NULL,
          pre_close_price decimal(19,4) NULL,
          PRIMARY KEY (id),
          KEY index_ts_code (ts_code)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
    '''.format(str)

    '''
    CREATE TABLE testTB (
          id int NOT NULL AUTO_INCREMENT,
          ts_code int NOT NULL,
          trade_time datetime NOT NULL,
          open_price decimal(19,4) NULL,
          high_price decimal(19,4) NULL,
          low_price decimal(19,4) NULL,
          close_price decimal(19,4) NULL,
          volume bigint NULL,
          amount bigint NULL,
          trade_date datetime NOT NULL,
          pre_close_price decimal(19,4) NULL,
          PRIMARY KEY (id),
          KEY index_ts_code (ts_code)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
    '''
    try:
        cursor.execute(sql_createDB_cmd)
        cursor.execute(sql_createTable_cmd)
    except Exception as msg:
        print(msg)
    connection.close()


def execute_scripts_from_file(filename, cursor):
    sql_cmd = 'CREATE DR_DataBase IF NOT EXISTS DR_DataBase'
    try:
        cursor.execute(sql_cmd)
    except Exception as msg:
        print(msg)

    # fd = open(filename, 'r', encoding='utf-8')
    # sqlFile = fd.read()
    # fd.close()
    # sqlCommands = sqlFile.split(';')
    # for command in sqlCommands:
    #     try:
    #         cursor.execute(command)
    #     except Exception as msg:
    #         print(msg)
    # print('sql执行完成')


def rush_pipe_to_db(df, table_name):
    # name: 输出的表名
    # con: 与read_sql中相同，数据库链接
    # if_exits： 三个模式：fail，若表存在，则不输出；replace：若表存在，覆盖原来表里的数据；append：若表存在，将数据写到原表的后面。默认为fail
    # index：是否将df的index单独写到一列中
    # index_label: 指定列作为df的index输出，此时index为True
    # chunksize： 同read_sql
    # dtype: 指定列的输出到数据库中的数据类型。字典形式储存：{
    # column_name: sql_dtype}。常见的数据类型有sqlalchemy.types.INTEGER(), sqlalchemy.types.NVARCHAR(), sqlalchemy.Datetime()
    host = 'localhost'
    port = 3306
    user = 'root'
    password = '68466296aB'
    DB = 'DR_DataBase'
    connection = sqlalchemy.create_engine(
        "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(user, password, host, port, DB))
    df.to_sql(
        name = table_name,
        con = connection,
        if_exists = 'append',
        index = False,
        dtype = {
            'trade_time':sqlalchemy.DateTime,
            'open':sqlalchemy.types.FLOAT(),
            'high':sqlalchemy.types.FLOAT(),
            'low':sqlalchemy.types.FLOAT(),
            'close':sqlalchemy.types.FLOAT(),
            'vol':sqlalchemy.types.INTEGER(),
            'amount':sqlalchemy.types.INTEGER(),
            'trade_date':sqlalchemy.types.INTEGER(),
            'pre_close':sqlalchemy.types.FLOAT()
        }
    )





def get_sql_files():
    sqlFileName = 'DBScript.sql'
    sqlFileName = os.path.join(os.getcwd(), 'TMQ', 'TMDataRepository', sqlFileName)
    return  sqlFileName

    # sql_files = []
    # files = os.listdir(os.path.dirname(os.path.abspath(__file__)))
    # for file in files:
    #     if os.path.splitext(file)[1] == '.sql':
    #         sql_files.append(file)
    # return sql_files



# now = datetime.datetime.now()
#
# if __name__ == "__main__":
#     connect_MySQL()
#
#
# from sqlalchemy.types import Integer,NVARCHAR,Float
# from datetime import datetime
# import pandas as pd
#
# def mapping_df_types(df):
#     dtypedict = {}
#     for i, j in zip(df.columns, df.dtypes):
#         if "object" in str(j):
#             dtypedict.update({i: NVARCHAR(length=255)})
#         if "float" in str(j):
#             dtypedict.update({i: Float(precision=2, asdecimal=True)})
#         if "int" in str(j):
#             dtypedict.update({i: Integer()})
#     return dtypedict
#
#
#
# df = pd.DataFrame([['a', 1, 2.0, datetime.now(), True]],columns=['str', 'int', 'float', 'datetime', 'boolean'])
# dtypedict = mapping_df_types(df)
# df.to_sql(name='test', con=con, if_exists='append', index=False, dtype=dtypedict)