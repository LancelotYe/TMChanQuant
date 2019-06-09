'''
《量化交易之路》读书笔记
'''

################################################################################################
# 2.1.1
price_str = '30.14, 29.58, 26.36, 32.56, 32.82'

price_array = price_str.split(',')

data_base = 20170118
# 4
data_array = [str(data_base + ind) for ind, _ in enumerate(price_array)]

data_array

# zip效果是同时迭代多个序列，每次分别从一个序列中取一个元素每一单其中某一序列到达结尾，则迭代宣告结束

stock_tuple_list = [(data, price) for data, price in zip(data_array, price_array)]
print('20170119日价格：{}'.format(stock_tuple_list[1][1]))

# 5.namedtuple可命名元祖，添加代码灵活性

from collections import namedtuple

stock_namedtuple = namedtuple('stock', ('date','price'))
stock_namedtuple_list = [stock_namedtuple(date, price) for date, price in zip(data_array, price_array)]

# 6.字典推导式 代码更简洁
stock_dict = {date: price for date, price in zip(data_array, price_array)}

# 7.字典有序
from collections import OrderedDict
stock_dict = OrderedDict((date, price) for date, price in zip(data_array, price_array))
stock_dict.keys()
################################################################################################
# 2.2.1
# 1.内置函数
# 对key操作
min(stock_dict)
# 对value操作
min(zip(stock_dict.values(), stock_dict.keys()))

# 2.自定义函数
# 计算所有收盘价格中第二大的价格元素
def find_second_max(dict_array):
    stock_prices_sorted = sorted(zip(dict_array.values(), dict_array.keys()))
    return stock_prices_sorted[-2]

if callable(find_second_max):
    print(find_second_max(stock_dict))

################################################################################################
# 2.2.2 lambda函数,函数为对象，类似block
find_second_max_lambda = lambda dict_array:sorted(zip(dict_array.values(), dict_array.keys()))[-2]

find_second_max_lambda(stock_dict)

# 返回多个值
def find_max_and_min(dict_array):
    stock_prices_sorted = sorted(zip(dict_array.values(), dict_array.keys()))
    return stock_prices_sorted[0], stock_prices_sorted[-1]

find_max_and_min(stock_dict)

################################################################################################
# 2.2.3
# 高阶函数
price_float_array = [float(price_str) for price_str in stock_dict.values()]
pp_array = [(price1, price2) for price1, price2 in zip(price_float_array[:-1], price_float_array[1:])]
# 下面使用map（）函数和reduce（）函数结合lambda函数完成需求，推导出每天的涨跌幅度
# 外层使用map（）函数针对pp_array的每一个元素执行操作，内层使用reduce（）函数即两个相邻的价格，求出涨跌幅度，返回外层结果list
from functools import reduce
change_array = map(
    lambda pp: reduce(lambda a, b: round((b-a)/a, 3), pp),
    pp_array
)
# print(list(change_array))
# map函数返回的数据类型是iterators，需要先转换成list类型
change_array = list(change_array)
# insert函数：insert(a,b)在索引a的位置，插入b
change_array.insert(0, 0)
change_array
'''
reduce(lambda a, b: round((b - a) / a, 3), (30.14, 29.58))
分解函数
round函数的作用是，保留小数点后三位round（x, 3）
map函数的作用，元祖组成的数组，将每个元祖拿出来使用作为reduce函数的参数
reduce函数的作用，传入数组参数与lambda的结合使用假设lambda是f（x,y）,传入的pp=[1,2,3,4,5],reduce(lambda x, y: f(x,y), [1,2,3,4,5])=f(f(f(f(f(1),2),3),4),5)
'''


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
################day1##################################day1##################################day1##################################day1##################
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################


stock_namedtuple = namedtuple('stock', ('date', 'price', 'change'))
stock_dict = OrderedDict((date, stock_namedtuple(date, price, change)) for date, price, change in zip(data_array, price_array, change_array))

# 使用fliter方法
up_days = filter(lambda day : day.change > 0 , stock_dict.values())
up_days = list(up_days)

# python 三目表达式
def filter_stock(stock_array_dict, want_up=True, want_calc_sum=False):
    if not isinstance(stock_array_dict, OrderedDict):
        raise TypeError('stock_array_dict must be OrderedDict!')
    # 三目表达式写法
    filter_func = (lambda day : day.change > 0) if want_up else (lambda day : day.change < 0)
    # 使用filter_func作为筛选函数
    want_days = list(filter(filter_func, stock_array_dict.values()))

    if not want_calc_sum:
        return want_days

    # 需要计算涨跌幅和
    change_sum = 0.0
    for day in want_days:
        change_sum += day.change
    return change_sum

