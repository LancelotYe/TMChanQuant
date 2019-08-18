# 实例1：均值回复策略
'''
以下代码实现一个简单的均值回复策略，首先分割训练测试集
'''
from abu.abupy import ABuSymbolPd
import matplotlib.pyplot as plot
import pandas as pd
import numpy as np
kl_pd = ABuSymbolPd.make_kl_df('usTSLA', n_folds=2)
# 头一年([:252])作为训练数据，美股交易中一年的交易日有252天
train_kl = kl_pd[:252]
# 后一年作为回测数据
test_kl = kl_pd[-252:]
# 分别画出两部分数据的收盘价格曲线
train = train_kl.close.values
test = test_kl.close.values
array = np.array([train, test])
tmp_df = pd.DataFrame(
    array.T,
    columns = ['train', 'test']
)

tmp_df[['train', 'test']].plot(subplots=True, grid=True, figsize=(14,7))

'''
总体思路如下：
1.将两年收盘价格分开，一年收盘价格作为训练数据，另一年的收盘价作为回归测试数据
2.训练数据通过收盘价格的均值和标准差构造买入信号和卖出信号
3.将训练数据计算出信号带入回归测试数据，对比策略收益结果和基准收益结果
'''
# 开始构造买入信号
# 训练数据的收盘价格均值
close_mean = train_kl.close.mean()
# 训练数据的收盘价格标准差
close_std = train_kl.close.std()

# 构造卖出信号阀值
sell_signal = close_mean + close_std/3
# 构造买入阀值
buy_signal = close_mean - close_std/3

# 可视化训练数据的卖出信号阀值，买入信号阀值及均值线
plot.figure(figsize=(14,7))
# 训练集收盘价格可视化
train_kl.close.plot()
# 水平线，买入信号，1w代表线的粗度
plot.axhline(buy_signal, color = 'r', lw = 3)
plot.axhline(close_mean, color = 'black', lw = 1)
plot.axhline(sell_signal, color = 'g', lw = 3)
plot.legend(['train_close','buy_signal','close_mean','sell_signal'], loc='best')
plot.show()


plot.figure(figsize=(14,7))
# 测试数据可视化
test_kl.close.plot()
# buy_signal直接带入买入信号
plot.axhline(buy_signal, color='r',lw=3)
plot.axhline(close_mean, color = 'black', lw = 1)
plot.axhline(sell_signal, color = 'g', lw = 3)
plot.legend(['train_close','buy_signal','close_mean','sell_signal'], loc='best')
plot.show()

'''
接下来
通过买入信号操作
'''
buy_index = test_kl[test_kl['close'] <= buy_signal].index
test_kl.loc[buy_index, 'signal']= 1
test_kl[52:57]


sell_index = test_kl[test_kl['close'] >= sell_signal].index
test_kl.loc[sell_index,'signal'] = 0
test_kl[48:53]

'''
这里假设全仓操作，由第一个信号决定
'''
# 全仓操作所以signal==keep
test_kl['keep']=test_kl['signal']
# 将keep列中的NAN使用向下填充的方式填充，使得keep代表最终交易状态
test_kl['keep'].fillna(method='ffill', inplace=True)

'''下面计算基准收益，计算目的是为了与使用策略后的收益进行对比，所以新加入数据列benchmark_profit,来计算每一天的收益。基准收益简单来说就是，你从时间序列第一天开始就持有股票，直到时间序列的最后一天'''
test_kl['benchmark_profit'] = np.log(test_kl['close']/test_kl['close'].shift(1))
# 仅仅为了说明np.log()函数的意义，添加benchmark_profit2只为了对比数据是否一致
test_kl['benchmark_profit2'] = test_kl['close']/test_kl['close'].shift(1) - 1
# 可视化对比两种方式计算出的profit是一致的
test_kl[['benchmark_profit', 'benchmark_profit2']].plot(subplots=True, grid=True, figsize=(14,7))

'''以下代码计算使用策略收益,test_kl['keep']是一个由01组成的数据列，用它乘以benchmark_profit,类似一个滤波器'''
test_kl['trend_profit'] = test_kl['keep'] * test_kl['benchmark_profit']
test_kl['trend_profit'].plot(figsize=(14,7))

test_kl[['benchmark_profit','trend_profit']].cumsum().plot(grid=True, figsize=(14,7))
# ld = test_kl[['benchmark_profit','trend_profit']].cumsum()
test_kl[['benchmark_profit','trend_profit']].cumsum().apply(np.exp).plot(grid=True)


