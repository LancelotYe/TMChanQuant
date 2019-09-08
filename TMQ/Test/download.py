import tushare as ts
import pandas as pd
import sys


def download(ts_code, start_date, end_date):
    pro = ts.pro_api()
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    tdf = pd.DataFrame()
    tdf['Date'] = df.trade_date
    tdf['Date'] = tdf['Date'].map(lambda x: '{}-{}-{}'.format(x[:4], x[4:6], x[6:8]))
    tdf['Open'] = df.open
    tdf['High'] = df.high
    tdf['Low'] = df.low
    tdf['Close'] = df.close
    tdf['Adj_Close'] = df.close
    tdf['Volume'] = df.vol
    tdf.to_csv('{}.csv'.format(ts_code))
    return tdf


if __name__ == '__main__':
    # download('000001.SZ', '20150102','20180102')
    download(sys.argv[1], sys.argv[2], sys.argv[3])


