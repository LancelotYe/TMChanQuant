
###################2019/6/8###################################
price_str = '30.14, 29.58, 26.36, 32.56, 32.82'
price_array = price_str.split(',')
data_base = 20170118

data_array = [str(data_base + ind) for ind , _ in enumerate(price_array)]

data_array


stock_tuple_list = [(data, price) for data, price in zip(data_array, price_array)]
print('20170119日的价格:{}'.format(stock_tuple_list[1][1]))

from collections import namedtuple

stock_namedtuple = namedtuple = namedtuple('stock',('date', 'price'))
stock_namedtuple_list = [stock_namedtuple(date, price) for date , price in zip(data_array, price_array)]

stock_dict = {date:price for date, price in zip(data_array, price_array)}


from collections import OrderedDict
stock_dict = OrderedDict((date , price) for date, price in zip(data_array, price_array))
stock_dict.keys()

min(stock_dict)

min(zip(stock_dict.values(), stock_dict.keys()))

def find_second_max(dict_array):
    stock_prices_sorted = sorted(zip(dict_array.values(), dict_array.keys()))
    return stock_prices_sorted[-2]

if callable(find_second_max):
    print(find_second_max(stock_dict))

find_second_max_lamdba = lambda dict_array:sorted(zip(dict_array.values(), dict_array.keys()))[-2]

find_second_max_lamdba(stock_dict)

def find_max_and_min(dict_array):
    stock_prices_sorted = sorted(zip(dict_array.values(), dict_array.keys()))
    return stock_prices_sorted[0], stock_prices_sorted[-1]

find_max_and_min(stock_dict)

price_float_array = [float(price_str) for price_str in  stock_dict.values()]
pp_array = [(price1 , price2) for price1, price2 in zip(price_float_array[:-1], price_float_array[1:])]

from functools import reduce
change_array = map(
    lambda pp : reduce(lambda a, b : round((b-1)/a , 3) , pp),
    pp_array
)
change_array = list(change_array)
change_array.insert(0, 1)
change_array