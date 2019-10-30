# 函数名也是变量
def add(x, y, f):
    return f(x) + f(y)

print(add(-5, 6, abs))

# map
"""
我们先看map。map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回。
举例说明，比如我们有一个函数f(x)=x^2，要把这个函数作用在一个list [1, 2, 3, 4, 5, 6, 7, 8, 9]上，就可以用map()实现如下：
"""
def f(x):
    return x * x
r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
"""
map()作为高阶函数，事实上它把运算规则抽象了，因此，我们不但可以计算简单的f(x)=x2，还可以计算任意复杂的函数，比如，把这个list所有数字转为字符串：
"""
#reduce
"""
再看reduce的用法。reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算，其效果就是
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
"""
# example1
from functools import reduce
def add(x, y):
    return x + y
reduce(add, [1, 2, 3, 4, 5, 6, 7, 8, 9])
# example2
def fn(x, y):
    return x * 10 + y
reduce(fn, [1, 3, 5, 7, 9])
# example3
def char2num(s):
    digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    return digits[s]
reduce(fn, map(char2num, '13579'))

# filter
"""
和map()类似，filter()也接收一个函数和一个序列。和map()不同的是，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。
例如，在一个list中，删掉偶数，只保留奇数，可以这么写
"""
def is_odd(n):
    return n % 2 == 1
f = filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])
list(f)

"""
把一个序列中的空字符串删掉，可以这么写：
"""
def not_empty(s):
    return s and s.strip()

list(filter(not_empty, ['A', '', 'B', None, 'C', '  ']))

"""
筛选素数
"""
def odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n

def not_divisible(n):
    return lambda x : x % n > 0

def primes():
    yield 2
    it = odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(not_divisible(n), it)

for n in primes():
    if n < 1000:
        print(n)
    else:
        break

"""
筛选回数
"""
def is_palindrome(n):
    return str(n) == str(n)[::-1]

output = filter(is_palindrome, range(1, 1000))
print('1~1000:', list(output))

"""
排序
"""
# 排序算法
sorted([36, 5, -12, 9, -21])
# 此外，sorted()函数也是一个高阶函数，它还可以接收一个key函数来实现自定义的排序，例如按绝对值大小排序：
sorted([36, 5, -12, 9, -21], key=abs)
# 我们再看一个字符串排序的例子：
sorted(['bob', 'about', 'Zoo', 'Credit'])
"""
默认情况下，对字符串排序，是按照ASCII的大小比较的，由于'Z' < 'a'，结果，大写字母Z会排在小写字母a的前面。
现在，我们提出排序应该忽略大小写，按照字母序排序。要实现这个算法，不必对现有代码大加改动，只要我们能用一个key函数把字符串映射为忽略大小写排序即可。忽略大小写来比较两个字符串，实际上就是先把字符串都变成大写（或者都变成小写），再比较。
这样，我们给sorted传入key函数，即可实现忽略大小写的排序：
"""
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
# 要进行反向排序，不必改动key函数，可以传入第三个参数reverse=True：
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)

# sorted()也是一个高阶函数。用sorted()排序的关键在于实现一个映射函数。
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_name(t):
    return t[0]

def by_score(t):
    return t[1]

L2 = sorted(L, key=by_score)
print(L2)