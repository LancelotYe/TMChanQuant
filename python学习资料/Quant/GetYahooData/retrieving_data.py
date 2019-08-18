#!/usr/bin/python
# -*- coding: utf-8 -*-

# retrieving_data.py

from __future__ import print_function

import pandas as pd
import MySQLdb as mdb


if __name__ == "__main__":
    # Connect to the MySQL instance
    db_host = 'localhost'
    db_user = 'sec_user'
    db_pass = 'password'
    db_name = 'securities_master'
    con = mdb.connect(db_host, db_user, db_pass, db_name)

    # Select all of the historic Google adjusted close data
    sql = """SELECT dp.price_date, dp.adj_close_price
             FROM symbol AS sym
             INNER JOIN daily_price AS dp
             ON dp.symbol_id = sym.id
             WHERE sym.ticker = 'GOOG'
             ORDER BY dp.price_date ASC;"""

    # Create a pandas dataframe from the SQL query
    goog = pd.read_sql_query(sql, con=con, index_col='price_date')    

    # Output the dataframe tail
    print(goog.tail())




# pandas内置雅虎金融数据对接
import pandas as pd
import numpy as np
from pandas_datareader import data, wb # 需要安装 pip install pandas_datareader
import datetime

# 定义获取数据的时间段
start = datetime.datetime(2017, 4, 1)
end = datetime.date.today()

# 获取股票信息 ex: 中国石油
# 如果要看上证指数请参考换成600000.ss
# 如果要看深成指请换成000001.sz
cnpc = data.DataReader("601857.SS", 'yahoo', start, end)

cnpc.head(5)

spy = data.DataReader("SPY", 'yahoo', start, end)
print(spy.tail(5))