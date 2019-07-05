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
    def set_buy_change_threshold(buy_change_threshold):
        TradeStrategy2.s_buy_change_threshold = buy_change_threshold

trade_strategy2 = TradeStrategy2()
trade_loop_back = TradeLoopBack(trade_days, trade_strategy2)
trade_loop_back.execute_trade()
print('回测策略2总盈亏为：{}%'.format(
    reduce(lambda a, b : a + b , trade_loop_back.profit_array)*100
))

plt.plot(np.array(trade_loop_back.profit_array).cumsum())








########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
################day3##################################day3##################################day3##################################day3##################
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################


# 静态方法类方法
# python中通过装饰器@classmethod与@staticmethod来表明方法为类方法和静态方法，通过类名.方法名()的形式调用：
# @staticmethod不需要任何参数。
# @classmethod不需要self参数，但第一个参数需要是表示自身的cls参数
# s_keep_stock_threshold与s_buy_change_threshold在TradeStrategy2中定义的方式都为类全局变量。
# @staticmethod方法中如果要使用带这个类中的变量，只能使用类名.属性名或者类名.方法名
# 代码如下:
# @staticmethod
# def set_buy_change_threshold(buy_change_threshold):
#     TradeStrategy2.s_buy_change_threshold = buy_change_threshold
# # @classmethod方法函数声明中持有cls参数们可以通过cls来访问类变量,如下面cls.s_keep_stock_threshold的使用,所以它的优点是避免硬编码.
# @classmethod
# def set_keep_stock_threshold(cls, keep_stock_threshold):
#     cls.s_keep_stock_threshold = keep_stock_threshold
# # 一下代码实现通过类方法和静态方法修改策略参数
# trade_strategy2 = TradeStrategy2()
# TradeStrategy2.set_buy_chnage_threshold(-0.08)
# TradeStrategy2.set_keep_stock_threshold(20)

################################################################################################
# 2.4.1
# 性能与效率
# itertools的使用
# 标准库中itertools提供了很多生成循环器的工具,其中很重要的用途是生成集合所有可能方式的元素排列或组合.在量化数据处理中经常需要使用itertools来完成数据的各种排列组合以寻找最优参数

import itertools
# (1)permutations()函数,考虑顺序组合元素,示例如下
items = [1,2,3]
for item in itertools.permutations(items):
    print(item)

# (2)combinations()函数,不考虑顺序,不放回数据
for item in itertools.combinations(items, 2):
    print(item)
# (3)combinations_with_replacrment()函数,不考虑顺序,有放回数据
for item in itertools.combinations_with_replacement(items, 2):
    print(item)

# (4)product函数,笛卡儿积.针对多个输入顺序进行排列组合,示例如下:
ab = ['a','b']
cd = ['c','d']
# 针对ab,cd两个集合进行排列组合
for item in itertools.product(ab, cd):
    print(item)

# 在量化中通过参数组合来寻找最优参数时一般都会使用笛卡儿积,本节将重点示列
# 下面继续刚才的回测实列,使用itertools.product(笛卡儿积)求出TradeStrategy2的最优参数,即求出下跌幅度买入阀值(s_buy_change_threshold)与买入股票后持有天数(s_keep_stock_threshold)如何取值,可以让策略最终盈利最大化.
# 首先将2.3节修改TradeStrategy2策略基础参数并执行回测的代码抽象出一个函数calc(),该函数的输入参数有两个,分别是持有天数和下跌买入阀值;输出返回值为3个,分别是盈亏情况,输入的持股天数和下跌买入阀值

def calc(keep_stock_threshold, buy_change_threshold):
    '''
    :param keep_stock_threshold:持股天数
    :param buy_change_threshold:下跌买入阀值
    :return:盈亏情况,输入的持股天数,输入的下跌买入阀值
    '''
    trade_strategy2 = TradeStrategy2()
    TradeStrategy2.set_keep_stock_threshold(keep_stock_threshold)
    TradeStrategy2.set_buy_change_threshold(buy_change_threshold)
    # 进行回测
    trade_loop_back = TradeLoopBack(trade_days, trade_strategy2)
    trade_loop_back.execute_trade()
    # 计算回测结果的最终盈亏值profit
    profit = 0.0 if len(trade_loop_back.profit_array) == 0 else reduce(lambda a, b : a + b, trade_loop_back.profit_array)
    # 返回值profit和函数的两个输入参数
    return profit, keep_stock_threshold, buy_change_threshold

# 测试,使用2.3节使用的参数
calc(20, -0.08)

# 笛卡儿积求最优属于有限参数范围内求最优的问题，即将有限个参数形成集合，多个有限集合进行笛卡儿积，寻找问题的最优参数。下面通过range（）函数使具体参数形成有限集合
# 示例如下
# range集合：买入后持股天数从2~30天，间隔两天
keep_stock_list = list(range(2, 30, 2))
print('持股天数参数组：{}'.format(keep_stock_list))
# 下跌买入阀值从-0.05到-0.15，即从5%下跌到15%
buy_change_list = [buy_change / 100.0 for buy_change in range(-5, - 16, -1)]
print('下跌阀值参数组：{}'.format(buy_change_list))

# 通过对多个有限集合进行笛卡儿积，使用上面封装的函数calc()分别将各个组合参数代入，计算参数对应的最终盈利结果，将结果加入result序列
result = []
for keep_stock_threshold, buy_change_threshold in itertools.product(keep_stock_list, buy_change_list):
    # 使用calc（）函数计算参数对应的最终盈利，结果加入result序列
    result.append(calc(keep_stock_threshold, buy_change_threshold))
print('笛卡儿积参数集合总共结果为:{}个'.format(len(result)))

# 下面使用sorted(result)将结果序列排序
# [::1]将整个排序结果反转，反转后盈亏收益从最高向低开始排序
# [:10]取出收益最高的前十个组合查看
sorted(result)[::-1][:10]


################################################################################################
# 2.4.2多进程 vs 多线程
# 真实运算中计算非常复杂，面对这个问题，一般使用多任务并行的方式来解决：
'''
启动多个进程
启动多个线程
启动多个进程，每个进程启动多个线程
'''
# 使用哪种方式最好？
# 由于全局解释锁GIL，Python的线程被限制为同一时刻值允许一个线程执行，所以Python的多线程适用于处理I/O密集型任务和并发执行的阻塞操作，多进程处理并行的计算密集型任务
# 1.使用多进程
# 下面使用（ProcessPoolExecutor）
from concurrent.futures import ProcessPoolExecutor
result = []
# 回调函数，通过add_done_callback任务完成后调用
def when_done(r):
    # when_done在主进程中运行
    result.append(r.result())
    '''
    with class_a() as a:上下文管理器：
    with作为关键字开头的python中称为上下文管理器，它的特点是：
    -在进入上下文管理器定义的缩进模块后，会触发A_Class中定义的__enter__()函数；
    -在结束上下文管理器定义的缩进模块后，会触发A_Class中定义的__exit__()函数。
    一般在__enter__()和__exit__()函数中定义相反的操作，如文件的打开和关闭，资源的创建和释放等。列如，在线程锁类threading.RLock中可以找到如下实现:
    def __enter__(self)
        self.acquire()
    def __exit__(self, t, v, tb):
        self.release()
    通过在__enter__()函数中使用acquire()函数来上锁，通过在__exit__()函数中使用release()函数来解锁
    '''
with ProcessPoolExecutor() as pool:
    for keep_stock_threshold, buy_change_threshold in itertools.product(keep_stock_list, buy_change_list):
        '''
            submit提交任务：使用calc()函数和的参数通过submit提交到独立进程提交的任务必须是简单函数，进程并行不支持类方法，闭包等，函数参数和返回值必须兼容pickle序列化，因为进程间的通信需要传递可序列化对象
        '''
        future_result = pool.submit(calc, keep_stock_threshold, buy_change_threshold)
        # 当进程完成任务即calc运行结束后的回调函数
        future_result.add_done_callback(when_done)

sorted(result)[::-1][:10]

# 2使用多线程ThreadPoolExecutor
# 使用多线程ThreadPoolExecutor与前面使用多进程的方法几乎一模一样，唯一的区别是使用ThreadPoolExecutor代替ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
result = []
def when_done(r):
    result.append(r.result())