'''
是列2：趋势跟踪策略
《海龟交易法则》是量化经典书籍中经典作品，其中介绍过一种趋势跟踪策略，即N日趋势突破策略
'''
# N1：当天收盘价高于N1天内最高价格作为买入信号，认为上升趋势成立买入股票
# N2：当天收盘价格低于N2天内最低价格作为卖出信号。认为下跌趋势成立卖出股票
'''
N1大于N2的原因是为了打造一个非均衡胜负收益以及非均衡胜负比例的环境
'''
import numpy as np
import pandas as pd
from abu.abupy import ABuSymbolPd
N1 = 42
N2 = 21
# # method test:pd.rolling_max()
# demo_list = np.array([1,2,1,1,100,1000])
# # 每3个一组找出每组中的最大值
# pd.rolling_max(demo_list, window=3)
'''
接下来继续使用特斯拉两年内的股票走势数据kl_pd,下面加入新的数据列nl_high,代表N1天内最高价格序列
'''
kl_pd = ABuSymbolPd.make_kl_df('usTSLA', n_folds=5)
kl_pd['n1_high'] = pd.rolling_max(kl_pd['high'], window=N1)
kl_pd[0:5]

# method test:pd.expanding_max()
# demo_list = np.array([1,2,1,1,100,1000])
# pd.expanding_max(demo_list)
'''
下面利用expanding_max函数填充n1_high前N1行数据
'''
expan_max= pd.expanding_max(kl_pd['close'])
# fillna()使用序列对应expan_max
kl_pd['n1_high'].fillna(value=expan_max, inplace=True)

'''下面构建N2天内最低价格卖出信号n2_low'''
kl_pd['n2_low'] = pd.rolling_min(kl_pd['low'], window=N2)
expan_min = pd.expanding_min(kl_pd['close'])
kl_pd['n2_low'].fillna(value=expan_min, inplace=True)

'''当天收盘价格超过N1天内的最高价突破定义来构建signal'''
buy_index = kl_pd[(kl_pd['close']>kl_pd['n1_high'].shift(1))&(kl_pd['key']>42)].index
kl_pd.loc[buy_index, 'signal'] = 1

sell_index = kl_pd[kl_pd['close'] < kl_pd['n2_low'].shift(1)].index
kl_pd.loc[sell_index, 'signal'] = 0

# kl_pd['signal'].fillna(method='ffill', inplace=True)
'''
因为要得到今天收盘价才进行操作，所以需要推迟到第二天
'''
kl_pd['keep'] = kl_pd['signal'].shift(1)
kl_pd['keep'].fillna(method='ffill', inplace=True)

kl_pd['benchmark_profit'] = np.log(kl_pd['close']/kl_pd['close'].shift(1))

kl_pd['trend_profit'] = kl_pd['keep'] * kl_pd['benchmark_profit']

kl_pd[['benchmark_profit','trend_profit']].cumsum().plot(grid=True, figsize=(14,7))




'''test案例，双高价比较'''

kl_pd = ABuSymbolPd.make_kl_df('usTSLA', n_folds=6)

N1 = 60
N2 = 30
kl_pd['n1_high'] = pd.rolling_max(kl_pd['high'], window=N1)
expan_max= pd.expanding_max(kl_pd['close'])
# fillna()使用序列对应expan_max
kl_pd['n1_high'].fillna(value=expan_max, inplace=True)

kl_pd['n2_high'] = pd.rolling_max(kl_pd['high'], window=N2)
# fillna()使用序列对应expan_max
kl_pd['n2_high'].fillna(value=expan_max, inplace=True)

buy_index = kl_pd[(kl_pd['close']>kl_pd['n1_high'].shift(1))&(kl_pd['key']>N1)].index
kl_pd.loc[buy_index, 'signal'] = 1

sell_index = kl_pd[kl_pd['close'] < kl_pd['n2_high'].shift(1)].index
kl_pd.loc[sell_index, 'signal'] = 0

kl_pd['keep'] = kl_pd['signal'].shift(1)
kl_pd['keep'].fillna(method='ffill', inplace=True)

kl_pd['benchmark_profit'] = np.log(kl_pd['close']/kl_pd['close'].shift(1))
kl_pd['trend_profit'] = kl_pd['keep'] * kl_pd['benchmark_profit']
kl_pd[['benchmark_profit','trend_profit']].cumsum().plot(grid=True, figsize=(14,7))

'''
仓位管理
凯里公式
'''
# b为赔率
# f = (p(win) * b - p(loss))/b

np.random.binomial(1,0.5)
