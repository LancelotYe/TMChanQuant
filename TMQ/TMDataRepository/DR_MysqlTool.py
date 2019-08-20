import pymysql
import pandas as pd
from abc import ABC,abstractmethod
import TMQ.TMDataRepository.DR_Config as drc


class MysqlTool(ABC):
    def __init__(self, conf_dict):
        self.g_connection = None
        self.connect_db(conf_dict)

    # 连接数据库
    def connect_db(self):
        conf_dict = drc.get_mysql_config_dict()
        # 连接数据库
        host = conf_dict['host']
        port = int(conf_dict['port'])
        user = conf_dict['user']
        password = conf_dict['password']
        db_name = conf_dict['db']
        self.g_connection = pymysql.connect(port=port,
                                            host=host,
                                            user=user,
                                            password=password,
                                            # db='demo',
                                            charset='utf8')
        cursor = self.g_connection.cursor()
        sql_create_db_cmd = 'CREATE DATABASE IF NOT EXISTS {};'.format(db_name)
        sql_use_db = 'USE {};'.format(db_name)
        try:
            cursor.execute(sql_create_db_cmd)
            cursor.execute(sql_use_db)
        except Exception as msg:
            print(msg)

    # 断连
    def disconnect_db(self):
        self.g_connection.close()

    #  创建表
    @abstractmethod
    def create_table(self, *args, **kwargs):
        pass

    # 插入数据
    @abstractmethod
    def insert_data(self, *args, **kwargs):
        pass

    # 获取数据
    @abstractmethod
    def get_data_from_db(self, *args, **kwargs):
        pass

    # 获取存在的索引
    @abstractmethod
    def get_exist_trade_date_index(self, *args, **kwargs):
        pass

    # 得到表名
    @abstractmethod
    def trans_ts_code_to_table_name(self, *args, **kwargs):
        pass


class OmsMysqlTool(MysqlTool):
    def __init__(self, conf_dict):
        super(OmsMysqlTool, self).__init__(conf_dict)
        self.oms_columns = ['ts_code','trade_time','open','high','low','close','vol','amount','trade_date','pre_close']

    # def connect_db(self):
    #     super(OmsMysqlTool, self).connect_db()
    #
    # def disconnect_db(self):
    #     super(OmsMysqlTool, self).disconnect_db()

    # 以下方法针对一分钟的股票数据，标记为OneMinuteStock简化为oms
    # 一分钟股票数据表格创建
    def create_table(self, ts_code):
        cursor = self.g_connection.cursor()
        # # 创建Table
        table_name = self.trans_ts_code_to_table_name(ts_code)
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
                '''.format(*self.oms_columns)
        sql_create_table_cmd = 'CREATE TABLE IF NOT EXISTS {} ({}) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8MB4;'.format(
            table_name, element)
        try:
            cursor.execute(sql_create_table_cmd)
        except Exception as msg:
            print(msg)

    def insert_data(self, ts_code, df):
        cursor = self.g_connection.cursor()
        table_name = self.trans_ts_code_to_table_name(ts_code)
        if len(df) == 0:
            print('No Data')
            return;
        df = df.fillna(999999)
        res = zip(*(df[a] for a in self.oms_columns))
        sql = 'INSERT IGNORE INTO {} VALUES '.format(table_name)
        for i in res:
            sql = sql + '{}'.format(i) + ','
        sql = sql.strip(',')
        try:
            cursor.execute(sql)
            self.g_connection.commit()
        except Exception as msg:
            print(msg)
            return False
        # cursor.close()
        return True

    # 获取数据库股票数据
    def get_data_from_db(self, ts_code, start, end, is_asc):
        # get tick data from database
        '''
        :param cursor: 游标
        :param table_name: 表名
        :param start: YYYY-MM-DD
        :param end: YYYY-MM-DD
        :param is_asc: 排序
        :return: 数据库股票数据
        '''
        cursor = self.g_connection.cursor()
        table_name = self.trans_ts_code_to_table_name(ts_code)
        order = 'ASC' if is_asc else 'DESC'
        select = 'SELECT * FROM {} WHERE trade_time>\'{}\' and trade_time<\'{}\' ORDER BY trade_time {};'.format(table_name, start, end, order)
        print(select)
        df = []
        try:
            cursor.execute(select)
            result = cursor.fetchall()
            df = pd.DataFrame(list(result), columns=self.oms_columns)
        except Exception as msg:
            print(msg)
        return df

    # result = ['20130102', '20130104']
    # start = '2013-01-02'
    # end = '2013-01-08'
    # select = 'SELECT * FROM {} WHERE trade_time>\'{}\' and trade_time<\'{}\' ORDER BY trade_time ASC;'.format(
    #     table_name,
    #     start, end)
    # 使用 cursor() 方法创建一个游标对象 cursor
    # 创建DB和Table

    # 获取数据库已存在的交易日期索引
    def get_exist_trade_date_index(self, ts_code, start, end):
        cursor = self.g_connection.cursor()
        table_name = self.trans_ts_code_to_table_name(ts_code)
        select = 'SELECT DISTINCT trade_date FROM {} \
        WHERE trade_time>\'{}\' and trade_time<\'{}\' \
        ORDER BY trade_time  ASC;'.format(
            table_name, start, end)
        result = []
        try:
            cursor.execute(select)
            # result = pd.DataFrame(list(cursor.fetchall()))
            result = [date[0] for date in cursor.fetchall()]
        except Exception as msg:
            print(msg)
        return result

    # 转换表名
    def trans_ts_code_to_table_name(self, ts_code):
        # ts_code改表名
        arr = ts_code.split('.')
        if len(arr) != 2:
            print('Ts_code Type Error')
            return ''
        table_name = arr[1] + arr[0]
        return table_name

# import TMQ.TMDataRepository.DR_TushareTool as tst
# ts_code = '000001.SZ'
# start_date = '20120103'
# end_date = '20120530'
# trade_date_df = tst.ts_get_trade_date(start_date, end_date)
class DownloadListMysqlTool(MysqlTool):
    def __init__(self, conf_dict):
        super(DownloadListMysqlTool, self).__init__(conf_dict)
        # cal_date作为索引，一份代码对应一个表
        self.download_list_columns = ['symbol', 'exchange', 'cal_date' , 'is_open', 'has _data']