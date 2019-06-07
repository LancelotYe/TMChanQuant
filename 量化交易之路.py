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
change_array.insert(0, 0)
change_array

#reduce(lambda a, b: round((b - a) / a, 3), (30.14, 29.58))
# 分解函数
# round函数的作用是，保留小数点后三位round（x, 3）
# map函数的作用，元祖组成的数组，将每个元祖拿出来使用作为reduce函数的参数
# reduce函数的作用，传入数组参数与lambda的结合使用假设lambda是f（x,y）,传入的pp=[1,2,3,4,5],reduce(lambda x, y: f(x,y), [1,2,3,4,5])=f(f(f(f(f(1),2),3),4),5)