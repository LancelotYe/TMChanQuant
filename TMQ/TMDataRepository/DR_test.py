
import pandas as pd
import pymysql

host = 'localhost'
port = 3306
user = 'root'
password = '68466296aB'
DB = 'DR_DataBase'

# symbol_id = '000001.SZ'
connection = pymysql.connect(port=port,
                             host=host,
                             user=user,
                             password=password,
                             # db=DB,
                             charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
# 创建DB和Table


# columns = ['ts_code', 'trade_time', 'open', 'high', 'low', 'close', 'vol', 'amount', 'trade_date', 'pre_close']
cursor = connection.cursor()
table_name = 'TT'
start = '2013-01-02'
end = '2013-01-08'

select = 'SELECT DISTINCT trade_date FROM tt WHERE trade_time>\'2013-01-02\' and trade_time<\'2013-01-08\' ORDER BY trade_time  ASC;'

select1 = 'SELECT * FROM {} WHERE trade_time>\'{}\' and trade_time<\'{}\' ORDER BY trade_time  ASC;'.format(table_name, start, end)
cursor.execute('Use {}'.format(DB))
cursor.execute(select1)
result = cursor.fetchall()
connection.close()


import tushare as ts
df = pd.DataFrame(list(result), columns = columns)


pro = ts.pro_api()
trade_date_df = pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')




# 打包存入数据库
def get_price_df(ts_code, start_date, end_date):
    df1 = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, asset='E', freq='1min')
    return df1
df = get_price_df(ts_code='000001.SZ', start_date='20130111', end_date='20140112')
columns = ['ts_code', 'trade_time', 'open', 'high', 'low', 'close', 'vol', 'amount', 'trade_date', 'pre_close']
res = zip(*(df[a] for a in columns))
sql = 'INSERT IGNORE INTO {} VALUES '.format(table_name)
for i in res:
    sql = sql + '{}'.format(i) + ','
sql = sql.strip(',')



# 连接数据库
import pymysql
connection = pymysql.connect(port=port,
                             host=host,
                             user=user,
                             password=password,
                             db=DB,
                             charset='utf8')
cursor = connection.cursor()
try:
    cursor.execute(sql)
    connection.commit()
except Exception as msg:
    print(msg)
cursor.close()
connection.close()