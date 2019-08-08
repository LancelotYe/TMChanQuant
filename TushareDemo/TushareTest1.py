import tushare as ts
df = ts.get_tick_data('600848',date='2018-12-12',src='tt')
df.head(10)