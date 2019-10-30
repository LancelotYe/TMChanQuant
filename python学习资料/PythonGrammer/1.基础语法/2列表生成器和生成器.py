"""
但是循环太繁琐，而列表生成式则可以用一行语句代替循环生成上面的list：
"""
l = [x * x for x in range(1, 11)]
"""
for循环后面还可以加上if判断，这样我们就可以筛选出仅偶数的平方：
"""
l = [x * x for x in range(1, 11) if x % 2 == 0]
"""
还可以使用两层循环，可以生成全排列：
"""
l = [m + n for m in 'ABC' for n in 'XYZ']
"""
运用列表生成式，可以写出非常简洁的代码。例如，列出当前目录下的所有文件和目录名，可以通过一行代码实现：
"""
import os
l = [d for d in os.listdir('.')]

"""
for循环其实可以同时使用两个甚至多个变量，比如dict的items()可以同时迭代key和value：
"""
d = {'x': 'A', 'y': 'B', 'z': 'C' }
for k, v in d.items():
    print(k, '=', v)
# 因此，列表生成式也可以使用两个变量来生成list：
l= [k + '=' + v for k, v in d.items()]

L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [s.lower() for s in L1 if isinstance(s, str)]
print(L2)

'''
通过列表生成式，我们可以直接创建一个列表。但是，受到内存限制，列表容量肯定是有限的。而且，创建一个包含100万个元素的列表，不仅占用很大的存储空间，如果我们仅仅需要访问前面几个元素，那后面绝大多数元素占用的空间都白白浪费了。

所以，如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？这样就不必创建完整的list，从而节省大量的空间。在Python中，这种一边循环一边计算的机制，称为生成器：generator。
'''
L = [x * x for x in range(10)]
L

g = (x * x for x in range(10))
g
next(g)
for n in g :
    print(n)


g = (x * x for x in range(10))
for n in g:
    print(n)
"""
比如，著名的斐波拉契数列（Fibonacci），除第一个和第二个数外，任意一个数都可由前两个数相加得到：
"""
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a + b
        n = n + 1
    return 'done'

"""
将斐波那契数列推算成generator
"""
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'

f = fib(6)


def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)

g = fib(6)
while True:
     try:
         x = next(g)
         print('g:', x)
     except StopIteration as e:
         print('Generator return value:', e.value)
         break