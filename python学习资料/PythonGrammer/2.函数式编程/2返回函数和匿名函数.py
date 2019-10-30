"""
高阶函数除了可以接受函数作为参数外，还可以把函数作为结果值返回。
我们来实现一个可变参数的求和。通常情况下，求和的函数是这样定义的：
"""
def calc_sum(*args):
    ax = 0
    for n in args:
        ax = ax + n
    return ax

# 但是，如果不需要立刻求和，而是在后面的代码中，根据需要再计算怎么办？可以不返回求和的结果，而是返回求和的函数：
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
f = lazy_sum(1, 3, 5, 7, 9)

# 闭包
"""
注意到返回的函数在其定义内部引用了局部变量args，所以，当一个函数返回了一个函数后，其内部的局部变量还被新函数引用，所以，闭包用起来简单，实现起来可不容易。
另一个需要注意的问题是，返回的函数并没有立刻执行，而是直到调用了f()才执行。我们来看一个例子：
"""
def count():
    fs = []
    for i in range(1,4):
        def f():
            return i * i
        fs.append(f)
    return fs

f1, f2, f3 = count()
# 全部都是9！原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。
"""
如果一定要引用循环变量怎么办？方法是再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变：
"""
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs

f1, f2, f3 = count()
f1()
f2()
f3()
"""
匿名函数
"""
# 在Python中，对匿名函数提供了有限支持。还是以map()函数为例，计算f(x)=x2时，除了定义一个f(x)的函数外，还可以直接传入匿名函数：
list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

f = lambda x : x * x
f(5)
# 使用匿名函数修改
def is_odd(n):
    return n % 2 == 1
L = list(filter(is_odd, range(1, 20)))

L= list(filter(lambda x:x%2==1, range(1,20)))