with ThreadPoolExecutor() as pool:
    for keep_stock_threshold, buy_change_threshold in itertools.product(keep_stock_list, buy_change_list):
        future_result = pool.submit(calc, keep_stock_threshold, buy_change_threshold)
        future_result.add_done_callback(when_done)
sorted(result)[::-1][:10]

# 仔细观察上面 多线程运行的输出结果可以发现，与串行的结果和多进程的结果不一致。原因在calc()函数中：
# TradeStrategy2.set_keep_stock_threshold(keep_stock_threshold)
# TradeStrategy2.set_buy_change_threshold(buy_change_threshold)
# 这两个设置参数的方法都是类方法，非实例方法。在同一进程中的多个线程不断针对类变量设置参数，结果是错误的，并无我们预想的结果。

# 2.4.3使用编译库提高性能
# 前面使用了多进程和多线程并行处理任务的技术，来提升Python代码的运行效率，除此之外，还有一些很棒的开源库可以提高性能比如：
# Numexpr可以快速计算数值，缺点是局限性大
# numba运行时动态编译Python代码来提高效率
# Cython静态编译Python代码来提高效率

# 买入后持股天数,放大寻找范围1~503天,间隔1天
keep_stock_list = list(range(1, 504, 1))
# 下跌买入阀值寻找范围 -0.01 ! -0.99 共99个
buy_change_list = [buy_change/100.0 for buy_change in range(-1, -100, -1)]
def do_single_task():
    task_list = list(itertools.product(keep_stock_list, buy_change_list))
    # print('笛卡儿积参数集合总共结果为:{}个'.format(len(task_list)))
    for keep_stock_threshold, buy_change_threshold in task_list:
        calc(keep_stock_threshold, buy_change_threshold)
# %time ipython magic code 详细查阅附录中关于Ipython的使用
%time do_single_task()

# numba动态编译可提高效率.下面可以看到只用一行代码nb.jit()来静态编译原始函数,之后调用编译好的do_singletask_nb()函数

import numba as nb
do_single_task_nb = nb.jit(do_single_task)
%time do_single_task_nb()

# 写代码要注意效率
for s in keep_stock_list+buy_change_list:
    print(s)

for s in itertools.chain(keep_stock_list, buy_change_list):
    print(s)

# 第一种方案会创建一个全新的序列,而itertools.chain()函数不会创建新的序列,所以如果输入序列非常大时会很节省内存,提升运行效率


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
################day4##################################day4##################################day4##################################day4##################
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

# 2.5代码调试

# 代码调试。

# python2中除法得到的结果不是浮点类型所以要做两步
# 1.导入from __future__ import division
# 2.buy_change/100.0 除数或者被除数中至少有一个浮点型
# 除了使用print函数可以打印输出以外还可以通过logging模块打印日志
import logging
# logging 有以下级别
'''
debug:调试信息
info:输出信息
warning:警告信息
error:错误信息
critical:严重错误
'''
# 通过loggin.basicConfig()统一设置运行环境日志的输出级别，只有大于等于设置级别的日志才能打印输出
logging.basicConfig(level=logging.INFO)
def gen_buy_change_list():
    logging.info("gen_buy_change_list begin")

# IDE中对断点支持最好的就是pycharm
import pdb
def gen_buy_change_list():
    for buy_change in range(-5, -16, -1):
        if buy_change == -10:
            # 通过set_trace打断点
            pdb.set_trace()
        buy_change = buy_change/100
        buy_change_list.append(buy_change)
    # 故意抛出异常
    raise RuntimeError('debug for pdb')
    return buy_change_list
try:
    _ = gen_buy_change_list()
except Exception as e:
    # 从捕获异常的地方开始调试，是经常使用的调试技巧
    pdb.set_trace()

'''
-l:堆栈信息
-n：下一步
-s:进入函数setp into
-c:继续执行continue
'''
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
################day5##################################day5##################################day5##################################day5##################
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
# 第三章 Numpy
# 量化工具
import numpy as np
normal_list = range(10000)
%timeit[i**2 for i in normal_list]

# NumPy数组和普通列表的操作方式也是不同的，NumPy通过广播机制作用与每一个内部元素，是一种并行化执行的思想，普通list则作用与整体
np_list = np.ones(5) * 3
print(np_list)
# 普通的列表把*3操作认为是整体性操作

# 3.1.2初始化操作
# 下面为一些常用的初始化np.array的方式：
# 100个0
np.zeros(100)
# shape:3行2列全是0
np.zeros((3,2))
# shape:3行2列全是1
np.ones((3,2))
# shape:x=2,y=3,z=3随机值
np.empty((2,3,3))
# 初始化序列与np_list一样的shape，值全是1
np.ones_like(np_list)
# 初始化序列与np_list一样的shape，值全是0
np.zeros_like(np_list)
# eye()得到对角线全是1的单位矩阵
np.eye(3)
# 可以将普通list作为参数，通过np.array来初始化np array
data = [[1,2,3,4],[5,6,7,8]]
arr_np = np.array(data)
arr_np

# 另外一个经常会使用的初始化方法linspace()。下面的示例在0~1之间等间隔生成10个元素的序列。
# 可以通过help(np.linspace)方法查看api文档
np.linspace(0,1,11)

# 下面的例子都尽量使用了股票数据，首先使用np.random.standard_normal()随机生成200只股票504个交易日服从正态分布的涨跌幅数据
# 504 = 252 * 2（两年每股交易日总数）
# 交易日的数量越多，股票的数量越多，生成的数据月服从正态分布
# 200只股票
stock_cnt = 200
# 504交易日
view_day = 504
# 生成服从正态分布：均值期望=0，标准差=1的序列
stock_day_change = np.random.standard_normal((stock_cnt, view_day))
# 打印出第一只股票，前5个交易日的涨跌幅情况
print(stock_day_change.shape)
print(stock_day_change[0:1,:5])
# 可以看到输出结果为200行504列的矩阵，每一行代表一只股票，每一列代表一个交易日。
# stock_day_change[0:1, :5]索引选区切片选择。选区第一只股票前五个交易日涨跌幅的方式。
# 0:2 代表第一只，第二只，0：5前五个交易日的涨跌幅数据

# 可以使用-1代表选取最后一个，即负数代表从后向前数
# -2:倒数第一只、第二只股票，-5：最后5个交易日的涨跌幅数据
stock_day_change[-2:,-5:]
# 以下代码交换上述两组股票交易日的切片数据，注意stock_day_change[0:2,0:5].copy()中的copy()的使用，如果这里不使用copy()的话，由于NumPy内部实现的机制全部是引用操作，所以当不使用copy()的时候得出的结果将会丢失stock_day_change[0:2, 0:5]
tmp = stock_day_change[0:2, 0:5].copy()
stock_day_change[0:2,0:5] = stock_day_change[-2:,-5:]
stock_day_change[-2:,-5:] = tmp

stock_day_change[0:2,0:5]
stock_day_change[-2:,-5:]



########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
################day6##################################day6##################################day6##################################day6##################
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################


# 3.1.4数据转换与规整
# 数据进行类型转换的目的，有些时候是为了规整数据，有些时候可以通过类型转化进一步得到有用的信息。以下代码使用astype(int)将涨跌幅转化为int结果，可以更清晰地发现涨跌幅数据两端的极限值
print(stock_day_change[0:2,0:5])
stock_day_change[0:2,0:5].astype(int)

# 如果只是想要规整float的数据。如保留两位小数，可使用np.around()函数，示列如下：
np.around(stock_day_change[0:2,0:5], 2)

# 很多时候需要处理的数据会有缺失，NumPy中nP.nan代表缺失，这里手工使切片中的第一个元素变na,代码如下：
# 使用copy()函数的目的是不修改原始序列
tmp_test = stock_day_change[0:2, 0:5].copy()
# 将第一个元素改成nan
tmp_test[0][0] = np.nan

# 下面使用np.nan_to_num()函数来用0来填充na，由于pandas中的dropna()和fillna()等方式更适合na处理，这里简单带过，示列如下
tmp_test = np.nan_to_num(tmp_test)
tmp_test


# 3.1.5逻辑条件进行数据筛选
# 找出切片内涨幅超过0.5的股票时段，通过输出结果可以看到返回的mask是bool的数组，示例如下：
mask = stock_day_change[0:2, 0:5] > 0.5
print(mask)

