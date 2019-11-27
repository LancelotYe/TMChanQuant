class Animal(object):
    def run(self):
        print('Animal is running...')

class Dog(Animal):
    pass

class Cat(Animal):
    pass

dog = Dog()
dog.run()

cat = Cat()
cat.run()

a = list() # a是list类型
b = Animal() # b是Animal类型
c = Dog() # c是Dog类型

isinstance(a, list)

isinstance(b, Animal)

isinstance(c, Dog)

"""
获取对象信息
"""
type(123)


import types


def fn():
    pass


type(fn) == types.FunctionType

type(abs) == types.BuiltinFunctionType

type(lambda x:x) == types.LambdaType

type((x for x in range(10))) == types.GeneratorType

"""
使用dir()
如果要获得一个对象的所有属性和方法，可以使用dir()函数，它返回一个包含字符串的list，比如，获得一个str对象的所有属性和方法：
"""
dir('ABC')

# 仅仅把属性和方法列出来是不够的，配合getattr()、setattr()以及hasattr()，我们可以直接操作一个对象的状态：
class MyObject(object):
    def __init__(self):
        self.x = 9
    def power(self):
        return self.x * self.x


obj = MyObject()
hasattr(obj, 'x')  # 有属性'x'吗？
setattr(obj, 'y', 19)  # 设置一个属性'y'
getattr(obj, 'y')  # 获取属性'y'


# 如果试图获取不存在的属性，会抛出AttributeError的错误：
getattr(obj, 'z') # 获取属性'z'
getattr(obj, 'z', 404)  # 获取属性'z'，如果不存在，返回默认值404

# 也可以获得对象的方法：
hasattr(obj, 'power')
getattr(obj, 'power')  # 获取属性'power'
fn = getattr(obj, 'power')  # 获取属性'power'并赋值到变量fn
fn()  # 调用fn()与调用obj.power()是一样的

# 通过内置的一系列函数，我们可以对任意一个Python对象进行剖析，拿到其内部的数据。要注意的是，只有在不知道对象信息的时候，我们才会去获取对象信息。如果可以直接写：
sum = obj.x + obj.y
sum = getattr(obj, 'x') + getattr(obj, 'y')

"""
由于Python是动态语言，根据类创建的实例可以任意绑定属性。
给实例绑定属性的方法是通过实例变量，或者通过self变量：
"""
class Student(object):
    def __init__(self, name):
        self.name = name

s = Student('Bob')
s.score = 90

# 但是，如果Student类本身需要绑定一个属性呢？可以直接在class中定义属性，这种属性是类属性，归Student类所有：
class Student(object):
    name = 'Student'

s = Student() # 创建实例s
print(s.name) # 打印name属性，因为实例并没有name属性，所以会继续查找class的name属性
s.name = 'Tom'  # 给实例绑定name属性
print(s.name)
print(Student.name) # 但是类属性并未消失，用Student.name仍然可以访问
del s.name  # 如果删除实例的name属性
delattr(s, 'name')
print(s.name)  # 再次调用s.name，由于实例的name属性没有找到，类的name属性就显示出来了


