import tushare as ts
import pandas as pd
df = ts.get_tick_data('600848',date='2018-12-12',src='tt')
df.head(10)


#########tushare pro
import tushare as ts
ts.set_token('bbe62c4557d639a8fc050c17c8fb7d6ec8d8611ca94dcac42136822b')
pro = ts.pro_api()
# 日线数据
df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')

df = ts.pro_bar(ts_code='000001.SZ', start_date='20130101', end_date='20161011', asset='E', freq='1min')

import os

filename = 'dataTest2.csv'
path = os.path.join(os.getcwd(), 'QuantData',filename)
df.to_csv(path)

#查询当前所有正常上市交易的股票列表
pro = ts.pro_api()

data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
filename = 'stock_list.csv'
path = os.path.join(os.getcwd(), 'QuantData',filename)
data.to_csv(path)