# mask的使用示例如下：
tmp_test = stock_day_change[0:2, 0:5].copy()
# 使用上述的mask数据筛选出符合条件的数组，即筛选mask中对应index值为true的
tmp_test[mask]

# 上述示例只为讲解过程，实际代码中一般会一行写完。比如下面的需求，找出tmp_test切片中>0.5的元素并且赋值为1，代码如下：
tmp_test[tmp_test > 0.5] = 1
tmp_test
# 针对多重筛选条件，使用|,&完成复合的逻辑筛选，注意需要使用括号将每一个条件括起来，否则会有错
tmp_test = stock_day_change[-2:,-5:]
print(tmp_test)
tmp_test[(tmp_test > 1) | (tmp_test < -1)]


# 3.1.6通过序列函数
# NumPy通过提供序列函数可以高效方便地处理序列：
# 1np.all()函数
# 判断stock_day_change[0:2,0:5]中是否全是上涨的
np.all(stock_day_change[0:2,0:5] > 0)

# 2np.any()函数
# np.any判断序列中是否有元素为true，即对布尔值序列进行或操作
np.any(stock_day_change[0:2,0:5] > 0)

# 3maximum()函数与minimum()函数
# 对两个序列对应的元素两两比较，maximum()结果集取大，相对使用maximum()为取小的结果集
np.maximum(stock_day_change[0:2,0:5], stock_day_change[-2:,-5:])

# 4np.unique()函数
change_int = stock_day_change[0:2,0:5].astype(int)
print(change_int)
# 数列中数值值唯一且不重复的值组成新的序列
np.unique(change_int)

# 5np.diff()
# Diff()执行的操作是前后两个临近数值进行减法运算。默认情况下axis=1, axis代表操作轴向
#axis=1
np.diff(stock_day_change[0:2,0:5])
# 下面同样使用diff()函数作用于相同序列，但axis=0，示列：
# 唯一区别axis=0 纵向操作
np.diff(stock_day_change[0:2,0:5], axis=0)


# 6np.where函数
# np.where函数在数据筛选、改造中有非常大的作用。
# np.where函数的语法句式有点类似Java中的三目运算法，。
tmp_test = stock_day_change[-2:,-5:]
print(np.where(tmp_test > 0.5, 1, 0))

print(np.where(tmp_test > 0.5, 1, tmp_test))

# 如果逻辑表达式为复合逻辑条件，则使用np.logical_and()和np.logical_or()函数，下面将序列中的值大于0.5并且小于1,否则赋值为0
np.where(np.logical_and(tmp_test > 0.5, tmp_test < 1), 1, 0)

# 3.1.7数据本地序列化操作
# 接下来通过np.save()函数可以轻松地将NumPy序列持久化保存。注意不需要添加后缀,save内部会自动生成.npy文件:
np.save('./gen/stock_day_change', stock_day_change)
# 读取只需要简单使用np.load()函数即可,但需要注意参数文件名要加上npy后缀,示例如下:
stock_day_change = np.load('./gen/stock_day_change.npy')
stock_day_change.shape


# 3.2基础统计概念与函数使用
# 量化中很多技术手段都是基于统计技术实现的,NumPy给python带来的不仅只是有序列并行化执行思想,更有统计学上很多方法的实现,比如期望np.mean(),方差np.var(),标准差np.std()等.
# 下面首先尝试以下NumPy中使用统计相关的函数.
# 用切片把序列切成只保留前4只股票,前4天的涨幅数据
stock_day_change_four = stock_day_change[:4,:4]
stock_day_change_four

# 3.2.1基础统计函数的使用
# 如果想知道stock_day_change的一些统计信息,比如横向地分析出某只股票在4天内统计信息,需要使用参数axis=1,举例如下
print('四天最大涨幅{}'.format(np.max(stock_day_change_four, axis=1)))

# 同理,下面分别是4天内的最大跌幅,振幅和平均涨跌数据
print('最大跌幅{}'.format(np.min(stock_day_change_four, axis=1)))
print('振幅幅度{}'.format(np.std(stock_day_change_four, axis=1)))
print('平均涨跌{}'.format(np.mean(stock_day_change_four, axis=1)))

# 如果想纵向地统计数据,即针对某一个交易日的4只股票进行统计分析,需要使用参数axis=0
print('股票在四天内最大涨幅{}'.format(np.max(stock_day_change_four, axis=0)))

# 从上面的输出可以看到,使用np.max()函数只能统计出某个交易日的最大涨幅,但是并不知道是哪一只股票,而使用np.argmax()函数即可以实现统计出哪一只股票在某个交易日的涨幅最大:
print('最大涨幅股票{}'.format(np.argmax(stock_day_change_four, axis=0)))
#输出: 最大涨幅股票[3 3 2 1]
# 意思是第一个交易日涨幅最大的为第4只股票,第二个交易日涨幅最大的为第4只股票,第三个交易日涨幅最大的为第3只股票,第四个工作日涨幅最大的为第2只股票


# 3.2.2基础统计概念
# 期望在概率论和统计学中,期望是试验中每次可能结果的概率乘以其结果的总和,反应一组数据平均取值的大小,用于表示分布中心位置
# 方差是衡量一组数据离散程度的度量,概率论中方差用于度量数据和其期望之间的离散程度,方差越大没说明数据越离散.
# 标准差为方差的算术平方根,标准差和变量的计算单位相同,所以比方差清晰.因此,很多时候在在分析时使用更多的是标准差

# 回到股市示例,如果有a,b两个交易者,他们多次交易平均战果都是赚100元,那么他们两人的期望都是100,但是a交易者获利的获利稳定性不好,假设振幅为50,即标准差为50,交易者b获利稳定性比a好,假设振幅为20,即标准差为20,示例:
# 离散函数
# loc均值,scale标准差
a_inverstor = np.random.normal(loc=100, scale=50, size=(100,1))
b_inverstor = np.random.normal(loc=100, scale=20, size=(100,1))
# 下面输出计算生成数据的标准差,方差及期望数据.

# a交易者
print('a交易者期望{0:.2f}元,标准差{1:.2f},方差{2:.2f}'.format(a_inverstor.mean(),a_inverstor.std(),a_inverstor.var()))
# b交易者
print('b交易者期望{0:.2f}元,标准差{1:.2f},方差{2:.2f}'.format(b_inverstor.mean(),b_inverstor.std(),b_inverstor.var()))

# 这里只生成100次交易数据,数据越多,月接近初始值
# 下面由可视化角度看以下a,b两个交易者的获利图
'''
-均值获利期望线
-均值获利期望线 + 获利标准差
-均值获利期望线 - 获利标准差
'''
# 为何标准差可以量化数据的振幅
# 标准差与方差是独立于期望的另一个对分布的度量,两个分布完全可能有相同的期望,而方差和标准差则不同

a_mean = a_inverstor.mean()
a_std = a_inverstor.std()
plt.plot(a_inverstor)

plt.axhline(a_mean + a_std, color='r')
plt.axhline(a_mean - a_std, color='g')


b_mean = b_inverstor.mean()
b_std = b_inverstor.std()
plt.plot(b_inverstor)

plt.axhline(b_mean + b_std, color='r')
plt.axhline(b_mean - b_std, color='g')


# 3.3.1正态分布基础概念
# 正态分布是常用的概率分布.正态分布有被称为高斯分布,因为高斯在1809年使用该分布来预测星体位置,正态曲线呈钟形,两头低,中间高,左右对称,因此又被称为钟形曲线.
# 正态分布曲线特点:
# -对于正态分布,数据的标准差越大,数据分布离散程度越大
# -对于正态分布,数据的期望位于曲线的对称轴中心.
stock_day_change = np.random.standard_normal((stock_cnt, view_day))

# 随机生成的第一只股票的涨跌数据,画出直方图
import scipy.stats as scs
# 均值期望
stock_mean = stock_day_change[0].mean()
# 标准差
stock_std = stock_day_change[0].std()