# 全部使用默认参数
print('所有上涨交易日：{}'.format(filter_stock(stock_dict)))
# want_up = False
print('所有下跌交易日：{}'.format(filter_stock(stock_dict, want_up=False)))

# 计算所有上涨的总和
print('所有上涨交易日的涨幅和：{}'.format(filter_stock(stock_dict, want_calc_sum=True)))

# 计算所有下跌的总和
print('所有下跌交易日跌幅和：{}'.format(filter_stock(stock_dict, want_up=False, want_calc_sum=True)))


################################################################################################
# 2.2.4偏函数
from functools import partial
# 筛选上涨交易日
filter_stock_up_days = partial(filter_stock, want_up=True, want_calc_sum=False)
# 筛选下跌交易日
filter_stock_down_days = partial(filter_stock, want_up=False, want_calc_sum=False)
# 筛选计算上涨交易日涨幅和
filter_stock_up_sums = partial(filter_stock, want_up=True, want_calc_sum=True)
# 筛选计算下跌交易日涨幅和
filter_stock_down_sums = partial(filter_stock, want_up=False, want_calc_sum=True)
print('所有上涨的交易日：{}'.format(filter_stock_up_days(stock_dict)))
print('所有下跌的交易日：{}'.format(filter_stock_down_days(stock_dict)))
print('所有上涨交易日的涨幅和：{}'.format(filter_stock_up_sums(stock_dict)))
print('所有下跌交易日的跌幅和：{}'.format(filter_stock_down_sums(stock_dict)))

'''
偏函数：
funcVar = partial(func, var2, var3)
funcVar(var1)
'''

################################################################################################
# 2.3.1
# 面向对象
'''
-下划线开头的名字代表protect，被看作保护的变量，在模块或类外部不可以使用，只有类或者子类才可以访问。不可以直接访问，需要通过类提供的接口才可以访问，不能用from xxx import × 导入
-任何以双下划线开头的名字都代表private，是私有变量，意思只有类本身才可以访问
-以双下划线开头以及双下划线结尾的代表python里特殊方法专用标识，如__init__()代表类的构造函数

'''
from collections import namedtuple
from collections import OrderedDict
from functools import reduce
class StockTradeDays(object):
    def __init__(self, price_array, start_date, date_array=None):
        # 私有价格序列
        self.__price_array = price_array
        self.__date_array = self._init_days(start_date, date_array)
        self.__change_array = self.__init_change()
        self.stock_dict = self._init_stock_dict()
    def __init_change(self):
        price_float_array = [float(price_str) for price_str in self.__price_array]
        pp_array = [(price1, price2) for price1, price2 in zip(price_float_array[:-1], price_float_array[1:])]
        change_array = map(
            lambda pp: reduce(lambda a, b :round((b-a)/a, 3), pp),
            pp_array
        )
        change_array = list(change_array)
        change_array.insert(0,0)
        return change_array

    def _init_days(self, start_date, date_array):
        '''
        protect方法
        '''
        if date_array is None:
            date_array = [str(start_date + ind) for ind , _ in enumerate(self.__price_array)]
        else:
            date_array = [str(date) for date in date_array]
        return date_array

    def _init_stock_dict(self):
        '''
        使用namedtuple,OrderedDict将结果合并
        :return:
        '''
        stock_namedtuple = namedtuple('stock', ('date', 'price', 'change'))
        stock_dict = OrderedDict(
            (date, stock_namedtuple(date, price, change)) for date, price, change in zip(self.__date_array, self.__price_array, self.__change_array)
        )
        return stock_dict
    def filter_stock(self, want_up=True, want_calc_sum=False):
        filter_func = (lambda day: day.change > 0) if want_up else (lambda day:day.change < 0)
        want_days = filter(filter_func, self.stock_dict.values())
        if not want_calc_sum:
            return want_days
        change_sum = 0.0
        for day in want_days:
            change_sum += day.change
        return change_sum

    def __str__(self):
        return str(self.stock_dict)
    __repr__ = __str__
    def __iter__(self):
        for key in self.stock_dict:
            yield self.stock_dict[key]
    def __getitem__(self, ind):
        date_key = self.__date_array[ind]
        return self.stock_dict[date_key]
    def __len__(self):
        return len(self.stock_dict)
# 1
price_array = '30.14, 29.58, 26.36, 32.56, 32.82'.split(',')
date_base = 20170118
trade_days = StockTradeDays(price_array, date_base)
trade_days
# 2
print('trade_days对象长度为:{}'.format(len(trade_days)))
# 3
# 自定义类通过实现__iter__()方法来支持迭代操作
# 通过以下代码来实现trade_days是否支持迭代操作
from collections import Iterable
if isinstance(trade_days, Iterable):
    for day in trade_days:
        print(day)
# 4对象方法调用
list(trade_days.filter_stock())
# 5对象支持索引获取
# 下面使用真是股票数据构造tradeday
# 特斯拉

