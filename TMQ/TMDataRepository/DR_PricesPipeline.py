#  数据传输管道
import os
import tushare as ts
import datetime
import pymysql
import sqlalchemy


def connect_MySQL():
    # 打开数据库连接
    host = 'localhost'
    port = 3306
    user = 'root'
    password = '68466296aB'
    DB = 'DR_DataBase'

    symbol_id = '000001.SZ'
    create_database(host, port, user, password)
    df = get_1min_price(symbol_id=symbol_id, start = '20180701', end = '20180718')
    # mysql: // user: passwd @ 127.0.0.1 / db_name?charset = utf8
    engine = sqlalchemy.create_engine("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(user, password, host, port, DB))
    con = engine.connect()
    rush_pipe_to_db(df, con, 'test_table')

def create_database(host, port, user, password):
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

    sql_cmd = 'CREATE DATABASE IF NOT EXISTS DR_DataBase'
    try:
        cursor.execute(sql_cmd)
    except Exception as msg:
        print(msg)
    connection.close()

def get_sql_files():
    sqlFileName = 'DR_DataBase.sql'
    sqlFileName = os.path.join(os.getcwd(), 'TMQ', 'TMDataRepository', sqlFileName)
    return  sqlFileName

    # sql_files = []
    # files = os.listdir(os.path.dirname(os.path.abspath(__file__)))
    # for file in files:
    #     if os.path.splitext(file)[1] == '.sql':
    #         sql_files.append(file)
    # return sql_files


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



def get_1min_price(symbol_id, start, end):
    pro = ts.pro_api()
    # 日线数据
    # df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
    df = pro.daily(ts_code=symbol_id, start_date=start, end_date=end)
    return df

def rush_pipe_to_db(df, connection, symbol_id):
    # name: 输出的表名
    # con: 与read_sql中相同，数据库链接
    # if_exits： 三个模式：fail，若表存在，则不输出；replace：若表存在，覆盖原来表里的数据；append：若表存在，将数据写到原表的后面。默认为fail
    # index：是否将df的index单独写到一列中
    # index_label: 指定列作为df的index输出，此时index为True
    # chunksize： 同read_sql
    # dtype: 指定列的输出到数据库中的数据类型。字典形式储存：{
    # column_name: sql_dtype}。常见的数据类型有sqlalchemy.types.INTEGER(), sqlalchemy.types.NVARCHAR(), sqlalchemy.Datetime()

    df.to_sql(
        name = symbol_id,
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


if __name__ == "__main__":
    connect_MySQL()