print('股票0 mean均值期望:{:.3f}'.format(stock_mean))
print('股票0 std标准差:{:.3f}'.format(stock_std))
# 绘制股票0的直方图
# bins柱子的数量
# density向量归一
plt.hist(stock_day_change[0], bins=50, density=True)
# linspace从股票0最小值->最大值生成数据
# def linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0):
fit_linspace = np.linspace(stock_day_change[0].min(),stock_day_change[0].max(),num=51)
# 概率密度函数(PDF, probability density function)
# 由均值,方差来描述曲线,使用scipy.stats.norm.pdf生成拟合曲线
pdf = scs.norm(stock_mean, stock_std).pdf(fit_linspace)
plt.plot(fit_linspace, pdf, lw=2, c='r')

# pdf函数在统计学中称为概率密度函数,是指在某个确定的取值点附近的可能性函数,将概率值分配给各个事件,得到事件的概率分布,让事件数值化,上面scs.norm返回pdf数值

# 统计套利中均值回复策略的理论依据为价格将围绕价值上下波动.与之类似,正态分布最大特点即为它的数据会围绕某个期望均值附近上下摆动,摆动幅度为数据的标准差.下面使用正态分布的这个特点做一个简单的量化小策略.

# 3.2.2 实例1正态分布买入策略
# 继续使用之前生成的200只股票504天的服从正态分布涨跌数据，保留后50天的随机数据作为策略验证数据，统计前454天中跌幅最大的3只股票，假设在第454天买入这3只股票。看结果
# np.sort()针对序列进行排序
# np.argsort()将展示排序的原序列号
# 保留50天的随机数据作为策略验证数据
keep_days = 50
# 统计前454天中的200只股票的涨跌数据，切片切出0-454day,view_days = 504
stock_day_change_test = stock_day_change[:stock_cnt, 0:view_day-keep_days]
# 打印出前454天中跌幅最大的3只股票，总跌幅通过np.sum()函数计算，np.sort()函数对结果排序
print(np.sort(np.sum(stock_day_change_test, axis=1))[:3])
# 使用np.argsort()函数针对股票跌幅进行排序，返回序号，即符合买入条件的股票序号
stock_lower_array = np.argsort(np.sum(stock_day_change_test, axis=1))[:3]
# 输出符合买入条件的股票序号
stock_lower_array

# 上面输出第一个序列中的元素分别代表3只跌幅最大的股票前454日总共下跌的幅度，可看到跌幅最大的股票下跌，和第二第三下跌的幅度，股票在NumPy对象stock_day_change中的序号
# 封装函数show_buy_lower()可视化选中的前三只跌幅最大的股票454日走势，以及从第454日买入后的趋势
def show_buy_lower(stock_ind):
    '''
    :param stock_ind:股票序号，即在stock_day_change中位置
    :return:
    '''
    # 设置一个一行两列的可视化图标
    _, axs = plt.subplots(nrows=1, ncols=2, figsize=(16,5))
    # view_days504 - keep_days50 = 454:view_days504
    # 绘制前454天开始到504天的股票走势,序列连续求和np.cumsum(), cumsum()函数[a,b,c,d].cumsum() = [a,a+b,a+b+c,a+b+c+d]
    axs[0].plot(np.arange(0, view_day - keep_days), stock_day_change_test[stock_ind].cumsum())
    # [view_day504 - keep_days50 = 454:view_day504]
    # 从第454天开始到504天的股票走势
    cs_buy = stock_day_change[stock_ind][view_day-keep_days:view_day].cumsum()
    # 绘制从第454天到504天中股票的走势图
    axs[1].plot(np.arange(view_day - keep_days, view_day), cs_buy)
    # 返回从第454天开始到504天计算盈亏的盈亏序列的最后一个值
    return cs_buy[-1]

# 假设等权重地买入3只股票
# 最后输出的盈亏比
profit = 0
# 遍历跌幅最大的3只股票序号序列
for stock_ind in stock_lower_array:
    # profit即3只股票从第454天买入开始计算，直到最后一天的盈亏比
    profit += show_buy_lower(stock_ind)
# str.format()支持{:.2f}形式保留两位小数
print('买入第{}只股票，从第454个交易日开始持有盈亏：{:.2f}%'.format(stock_lower_array, profit))

# 这个策略之所以可以盈利，是由于，通过np.random.standard_normal()建立的服从正态分布的涨跌数据，这样我们买入前454天中跌幅最大的3只股票的理论一句就是按照正态分布理论，这三只股票后期涨跌分布一定是涨的概率大于跌的概率



# 3.4伯努利分布
'''
3.4.1
伯努利分布是很简单的离散分布，随机变量只可能两个可能取值，即1和0，如果随机变量取值1的概率为p,那么0的概率为1-p
NumPy中使用numpy.random.binomial(1,p)来获取1的概率为p的前提下，生成随机变量，如果p=0.5，就类似抛硬币
'''

# 3.4.2
# 如何在交易中获取优势
# 实现函数casino()函数，假设有100个赌徒，每个赌徒都有1000000元，并且每个人都想在赌场玩1000万次，在不同胜率、赔率和手续费下casino()函数返回总体统计结果：
gamblers =100
def casino(win_rate, win_once=1, loss_once=1, commission=0.01):
    '''
    赌场：简单设定每个赌徒都有1000000元，并且每个赌徒都想玩10000000次，
    但是如果没钱了就别想玩了
    win_rate输赢的概率
    win_once每次赢钱数
    loss_once每次输钱数
    commission手续费这里简单设置为0.01 1%
    :return:
    '''
    my_money = 1000000
    play_cnt = 10000000
    commission = commission
    for _ in np.arange(0, play_cnt):
        w = np.random.binomial(1, win_rate)
        if w:
            my_money+= win_once
        else:
            my -= loss_once
        my_money -= commission
        if my_money <= 0:
            break
    return my_money



# 第四章
# 4.1基本操作方法
# 4.1.1DataFrame构建方法
import pandas as pd
# 以NumPy的200只股票，和504天为例子
stock_day_change = np.load('./gen/stock_day_change.npy')
stock_day_change.shape

# NumPy访问数据有缺陷，不容易
pd.DataFrame(stock_day_change).head()
pd.DataFrame(stock_day_change).tail()
pd.DataFrame(stock_day_change)[:5]

# 4.1.2索引行列序列
# 下面使用股票0，股票1为例
stock_symbols = ['股票'+str(x) for x in range(stock_day_change.shape[0])]
# 通过构造直接设置index参数，head(2)

'''
下面使用pd.date_range()函数生成一组连续的时间序列，使用生成的序列作为DataFrame的列索引，代表每一个交易日，通过columns参数传入时间序列初始化DataFrame对象。
'''
# 从2017-1-1向上时间递进，单位freg='1d'即1天
days = pd.date_range('2017-1-1', periods = stock_day_change.shape[1], freq='1d')
# 股票0 ->股票stock_day_change.shape[0]
stock_symbols = ['股票'+ str(x) for x in range(stock_day_change.shape[0])]
# 分别设置index和columns
df = pd.DataFrame(stock_day_change, index=stock_symbols, columns=days)
df.head(2)


# 4.1.3金融时间序列
'''
在量化分析中最常见的数据类型是金融时间序列，对于时间序列，pandas拥有非常丰富友好的方法来分析挖掘数据。下面的代码首先将数据df做个转置，得到行索引为时间，列索引为股票代码的金融时间序列。
'''
df = df.T
df.head()

'''
以下代码对df进行重新采样，以21天为周期，对21天内的时间平均来重新塑造数据。
'''
df_20 = df.resample('21D', how='mean')
df_20.head()

# 4.1.4Series构建及方法
'''
使用上面一个股票的时间序列数据，可以直接通过列索引df['股票0']得到股票0的时间顺序涨跌幅数据，通过type(df_stock0)来查看返回类型，发现返回的是Series类型：
'''
df_stock0 = df['股票0']

print(type(df_stock0))

df_stock0.head()

'''
Series是pandas中另一个非常重要的类，可以简单理解Series是只有一列数据的DataFrame对象，他们之间大多数函数都是可以通用的，使用方式也是和类似，比如上面使用head()函数打印出Series的前5行数据
'''

df_stock0.cumsum().plot()

'''
本质上pandas在基于分装NumPy的数据操作上还分装Matplotlib，起到了承上启下的重要作用。
'''


