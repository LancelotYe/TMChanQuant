import tushare as ts
from numpy import NaN
import pandas as pd


# ts.set_token('bbe62c4557d639a8fc050c17c8fb7d6ec8d8611ca94dcac42136822b')

def one_day_sell(ts_code, start_date, end_date):
    df1 = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, asset='E', freq='15min')
    df1 = df1.sort_values(by='trade_time')
    df = df1[df1['trade_time'].str.contains('14:45:00')|df1['trade_time'].str.contains('09:45:00')]
    df.loc[df['trade_time'].str.contains('14:45:00'), 'buytime'] = 1
    df = df.fillna(0)
    df.pre_close = df.close.shift()
    df['win_money'] = df.close - df.pre_close
    df.loc[df.buytime==1,'win_money'] = NaN
    df.loc[df.win_money>0, 'win'] = 1
    df.loc[df.win_money<=0, 'win'] = 0
    df1['win'] = df.win
    df1['win_money'] = df.win_money
    df1.to_csv('{}.csv'.format(ts_code))

pro = ts.pro_api()
df = pro.hs_const(hs_type='SH')
df.to_csv('SH.csv')
df = pro.hs_const(hs_type='SZ')
df.to_csv('SZ.csv')

if __name__ == '__main__':
    start_date = '20190408'
    end_date = None
    # ts_code = '000001.SZ'
    df = pd.read_csv('SH.csv')
    ts_codes = list(df[12:16].ts_code)
    for code in ts_codes:
        one_day_sell(code, start_date, end_date)
