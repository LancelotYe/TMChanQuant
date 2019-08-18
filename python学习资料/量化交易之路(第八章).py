'''
以下代码为第七章海龟交易法
'''
# from abu.abupy import AbuFactorBuyBase
#
# class AbuFactorBuyBreak(AbuFactorBuyBase):
#     def __init__(self, **kwargs):
#         # 突破xd
#         self.xd = kwargs['xd']
#         # 忽略连续创新高，比如买入后第二天又突破新高，忽略
#         self.skip_days = 0
#         # 在输出生成的orders_pd中显示名字
#         self.factor_name = '{}:{}'.format(self.__class__.__name__,self.xd)
#
#
#     def fit_day(self, today):
#         day_ind = int(today.key)
#         # 忽略不符合买入日（统计周期内前xd天及最后一天）
#         if day_ind < self.xd - 1 or day_ind >= self.kl_pd.shape[0] - 1:
#             return None
#
#         if self.skip_days > 0:
#             # 执行买入订单后的忽略
#             self.skip_days -= 1
#             return None
#
#         # 今天收盘价格达到xd天内最高价格则符合条件
#         if today.close == self.kl_pd.close[day_ind - self.xd + 1:day_ind+1].max():
#             # 把xd赋值给忽略买入日，即xd天内再次又创新高，也不买了
#             self.skip_days = self.xd
#             # 生成买入订单
#             return self.make_buy_order(day_ind)
#         return None

from abu.abupy import AbuFactorBuyBreak