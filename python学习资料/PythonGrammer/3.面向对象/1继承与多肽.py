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