from abupy import ABuSymbolPd

price_array = ABuSymbolPd.make_kl_df('TSLA', n_folds=2).close.tolist()

date_array = ABuSymbolPd.make_kl_df('TSLA', n_folds=2).date.tolist()


price_array[:5],date_array[:5]

trade_days = StockTradeDays(price_array, date_base, date_array)

trade_days[-1]

########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
################day2##################################day2##################################day2##################################day2##################
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

# 2.3.2
# 封装、继承和多态是面向对象的三大特点
# 下面编写一个量化交易策略基类
import six
from abc import ABCMeta, abstractmethod
class TradeStrategyBase(six.with_metaclass(ABCMeta, object)):
    '''
    量化策略抽象基类
    '''
    @abstractmethod
    def buy_strategy(self, *args, **kwargs):
        # 买入策略基类
        pass
    @abstractmethod
    def sell_strategy(self, *args, **kwargs):
        # 卖出策略基类
        pass

'''
    元类就是创建类的类，在python中，只有type类及其子类才可以当元类，
    type创建类时，参数格式：type(classname,parentclasses,attrs),
    classname是类名，字符串类型,
    parentclasses是类的所有父类，元祖类型,
    attrs是类的所有{属性：值},是字典类型
    一切类的创建最终都会调用type.__new__(cls,classname,bases,attrs),它会在堆中创建一个类对象，并返回该对象
    当通过type.__new__(cls,classname,bases,attrs)创建类时,cls就是该类的元类，它是type类或其子类。
    ABCMeta是一个抽象类的元类，用来创建抽象类基类：Metaclass for defining Abstract Base Classes(ABCs)
    six.with_metaclass是用元类来创建类的方法，调用一个内部类，在内部类的__new__函数中，返回一个新创建的临时类
    six.with_metaclass(ABCMeta, object)就是通过内部类__new__函数返回一个ABCMeta元类创建的临时类，作为TradeStrategyBase类是ABCMeta元类的对象，是由ABCMeta元类生成的
'''
'''
    TradeStrategyBase类通过继承ABCMeta,@abstractmethod声明方法为接口。@xxx这种方法在Python中称为装饰器。装饰器是在Python闭包技术基础上再次底层封装的技术，是建立在Python里一切皆对象的根本上。多个装饰器修饰一个方法时，需要注意装饰器的顺序。
    def buy_strategy(self, *args, **kwargs):中*args,**kwargs代表可接受任意数量参数的函数。
    为了能让一个函数接受任意数量的位置参数，可以使用一个*参数，他的数据结构类型为list列表。为了接受任意数量的关键字参数，使用一个以**开头的参数，它的数据结构类型为dict类型。
'''

'''
下面编写具体的量化策略TradeStrategy1,继承TradeStrategyBase实现buy_strategy()与sell_strategy()接口。它的交易策略为：当股价上涨一个阀值（默认7%）时买入股票并持有s_keey_stock_threshold天，代码如下：
'''
class TradeStrategy1(TradeStrategyBase):
    '''
    买入股票并持有20天
    '''
    s_keep_stock_threshold = 20
    def __init__(self):
        self.keep_stock_day = 0
        self.__buy_change_threshold = 0.07
    def buy_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_day == 0 and trade_day.change > self.__buy_change_threshold:
            self.keep_stock_day += 1
        elif self.keep_stock_day > 0:
            self.keep_stock_day += 1
    def sell_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_day >= TradeStrategy1.s_keep_stock_threshold:
            self.keep_stock_day = 0

    @property
    def buy_change_threshold(self):
        return self.__buy_change_threshold
    @buy_change_threshold.setter
    def buy_change_threshold(self, buy_change_threshold):
        if not isinstance(buy_change_threshold, float):
            raise TypeError('buy_change_threshold must be float!')
        self.__buy_change_threshold = round(buy_change_threshold, 2)


class TradeLoopBack(object):
    '''
    交易回测系统
    '''
    def __init__(self, trade_days, trade_strategy):
        '''
        使用前面封装的StockTradeDays类和本节编写的交易策略类
        TradeStrategyBase类初始化交易系统
        :param trade_days:
        :param trade_strategy:
        '''
        self.trade_days = trade_days
        self.trade_strategy = trade_strategy
        # 交易盈亏结果序列
        self.profit_array = []
    def execute_trade(self):
        '''
        执行交易系统
        :return:
        '''
        for ind, day in enumerate(self.trade_days):
            '''
            以时间驱动，完成交易回测
            '''
            if self.trade_strategy.keep_stock_day > 0:
                # 如果有持有股票，加入交易盈亏结果序列
                self.profit_array.append(day.change)
            # hasattr用来查询对象有没有实现某个方法
            if hasattr(self.trade_strategy, 'buy_strategy'):
                # 买入策略执行
                self.trade_strategy.buy_strategy(ind, day, self.trade_days)

            if hasattr(self.trade_strategy, 'sell_strategy'):
                # 卖出策略执行
                self.trade_strategy.sell_strategy(ind, day, self.trade_days)

