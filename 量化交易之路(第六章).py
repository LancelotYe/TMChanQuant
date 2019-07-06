'''
第六章 量化工具---数学
'''

# 6.1回归与插值
'''
回归，指研究一组随机变量(Y1,Y2,Y3...Yi)和另一组(X1,X2,...,Xk)变量之间的关系的统计分析方法，又称多重回归分析。
通常Y1,Y2,...,Yi是因变量;X1,X2,...,Xk是自变量。
'''
'''
1.偏差绝对值之和最小（MAE）
2.偏差平方和最小（MSE）对误差极值的惩罚程度
3.偏差平方和开平方最小（RMSE）对误差的评估
'''
import numpy as np
from abu.abupy import ABuSymbolPd
tsla_close = ABuSymbolPd.make_kl_df('usTSLA').close
x = np.arange(0, tsla_close.shape[0])
y = tsla_close.values

'''
下面通过statsmodels.api.OLS()函数实现一次多项式拟合计算，即最简单的y = kx + b。使用summary（）函数可以看到
Method = Least Squares,即使用了最小二乘法。
'''
import statsmodels.api as sm
from statsmodels import regression
import matplotlib.pyplot as plt
def regress_y(y):
    y = y
    x = np.arange(0, len(y))
    x = sm.add_constant(x)
    # 使用OLS做拟合
    model = regression.linear_model.OLS(y,x).fit()
    return model

model = regress_y(y)
b = model.params[0]
k = model.params[1]

y_fit = k * x + b
plt.plot(x, y)
plt.plot(x, y_fit, 'r')
# summary()函数模拟拟合概述
model.summary()


'''
按照公式计算
MAE
'''
MAE = sum(np.abs(y-y_fit))/ len(y)
print('偏差绝对值之和(MAE)={}'.format(MAE))
MSE = sum(np.square(y-y_fit))/len(y)
print('偏差绝对值之和（MSE)={}'.format(MSE))
RMSE = np.sqrt(MSE)
print('偏差绝对值之和(RMSE)={}'.format(RMSE))


'''
多项式回归
观察上面的误差值，由于一次线性回归所以误差值很大，多项式回归拟合最简单的方式就是使用np.polynomial()函数
'''
# 以下计算1~9次多项式回归，计算MSE的值，可以看到随着poly的增大，MSE的值逐步降低
from sklearn import metrics
MAE2 = metrics.mean_absolute_error(y, y_fit)
MSE2 = metrics.mean_squared_error(y, y_fit)
RMSE2 = np.sqrt(MSE2)

import itertools
_, axs = plt.subplots(nrows=3, ncols=3, figsize=(15,15))
axs_list = list(itertools.chain.from_iterable(axs))

poly = np.arange(1, 10, 1)
for p_cnt, ax in zip(poly, axs_list):
    # 使用polynomial.Chebyshev.fit()函数进行多项式拟合
    p = np.polynomial.Chebyshev.fit(x, y, p_cnt)
    # 使用p直接对x序列代入即得到拟合结果序列
    y_fit = p(x)
    # 度量mse值
    mse = metrics.mean_squared_error(y, y_fit)
    # 使用拟合次数和mse误差大小设置标题
    ax.set_title('{} poly MSE={}'.format(p_cnt, mse))
    ax.plot(x,y,'',x,y_fit,'r.')
