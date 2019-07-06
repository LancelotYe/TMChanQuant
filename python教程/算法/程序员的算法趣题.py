'''
算法学习
'''



# 03翻牌
'''
解题
'''
import numpy as np
ar = np.zeros(100)
def myTest():
    for i in  range(2,101):
        for j in range(i, 101, i):
            ar[j-1]=1 if (ar[j-1]==0) else 0

myTest()

'''
答案
'''
card = np.zeros(100)
for i in range(2, 101):
    j = i - 1
    while j < card.size:
        card[j]=1 if card[j]==0 else 0
        j += i


