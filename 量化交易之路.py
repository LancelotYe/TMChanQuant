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