# 4.1.5重采样数据
'''
继续之前的resample()函数重采样话题，所有股票网站都提供了日K线，周K线，月K线等周期数据，但最原始的数据只是日K线数据。下面的代码通过重采样实现周K线，月K线的构建。刚刚构建使用how参数的值为’mean‘,下面的代码使用how='ohlc',它代表周期ohlc值，所以结果从一个列的Series变成了有4列数据的DataFrame
'''
df_stock0_5 = df_stock0.cumsum().resample('5D',how='ohlc')
df_stock0_20 = df_stock0.cumsum().resample('21D',how='ohlc')

from abupy import ABuMarketDrawing
ABuMarketDrawing.plot_candle_stick(df_stock0_5.index,df_stock0_5['open'].values,df_stock0_5['high'].values,df_stock0_5['low'].values,df_stock0_5['close'].values,np.random.random(len(df_stock0_5)),None,'stock',day_sum=False,html_bk=False,save=False)


# 4.2基本数据分析示例
'''
下面使用真正的股票数据构成DataFrame对象，继续学习pandas的使用，
首先取特斯拉电动车两件的股票数据
'''
from abu.abupy import ABuSymbolPd
# n_folds = 2年
tsla_df = ABuSymbolPd.make_kl_df('usTSLA', n_folds=2)
tsla_df.tail()

# 下面使用pandas的plot()函数展示TSLA在统计周期内的大致情况，注意只用一行代码就可以画出走势图
tsla_df[['close','volume']].plot(subplots=True, style=['r','g'], grid=True)

# pandas的DataFrame对象总览数据的函数info()的用途是查看数据是否缺失，以及各个子数据的数据类型
tsla_df.info()
# pandas的DataFrame对象总览数据的函数describe()的用途是，分别展示每组数据的统计信息
tsla_df.describe()

# 4.2.2索引选取和切片选择
# NumPy章节讲过使用索引选取序列和切片选择，pandas支持类似NumPy一样的操作，但也可以直接使用列名，行名称，甚至组合使用，特点是需要使用loc或者iloc声明方式。
# 使用loc配合行动名称，列名称选取切片示例如下：
tsla_df.loc['2017-07-23':'2017-07-31', 'open']
# 使用iloc配合行数值及列索引数值选取切片
# [1:5]:(1,2,3,4),[2,6]:(2,3,4,5)
tsla_df.iloc[1:5,2:6]
# 切取所有行
tsla_df.iloc[:,2:6]
# 切取所有列
tsla_df.iloc[35:37]

'''
混合使用方式，实际项目中使用最频繁的
'''
# 指定一个列
print(tsla_df.close[0:3])
# 通过组成一个列表选择多个列
tsla_df[['close','high','low']][0:3]


# 4.2.3逻辑条件进行数据筛选
# 句法结构与NumPy通过逻辑条件进行数据筛选，以下代码筛选出涨跌幅大于8%的交易数据。
# abs为取绝对值的意思，不是防抱死
tsla_df[np.abs(tsla_df.p_change)>8]

# 以下代码在筛选满足'涨跌幅大于8%的交易日'的条件基础上，增加条件'交易成交量大于统计周期内的平均值的2.5倍'，完成后筛选出的数据就是股票交易中常说的放量突破（当然可以有更复杂的定义）
tsla_df[(np.abs(tsla_df.p_change)>8) & (tsla_df.volume > 2.5*tsla_df.volume.mean())]



# 4.2.4数据转换与规整
# 1.数据序列值排序
# 以下代码对涨跌幅进行排序
tsla_df.sort_index(by='p_change')[:5]

# 降序排列
tsla_df.sort_index(by='p_change', ascending=False)

# 2.缺失数据处理
# pandas在对缺失数据的处理上接口友好程度相对NumPy大幅提升
# 如果一行数据中存在na就删除这一行
tsla_df.dropna()
# 通过how控制，如果一行的数据中全部都是na就删除行
tsla_df.dropna(how='all')
# 使用指定值填充na，inplace代表就地操作，即不返回新的序列在原始序列上修改,就是覆盖原来数据
tsla_df.fillna(tsla_df.mean(), inplace=True)

# 3.数据转化处理
# pct_change()函数对序列从第二项开始向前做减法后再除以前一项，这个操作在股票量化等领域经常使用，因为pct_change()针对价格序列的操作结果即是涨跌幅序列。即pct_change（a,b,c）= (na, b-a/a, c-b/b)
tsla_df.close[:3]

tsla_df.close.pct_change()[:3]

# round函数使用如下
change_ratio = tsla_df.p_change
np.round(change_ratio[-5:] * 100, 2)

# 下面使用Series对象的map(0函数针对列数据atr21，来实现同样的功能。
format = lambda x: '%.2f'%x
tsla_df.atr21.map(format).tail()

# 4.2.5数据本地序列化操作
# pandas的I/O操作API的最主要格式有CSV,SQL,XLS,JSON,HDF5针对量化领域最常使用的是CSV格式和HDF5格式。下面展示CSV使用，abu使用的是HDF5


# 使用to_csv保存dataframe对象，columns列名称
tsla_df.to_csv('./gen/tsla_df.csv', columns=tsla_df.columns, index=True)

# 使用read_csv读取
tsla_df_load = pd.read_csv('./gen/tsla_df.csv', parse_date = True, index_col=0)

# 查看从文件中重新读取dataframe对象
tsla_df_load.tail()


# 4.3实例1：寻找股票异动涨跌幅阀值
# 美股交易没有涨停、跌停的概念，全靠市场自己调节。这样的话公司市值及流通性对涨跌幅有着至关重要的意义，对于谷歌等市值高，流动性好的公司，也许3%~5%的振幅已经很高了；但对于很多市值小，流通性不好的股票，也许每天5%以上的振幅是一种常态。如果把涨跌数据分类成10份，Top10%振幅的就认为是异常表现的振幅，我们的需求是鉴定TSLA的异常振幅阀值是多少。
# 下面首先通过直方图hist，对tsla_df.p_change有个感性的认识。
tsla_df.p_change.hist(bins=80)
# x坐标代表分散成80等份的区间  y坐标代表分散成80等份的区间划分下的个数
# 使用qcut()函数将涨跌幅数据进行平均分类，这里分为10份，value_counts()函数经常和qcut()函数一起使用，便于更直观地显示分离结果。
# value_counts()的使用需要记住，只有Series对象才有value_counts()方法。

cats = pd.qcut(np.abs(tsla_df.p_change), 10)
cats.value_counts()


# 4.3.1数据离散化
# 前面的pd.qcut()将数据平均分为若干份，如果交易者有自己的分类准则，那么应该使用pd.cut()传入bins
# 将涨跌幅数据手工分类，从负无穷到-7,-5,-3,0,3,5,7,正无穷
bins = [-np.inf, -7.0, -5, -3, 0, 3, 5, 7, np.inf]
cats = pd.cut(tsla_df.p_change, bins)
cats.value_counts()
# pd.cut()函数经常会和pd.get_dummies()函数配合使用，将数据由连续数值类型变成离散类型，即将数据离散化，get_dummies()操作后生成哑变量矩阵
# cr_dummies为列名称前缀
change_ration_dummies = pd.get_dummies(cats, prefix='cr_dummies')
change_ration_dummies.tail()


y = np.random.randn(10000,1)
x = list(range(-4,4,1))
n = plt.hist(y,x)
# 统计Y在X这个区间划分下的个数


# 4.3.2concat,append,merge的使用
# 如果我们把上面得到的change_ration_dummies表格与tsla_df进行合并，那么最简单的方式是直接使用concat()函数
pd.concat([tsla_df, change_ration_dummies], axis=1).tail()#列数据对应
# 上述concat()函数是在axis=1,即纵向上的连续数据，如果横轴上的连续收据，同样可使用concat axis=0，但是更加简单的方式是直接使用append()函数
# pd.concat()函数的连续axis=0,纵向连接atr>14的df和p_change>10的df
pd.concat([tsla_df[tsla_df.p_change > 10],tsla_df[tsla_df.atr21 > 16]], axis = 0)
tsla_df[tsla_df.p_change > 10].append(tsla_df[tsla_df.atr21>16])
# 用于pandas数据连结归并除上述pd.concat()和append()外，还会使用到pd.merge()函数，他的使用最复杂，参数组合组多，但也是灵活性最强的方式。特别是针对多个不同key的序列，但由于量化分析一般需要处理的都是时间序列
stock_a = pd.DataFrame({'stock_a':['a','b','c','d','a'],'data':range(5)})
stock_b = pd.DataFrame({'stock_b':['a','b','c'],'data2':range(3)})
pd.merge(stock_a,stock_b,left_on='stock_a',right_on='stock_b')

