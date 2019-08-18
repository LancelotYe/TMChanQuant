import tushare as ts



def ts_get_oms_price(ts_code, start_date, end_date):
    # get tick data from tushare
    # 一次最多获取7000条数据
    # 假设从20140112-20130111，从20140112开始往后获取7000条数据，最多到20131129，中间跨度最多30个交易日
    # 所以我们保守可以一次下载15天，最多不超过30天
    '''
    :param ts_code: symbol 000000.SZ
    :param start_date: YYYYMMDD
    :param end_date: YYYYMMDD
    :return: df
    '''
    try:
        df1 = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, asset='E', freq='1min')
    except Exception as msg:
        print(msg)
        return None
    return df1


def ts_get_trade_date(start_date, end_date):
    '''
        :param start_date: YYYYMMDD
        :param end_date: YYYYMMDD
        :return: df
        '''
    pro = ts.pro_api()
    df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
    return df

# ts_code = '000001.SZ'
# start_date = '20120301'
# start_date = '20120320'
# end_date = '20120320'
# df1 = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, asset='E', freq='1min')