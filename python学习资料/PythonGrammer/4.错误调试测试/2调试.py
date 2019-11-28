'''
断言
凡是用print()来辅助查看的地方，都可以用断言（assert）来替代：
'''
def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!'
    return 10 / n

def main():
    foo('0')

'''
logging
把print()替换为logging是第3种方式，和assert比，logging不会抛出错误，而且可以输出到文件：
'''
import logging
logging.basicConfig(level=logging.INFO)
s = '0'
n = int(s)
logging.info('n = %d' % n)
print(10 / n)
'''
logging.info()就可以输出一段文本。运行，发现除了ZeroDivisionError，没有任何信息。怎么回事？

别急，在import logging之后添加一行配置再试试：
'''
logging.basicConfig(level=logging.INFO)

'''pdb'''