# 4.4实例2：星期几是这个股票的好日子
# 下面实例展示就是分析TSLA的数据,从数据中发现周几是TSLA的'好日子'
# tsla_df数据中date_week字段代表周几，首先使用np.where()为DataFrame对象添加一列新数据positive，代表交易日当天股票上涨还是下跌
tsla_df['positive'] = np.where(tsla_df.p_change > 0, 1, 0)
tsla_df.tail()

# 4.4.1构建交叉表
# 使用pd.crosstab()构建一个交叉表，行使用data_week信息，列使用positive
'''
交叉表的：集合周几的positive的数量
'''
xxt = pd.crosstab(tsla_df.date_week, tsla_df.positive)
xt = pd.crosstab(tsla_df.positive, tsla_df.date_week)
xxt
# 下面的代码是经常和pd.crosstab()配套出现的代码，
xt_pct=xxt.div(xxt.sum(1).astype(float), axis=0)

xt_pct.plot(figsize=(8,5),kind='bar',stacked=True,title='date_week -> positive')
plt.xlabel('date_week')
plt.ylabel('positive')


# 4.4.2构建透视表
'''
前面的操作可以用更简单的工具pivot_table()（透视表）求出结果
'''
tsla_df.pivot_table(['positive'], index=['date_week'])
# 如下代码所示，和crosstab(),pivot_table()有着类似功能的是groupby()函数，函数操作更加底层，句法也更难理解，但是可以解决的问题也更加全面。对于pandaas，首先学会使用crosstab()和pivot_table()函数，遇到这类问题一般都可以通过他们来解决。
tsla_df.groupby(['date_week','positive'])['positive'].count()

# 4.5实例3：跳空缺口
# 跳空缺口是指股价开盘价高于昨天的最高价或低于昨天的最低价，使K线图出现空挡的现象。
'''
普通缺口：特点就是很快被回补，价格在几天内就会回补
突破缺口：当价格或成交量伴随跳空（向上或者向下）跳出震荡区，则预示着新趋势的形式
衰竭缺口：缺口没有很快回补，走势也反复无常，最终慢慢地回补缺口，预示着市场走势将可能有剧烈的反转
'''
# 下面根据上面描述的理论来寻找TSLA电动车的跳空缺口，但并不是使用传统的跳空定义方式，因为这种方式很容易夹杂普通缺口，这列定义缺口的方式如下。
# 今天如果是上涨缺失，那么跳空的确定需要今天的最低价格大于昨天收盘价格一个阀值以上，确定为跳空
# 今天如果是下跌，那么跳空的确定需要昨天的收盘价大于今天的最高价格一个阀值以上，确定向下跳空
# 这种方式确定的跳空缺口存在很强的支撑或者阻力，首先确定跳空阀值，这里的计算方式是使用统计周期内收盘价格的中位数的3%：
jump_threshold = tsla_df.close.median() * 0.03
jump_threshold

# 接下来使用for循环遍历每一个交易日，按照上面描述的确定跳空方式来寻找跳空缺口。这里新建了一张表格来存储跳空数据jump_pd
# jump代表跳空方向，方便之后的数据处理
# jump_power代表跳空的能量，这里的能量计算是由缺口的高度除以阀值获得，能量再次量化了支撑或者阻力的大小
jump_pd = pd.DataFrame()
def judge_jump(today):
    global jump_pd
    if today.p_change > 0 and (today.low - today.pre_close) > jump_threshold:
        '''
        符合向上跳空
        '''
        # jump记录方向1向上
        today['jump'] = 1
        # 向上跳能量=（今天最低-昨收）/跳空阀值
        today['jump_power'] = (today.low - today.pre_close)/jump_threshold
        jump_pd = jump_pd.append(today)
    elif today.p_change < 0 and (today.pre_close - today.high) > jump_threshold:
        '''
        符合向下跳空
        '''
        # jump记录方向 -1向下
        today['jump'] = -1
        # 向下跳能量 = （昨收 - 今天最高）/跳空阀值
        today['jump_power'] = (today.pre_close - today.high)/jump_threshold
        jump_pd = jump_pd.append(today)

for kl_index in np.arange(0, tsla_df.shape[0]):
    # 通过ix一个一个拿
    today = tsla_df.ix[kl_index]
    judge_jump(today)
#filter 按照顺序只显示这些列
jump_pd.filter(['jump','jump_power','close','date','p_change','pre_close'])

'''
输出结果jump_pd为符合跳空筛选的交易日，注意观察jump_power可以发现，跳空能量呃涨跌幅值成正比。
上面实现的代码虽然可以正常运行，输出结果也没有问题，但是pandas对象中有另一种优雅的方式针对上面的for循环优化写法和效率，即使用apply()函数。该函数接受一个处理函数作为参数，处理函数默认只有一个参数也就是行或列数据，通过axis参数确定是行还是列，如果处理函数需要另外的参数配合，可以通过args参数，它接受一个tuple来扩展。使用apply()代替上述for循环实现方式如下:
'''
jump_pd = pd.DataFrame()
# axis=1即行数据，tsla_df的每一条行数据即为每一个交易日数据
tsla_df.apply(judge_jump, axis=1)
'''
上面使用apply函数筛选出的jump_pd与for循环的结果是一致的
'''
# 以下代码使用ABuMarketDrawing将走势和选取的跳空缺口一起画出并标示
from abu.abupy import ABuMarketDrawing
# view_idnexs传入jump_pd.index,即在K线图上使用圆圈来标示跳空点
ABuMarketDrawing.plot_candle_form_klpd(tsla_df, view_indexs=jump_pd.index)


# 4.6pandas 三维面板的使用
# pandas最常用的对象：Series（一维带索引的序列数据）DataFrame（二维矩阵，由行索引，列索引和数据矩阵组成）
'''
对于更高维度的数据，由于多个纬度理解难度将呈几何级数增长，可视化不方便等问题，实际工程中的用途并不广泛，但有些情况下使用高维数据结构也会带来高效和灵活度的提升。
'''
# 使用abu量化系统的
from abu.abupy import ABuIndustries
r_symbol = 'usTSLA'
# 这里获取了和TSLA点动成处于同意行业的股票，组成pandas三维面板panel数据
p_date, _ = ABuIndustries.get_industries_panel_from_target(r_symbol, show=False)
# 通过type()函数来看一下p_date的类型
type(p_date)
# <class 'pandas.core.panel.Panel'>
# Dimensions: 7 (items) x 380 (major_axis) x 12 (minor_axis)
# Items axis: usF to usTTM
# Major_axis axis: 2017-06-28 00:00:00 to 2018-12-31 00:00:00
# Minor_axis axis: close to atr14
p_date['usTTM'].head()
# 高维的Panel通过轴向的转换等空间操作，可以高效灵活地变幻出各种数据形式
'''
Panel的swapaxes()方法指定交互items,minor轴向的空间位置，转换后的结果显示三维面板Panel由原来的7 (items) x 380 (major_axis) x 12 (minor_axis)变成12*380*7的数据结构
'''
p_data_it = p_date.swapaxes('items','minor')

'''
通过拿出item axis 中的close来选取所有股票的close，形成一个新的横切面数据
'''
p_data_it_close = p_data_it['close'].dropna(axis=0)
p_data_it_close

'''
将所有股票的close数据序列化标准化后可视化
'''
from abu.abupy import ABuScalerUtil
# scaler_std将所有close的切面数据做标准化，为了可视化在同一范围
p_data_it_close = ABuScalerUtil.scaler_std(p_data_it_close)
p_data_it_close.plot()
plt.legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)
plt.ylabel('Price')
plt.xlabel('Time')


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
################5##################################5##################################5##################################5##################
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

# Matplotlib是python上最基础也最常用的可视化工具
import matplotlib.pyplot as plt
from abu.abupy import ABuSymbolPd
tsla_df = ABuSymbolPd.make_kl_df('usTSLA', n_folds=2)
tsla_df.tail()

