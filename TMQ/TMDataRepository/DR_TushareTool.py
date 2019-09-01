import tushare as ts
import TMQ.Tool.TMDate as tmd
import TMQ.Tool.TMConfig as tmc
from TMQ.Tool.TMConfig import tm_print
import datetime
import threading


class TsTool():
    _instance_lock = threading.Lock()
    def __init__(self):
        self.tokens = self.get_token()
        self.using_token = None
        self.using_time = None
        self.target_refresh_time = datetime.datetime.today()
        self.token_index = None

    @classmethod
    def instance(cls, *args, **kwargs):
        with TsTool._instance_lock:
            if not hasattr(TsTool, "_instance"):
                TsTool._instance = TsTool()
        return TsTool._instance

    def check_token(self):
        # 设置刷新时间
        if datetime.datetime.now() >= self.target_refresh_time:
            self.target_refresh_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
            self.using_time = 5
            self.token_index = 0
            self.using_token = self.tokens[self.token_index]
            ts.set_token(self.using_token)
        else:
            using_time = self.using_time - 1
            if using_time == 0:
                using_time = 5
                self.token_index += 1
                self.using_token = self.tokens[self.token_index]
                ts.set_token(self.using_token)
            self.using_time = using_time

        if self.token_index >= len(self.tokens):
            tmc.tm_print('token已经使用完毕')
            return False

        # print('using_token:{}\nusing_time:{}\ntargte_refresh_tim:{}\ntoken_index:{}'
        #       .format(self.using_token,self.using_time,self.target_refresh_time,self.token_index))
        return True

    def get_token(self):
        tokens = tmc.get_ts_tokens()
        return tokens



    # 大于start日期小于end日期的价格
    def ts_get_oms_price(self, ts_code, start_date, end_date):
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
        if self.check_token() == False:
            return None

        end_date = tmd.date_add_days(end_date, 1)
        try:
            df1 = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, asset='E', freq='1min')
        except Exception as msg:
            print(msg)
            return None
        return df1

    # start到end所有交易日期
    def ts_get_trade_date(self, start_date, end_date):
        '''
            :param start_date: YYYYMMDD
            :param end_date: YYYYMMDD
            :return: df
            '''
        pro = ts.pro_api()
        df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
        return df

