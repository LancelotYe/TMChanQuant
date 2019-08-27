import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    # def __init__(self):
    #     pass
    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance



# obj1 = Singleton()
# obj2 = Singleton()
# print(obj1,obj2)
#
# def task(arg):
#     obj = Singleton()
#     print(obj)
#
# for i in range(10):
#     t = threading.Thread(target=task,args=[i,])
#     t.start()




# import threading
#
# class SingletonType(type):
#     _instance_lock = threading.Lock()
#     def __call__(cls, *args, **kwargs):
#         if not hasattr(cls, "_instance"):
#             with SingletonType._instance_lock:
#                 if not hasattr(cls, "_instance"):
#                     cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
#         return cls._instance

# class Foo(metaclass=SingletonType):
#     def __init__(self,name):
#         self.name = name


# obj1 = Foo('name')
# obj2 = Foo('name')
# print(obj1,obj2)




# def Singleton(cls):
#     _instance = {}
#
#     def _singleton(*args, **kargs):
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kargs)
#         return _instance[cls]
#
#     return _singleton


# @Singleton
# class A(object):
#     a = 1
#
#     def __init__(self, x=0):
#         self.x = x

#
# a1 = A(2)
# a2 = A(3)
# print(a1,a2)

def SingletonCls(cls, class_name):
    if not hasattr(class_name, "_instance"):
        with class_name._instance_lock:
            if not hasattr(class_name, "_instance"):
                class_name._instance = object.__new__(cls)

    return class_name._instance