'''
plt.plot()是最简单也是最常用的绘图方式，可以通过pandas的Series直接作为参数进行绘制，也可以通过NumPy对象，甚至Python的list对象它都是支持的。
'''
def plot_demo(axs=None, just_series=False):
    '''
    绘制tsla的收盘价曲线
    :param axs: 子画布
    :param just_series: 是否绘制一条收盘曲线使用Series
    :return:
    '''
    # 如果参数传入子画布则使用子画布绘制
    drawer = plt if axs is None else axs
    drawer.plot(tsla_df.close, c='r')
    if not just_series:
        # 为了使曲线不重叠，y变量加了10哥单位tsla_df.close.values + 10
        # numpy对象tsla_df.close.index + tsla_df.close.values, 绿色
        drawer.plot(tsla_df.close.index, tsla_df.close.values + 10, c='g')
        # 为了使曲线不重叠，y变量加了20个单位
        # list对象，Numpy.tolist()将Numpy对象转换为list对象，蓝色
        drawer.plot(tsla_df.close.index.tolist(),(tsla_df.close.values + 20).tolist(), c='b')
    plt.xlabel('time')
    plt.ylabel('close')
    plt.title('TSLA  CLOSE')
    plt.grid(True)#是否显示网格
plot_demo()

# 5.1.2matplotlib子画布及loc使用
# matplotlib使用legend()函数操作标注,参数loc代表标注位置。下面代码通过生成多个子画布使用不同的loc值来示例标注及loc的使用
_,axs = plt.subplots(nrows=2, ncols=2, figsize=(14,10))
# 画布0,loc：0 plot_demo中传入画布，则使用传入的画布绘制
drawer = axs[0][0]
plot_demo(drawer)
drawer.legend(['Series', 'Numpy', 'List'], loc = 0)
# 画布1,loc：1 plot_demo中传入画布，则使用传入的画布绘制
drawer = axs[0][1]
plot_demo(drawer)
drawer.legend(['Series', 'Numpy', 'List'], loc = 1)
# 画布2,loc：2 plot_demo中传入画布，则使用传入的画布绘制
drawer = axs[1][0]
plot_demo(drawer)
drawer.legend(['Series', 'Numpy', 'List'], loc = 2)
# 画布3,loc：3 plot_demo中传入画布，则使用传入的画布绘制
drawer = axs[1][1]
plot_demo(drawer)
drawer.legend(['Series', 'Numpy', 'List'], bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)

'''
上述代码使用plt.subplot()函数生成多个子画布，返回的axs是NumPy类型，参数nrows和ncols分别代表x和y轴的shape值，所以plt.subplots(nrows=2, ncols=2, figsize=(14,10))实际会生成一个2*2（两行两列的）NumPy对象axs.在之前plot_demo()函数的基础上使用legend()函数对绘制进行标注，这里loc使用 不同的值，将导致标注的位置发生变化，axs[1][1]演示使用bbox_to_anchor将标注绘制在画布的外面。如果loc无特殊需求，一般使用loc='best'简单指定，即自动选择最优的位置进行标注绘制
'''

# 5.1.3K线图的绘制
# Matplotlib对绘制K线图有直接的函数封装，所以使用Matplotlib绘制K线图非常简单。绘制K线图主要的工作就是制作一个qutotes
# qutotes里每个数据是一根蜡烛，绘制标准K线图使用matplotlib.finance.candlestick_ochl()函数，函数后缀的ochl。另外还有matplotlib.finance.candlestick2_ohlc()函数，后缀ohlc的意思是按照顺序组织数据加入到quotes中。

import matplotlib.finance as mpf
__colorup__ = 'red'
__colordown__ = 'green'
# 为了示例清晰，只拿出前30天的交易数据绘制蜡烛图
tsla_part_df = tsla_df[:100]
fig, ax = plt.subplots(figsize=(14,7))
qutotes = []
for index, (d,o,c,h,l) in enumerate(zip(tsla_part_df.index, tsla_part_df.open, tsla_part_df.close, tsla_part_df.high, tsla_part_df.low)):
    # 蜡烛图的日期要使用matplotlib.finance.date2num进行转换为特有的数字值
    d = mpf.date2num(d)
    # 日期，开盘，收盘，最高，最低组成tuple对象val
    val = (d,o,c,h,l)
    # 将val加入qutotes
    qutotes.append(val)
# 使用mpf.candlestick_ochl进行蜡烛绘制，ochl代表：open,close,high,low
mpf.candlestick_ochl(ax, qutotes, width=0.6, colorup=__colorup__, colordown=__colordown__)
ax.autoscale_view()
ax.xaxis_date()

# 5.2使用Bokeh交互可视化
# 有些时候将一段数据可视化后与偶交互操作的需求。当绘制蜡烛图数量比较多的时候，可能有平移，放大某一时段等交互需求，Python实现这些交互需求解决方案一般通过网页形式的可视化，配合javascript与网页完成交互。
# Bokeh是一门专门针对Web浏览器实现呈现功能的交互式可视化Python库，具体使用示例
#
import pandas as pd
import numpy as np
from abu.abupy import ABuMarketDrawing
ABuMarketDrawing.plot_candle_form_klpd(tsla_df, html_bk=True)

tsla_df.index.datetime()

pd.to_datetime(tsla_df.index)

# 5.3使用pandas可视化数据
# pandas封装了Matplotlib，使用Matplotlib可以实现的绘制可视化都可以使用pandas用更简单的方式实现。由于pandas是为了金融量化而生的库，包含很多金融量化接口，所以pandas直接可视化金融数据非常简单。
# 5.3.1绘制股票的收益及收益波动情况
'''
计算收益波动一般会使用pd.rolling_std()函数和rolling_std()函数，简单使用示例如下
'''
# 示列序列
demo_list = np.array([2,4,16,20])
df = pd.DataFrame(demo_list)
# 以3天为周期计算波动
demo_window = 3
# pd.rolling_std * np.sqrt

#pd.rolling_std(demo_list, window=demo_window, center=False) * np.sqrt(demo_window) 无效方法

df.rolling(window=demo_window,center=False).std() * np.sqrt(demo_window)
# rolling.std 函数的意思是根据参数demo_window的大小，从原始序列依次取出demo_window个元素做std()操作标准差（），波动即等于每次取出子序列std（）之后的结果乘以demon_window开方值

# 上述代码之所以使用np.sqrt()函数开平方demo_window天数，是因为std()函数的计算本是方差开方，如果使用var()函数计算就可以直接使用天数:
np.sqrt(pd.Series([2,4,16]).var() * demo_window)

# 接下来使用np.log()函数计算投资收益，使用pd.rolling_std()函数计算每20个交易日的移动收益标准差，使用pd.ewmstd()函数，计算每20个交易日的加权移动收益标准差，最后绘制各组数据
tsla_df_copy = tsla_df.copy()
# 投资回报
tsla_df_copy['return'] = np.log(tsla_df['close']/tsla_df['close'].shift(1))
# 移动收益标准差
tsla_df_copy['mov_std'] = tsla_df_copy['return'].rolling(window=20,center=False).std()*np.sqrt(20)
# 加权移动收益标准差与移动收益标准差基本相同，只不过前者根据时间权重计算std
# tsla_df_copy['std_ewm'] = pd.ewmstd(tsla_df_copy['return'],span=20,min_periods=20,adjust=True)*np.sqrt(20)
tsla_df_copy['std_ewm'] = tsla_df_copy['return'].ewm(span=20,min_periods=20,adjust=True).std()*np.sqrt(20)  # pd.ewmstd(tsla_df_copy['return'],span=20,min_periods=20,adjust=True)*np.sqrt(20)

tsla_df_copy[['close','mov_std','std_ewm','return']].plot(subplots=True, grid=True)

# 5.3.2绘制股票的价格和均线
# 以下代码绘制股票的价格30日均线，60日均线，90日均线
import matplotlib.pyplot as plt
tsla_df.close.plot()
#ma 30
tsla_df.close.rolling(window=30).mean().plot()
#ma 60
tsla_df.close.rolling(window=60).mean().plot()
#ma 90
tsla_df.close.rolling(window=90).mean().plot()
# loc='best'即自动寻找适合的位置
plt.legend(['close','30 mv','60 mv','90 mv'], loc='best')

