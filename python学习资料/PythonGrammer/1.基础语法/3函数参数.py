# 可变参数
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

calc(1, 2)
calc()

# 关键字参数
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

person('Adam', 45, gender='M', job='Engineer')
'''
name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
'''
