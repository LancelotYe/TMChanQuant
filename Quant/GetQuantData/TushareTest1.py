import tushare as ts
df = ts.get_tick_data('600848',date='2018-12-12',src='tt')
df.head(10)


#########tushare pro
import tushare as ts
ts.set_token('token')
pro = ts.pro_api()
# 日线数据
df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')


df = ts.pro_bar(ts_code='000001.SZ', start_date='20180101', end_date='20181011', asset='E', freq='1min')