# 5.3.3其他pandas统计图形种类
# pandas通过plot（）函数传入kind参数支持绘制其他图形
# kind参数
'''
line
bar
barh：横向柱状图
hist
kde:绘制密度曲线
density：同kde
pie：饼图
'''
# 股票中有个概念叫低开高收
'''
iloc获取所有低开高走的下一个交易日组成low_to_high_df，由于是下一个交易日所以要对满足条件的交易日再次通过iloc获取，下一个交易日index用key.values +1 ，key序列的值即为0-len(tsla_df),即为交易日index。
'''
low_to_high_df = tsla_df.iloc[tsla_df[(tsla_df.close > tsla_df.open) & (tsla_df.key!= tsla_df.shape[0]-1)].key.values + 1]

# 通过where将下一个交易日的涨跌幅通过ceil和floor向上及向下取整
change_ceil_floor = np.where(low_to_high_df['p_change'] > 0,np.ceil(low_to_high_df['p_change']),np.floor(low_to_high_df['p_change']))
# 使用pd.Series包裹，方便之后绘制
change_ceil_floor = pd.Series(change_ceil_floor)
'''
(tsla_df.close > tsla_df.open)&(tsla_df.key<>tsla_df.shape[0]-1)设置条件收盘价格大于开盘，且不是数据中最后一个交易日
使用iloc选取低开高收的下一个交易日行数据
np.ceil()函数将数据向上取整
np.floor()函数向下取整
使用np.where()函数将涨跌>0的值使用ceil取整数，将涨跌<0的值使用floor取整数，不使用astype(int)的目的是不想取0值，否则+0.4和-0.4这种数都会变成0，即丢失了涨跌方向信息
将np.where()函数返回Numpy数据使用pd.Series包裹，方便绘制
'''
# 下面使用subplot()函数生成子画布，plot()函数通过传入ax在不同画布上使用不同kind参数。通过可视化可以看出：在统计周期tsla低开高收的下一个交易日下跌的情况比上涨的情况还要多，而且比较明显。下面代码量化了下跌的Sum与上涨的Sum

print('低开高收的下一个交易日所有下跌的跌幅取整和Sum：' + str(change_ceil_floor[change_ceil_floor < 0].sum()))
print('低开高收的下一个交易日所有上涨的涨幅取整和Sum：' + str(change_ceil_floor[change_ceil_floor > 0].sum()))

_,axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
# 柱状图
change_ceil_floor.value_counts().plot(kind='bar', ax=axs[0][0])
# 水平柱状图
change_ceil_floor.value_counts().plot(kind='barh',ax=axs[0][1])
# 概率密度图
change_ceil_floor.value_counts().plot(kind='kde', ax=axs[1][0])
# 圆饼图
change_ceil_floor.value_counts().plot(kind='pie', ax=axs[1][1])

# 5.4 使用Seaborn可视化数据
# Seaborn是Matplotlib分装的更高级api，从而作图更加容易
import seaborn as sns
# 通过一行代码将直方图以及密度图一起绘制
sns.distplot(tsla_df['p_change'], bins=80)

# 针对pandas的DataFrame数据，使用列名称定轴绘制箱型图,tsla_df中date_week代表星期几，使用date_week作为x轴，p_change涨跌幅数据作为y轴，使用boxplot()函数绘制箱型图来可视化振幅最大（即p_change普遍偏大）周四箱体最矮，即tsla周四相对股票振幅最小（即p_change普遍偏小）

sns.boxplot(x='date_week',y='p_change',data=tsla_df)

# 通过sns.jointplot()函数，可视化两组数据的相关性即概率密度分布
sns.jointplot(tsla_df['high'], tsla_df['low'])

# 通过sns.heatmap绘制相关热力图
# 下面代码使用pd.DataFrame.join()函数的p_change涨跌幅数据接起来组成一个新的DataFrame
change_df = pd.DataFrame({'tsla':tsla_df.p_change})
#join usGOOG
change_df = change_df.join(pd.DataFrame({'goog':ABuSymbolPd.make_kl_df('usGOOG',n_folds=2).p_change}), how='outer')
# join usAAPL
change_df = change_df.join(pd.DataFrame({'aapl':ABuSymbolPd.make_kl_df('usAAPL',n_folds=2).p_change}), how='outer')
# join usFB
change_df = change_df.join(pd.DataFrame({'fb':ABuSymbolPd.make_kl_df('usFB',n_folds=2).p_change}), how='outer')
# join usBIDU
change_df = change_df.join(pd.DataFrame({'bidu':ABuSymbolPd.make_kl_df('usBIDU',n_folds=2).p_change}), how='outer')

change_df = change_df.dropna()
change_df.head()

# 下面使用pd.DataFrame.corr()函数计算每组数据的协方差，使用热力图展示每组股票涨跌幅的相关性

corr = change_df.corr()
_,ax = plt.subplots(figsize=(8,5))
sns.heatmap(corr, ax=ax)

# 5.5实例1：可视化量化策略的交易区间及卖出原因
# 假定我们运行一个量化策略，执行回测。我们的需求就是在收盘价格时间序列的基础上标明上面这个持有区间
# 封装函数plot_trade()实现上述需求，使用plt.fill_between()函数填充标注持有区间
def plot_trade(buy_date,sell_date):
    # 找出2014-07-28对应时间序列中的index作为start
    start = tsla_df[tsla_df.index == buy_date].key.values[0]
    # 找出2014-09-05对应时间序列中的index作为end
    end = tsla_df[tsla_df.index == sell_date].key.values[0]
    plot_demo(just_series=True)
    plt.fill_between(tsla_df.index, 0, tsla_df['close'], color='blue', alpha=.08)
    # 标注股票持有周期为绿色，使用start和end切片周期
    plt.fill_between(tsla_df.index[start:end],0,tsla_df['close'][start:end], color='green', alpha=.38)
    # 设置y轴的显示范围，如果不设置ylim，将从0开始最为起点显示，效果不好
    plt.ylim(np.min(tsla_df['close'])-5, np.max(tsla_df['close'])+5)
    # 使用loc='best'
    plt.legend(['close'], loc='best')
    # 标注交易区间
plot_trade('2017-07-28','2017-09-05')


# ....
# 5.8.1MACD指标的可视化
# Python中计算技术指标一般通过TA-Lib提供的各种接口，如RSI只需要简单调用talib.RSI()函数，OBV需要调用talib.OBV()函数，我们只要传入对应的参数就行。
'''
MACD称为指数平滑异动移动平均线，是从双指数移动平均线发展而来，由快的指数移动平均线(EMA12)减去慢的指数移动平均线（EMA26）得到快线DIF，再用2*（快线DIF-DIF的9日加权移动均线DEA）得到MACD柱。
MACD的意义和双移动平均线基本相同，即由快，慢均线的离散，聚合形态，表征当前的多空状态和股价可能的发展变化趋势，但阅读起来更方便。
当MACD从负数转向正数时，是买入的信号，当MACD从正数转向负数时，是卖出的信号。当MACD以大角度变化时，表示快的移动平均线和慢的移动平均线的差距非常迅速地拉开，代表了一个市场大趋势的转变。


安装ta-lib方法 
windows：先下载安装包，然后运行Native Tools Command Prompt安装
Move to C:\ta-lib\c\make\cdr\win32\msvc
Build the Library nmake
'''
import matplotlib.pyplot as plt
import numpy as np
import talib

kl_index = tsla_df.index
#talib.MACD:注意参数序列必是NumPy序列，所以不能是tsla_df.close
dif, dea, bar = talib.MACD(tsla_df.close.values, fastperiod=12, slowperiod=26, signalperiod=9)
plt.plot(kl_index, dif, label='macd dif')
plt.plot(kl_index, dea, label='signal dea')
bar_red = np.where(bar > 0, bar, 0)
bar_green = np.where(bar < 0, bar, 0)
# 绘制bar>0的柱状图
plt.bar(kl_index, bar_red, facecolor='red', label='hist bar')
# 绘制bar<0的柱状图
plt.bar(kl_index, bar_green, facecolor='green', label='hist bar')
plt.legend(loc='best')