trade_loop_back = TradeLoopBack(trade_days, TradeStrategy1())
trade_loop_back.execute_trade()
print('回测策略1总盈亏为：{}%'.format(reduce(lambda a, b : a+b, trade_loop_back.profit_array) * 100))

import numpy as np
import matplotlib.pyplot as plt
plt.plot(np.array(trade_loop_back.profit_array).cumsum())


################################################################################################
# 静态方法、类方法与属性
# 1.属性
# TradeStrategy1 类中的slef.__buy_change_threshold被定义为私有变量，外部不能直接赋值，使用了@property来赋值，代码如下
'''
    @property
    def buy_change_threshold(self):
        # getter 函数
        return self.__buy_change_threshold
    @buy_change_threshold.setter
    def buy_change_threshold(self, buy_change_threshold):
        if not isinstance(buy_change_threshold, float):
            raise TypeError('buy_chnage_threshold must be float!')
        self.__buy_change_threshold = round(buy_change_threshold, 2)
'''
# 第一个@property方法是一个getter函数，它使得buy_change_threshold成为一个属性，
# @buy_change_threshold.setter属性添加了setter函数，这样外部的访问和设置形式如下。
# 访问：
trade_strategy1 = TradeStrategy1()
trade_strategy1.buy_change_threshold
# 设置
trade_strategy1.buy_change_threshold = 0.08
trade_strategy1.buy_change_threshold

# 使用@property的目的是给实力增加除访问与修改之外的其他处理逻辑，比如buy_change_threshold.setter做了类型检查和将float阀值保留两位小数操作，不要写没有做任何其他额外操作的property。
trade_strategy1 = TradeStrategy1()
trade_strategy1.buy_change_threshold = 0.1
trade_loop_back = TradeLoopBack(trade_days, trade_strategy1)
trade_loop_back.execute_trade()
print('回测策略1总盈亏为：{}%'.format(reduce(lambda a , b : a + b, trade_loop_back.profit_array)) * 100)
plt.plot(np.array(trade_loop_back.profit_array).cumsum())


################################################################################################
# 继续编写一个均值回复交易策略，当股价连续两个交易日下跌，且下跌幅度超过一个阀值（默认-10%）时，买入股票并持有s_keep_stock_threshold(10天)，代码如下
class TradeStrategy2(TradeStrategyBase):
    '''
    交易策略2：均值回复策略，当股价连续两个交易日下跌，且下跌幅度超过阀值默认s_buy_change_threshold(-10%),
    买入股票并持有s_keep_stock_threshold(10天)
    '''
    # 买入后持有天数
    s_keep_stock_threshold=10
    # 下跌买入阀值
    s_buy_change_threshold = -0.10
    def __init__(self):
        self.keep_stock_day = 0
    def buy_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_day == 0 and trade_ind >= 1:
            '''当没有持有股票的时候self.keep_stock_day == 0 并且trade_ind>=1,不是所有交易开始的第一天，因为需要yesterday数据'''
            #trade_day.change < 0 bool:今天股价是否下跌
            today_down = trade_day.change < 0
            #昨天股价是否下跌
            yesterday_down = trade_days[trade_ind - 1].change < 0
            # 两天总跌幅
            down_rate = trade_day.change + trade_days[trade_ind - 1].change
            if today_down and yesterday_down and down_rate < TradeStrategy2.s_buy_change_threshold:
                # 买入条件成立：连跌两天，跌幅超过s_buy_change_threshold
                self.keep_stock_day += 1
        elif self.keep_stock_day > 0:
            self.keep_stock_day += 1
    def sell_strategy(self, trade_ind, trade_day, trade_days):
        if self.keep_stock_day >= TradeStrategy2.s_keep_stock_threshold:
            self.keep_stock_day = 0
    @classmethod
    def set_keep_stock_threshold(cls, keep_stock_threshold):
        cls.s_keep_stock_threshold = keep_stock_threshold
    @staticmethod
    def set_buy_chnage_threshold(buy_change_threshold):
        TradeStrategy2.s_buy_change_threshold = buy_change_threshold

trade_strategy2 = TradeStrategy2()
trade_loop_back = TradeLoopBack(trade_days, trade_strategy2)
trade_loop_back.execute_trade()
print('回测策略2总盈亏为：{}%'.format(
    reduce(lambda a, b : a + b , trade_loop_back.profit_array)*100
))

plt.plot(np.array(trade_loop_back.profit_array).cumsum())