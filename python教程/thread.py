# 多进程
# import os
#
# def myfork():
#     a=1
#     pid = os.fork()
#     if pid == 0:
#         print('this is child', pid, os.getpid(), os.getppid())
#         print(a+1)
#     else:
#         print('this is parent', pid, os.getpid(), os.getppid())
#         print(a+3)
#
#
# if __name__ == '__main__':
#     myfork()

# 多进程
'''
Unix/Linux操作系统提供了一个fork()系统调用，调用一次，返回两次。因为操作系统自动吧当前
'''



'''
多任务可以由多进程完成，也可以由一个进程内的多线程完成
我们前面提到了进程由若干线程组成的，一个进程至少有一个线程。
由于线程是操作系统直接支持的执行单位，因此，高级语言通常都内置多线程的支持，python的线程是真正的Posix Thread，而不是模拟出来的线程。
Python的标准库提供了两个模块：_thread和threading,_thread是低级模块,threading是高级模块，对_thread进行封装。绝大多数情况下，
我们只需要使用threading这个高级模块
'''
import time,threading


#新线程执行的代码
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended' % threading.current_thread().name)

# Lock
'''
多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在与每一个进程中，互不影响，而多线程中，
所有变量都由所有线程共享，所以任何一个变量都可以被任何一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时改变一个变量，
把内容改乱了。
'''
import time ,threading
# 假定这是你的银行存款
balance = 0

def change_it(n):
    # 先存后取，结果应该为0
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)

'''
我们定义了一个共享变量balance，初始值为0，并且启动两个线程，先存后取，理论上结果应该为0，但是，由于线程的调度是由操作系统决定的，
当t1,t2交替执行时，只要循环次数足够多，balance的结果就不一定是0了（原因是因为高级语言的一条语句在CPU执行时是若干条语句）
'''

'''
究其原因，是因为修改balance需要多条语句，而执行这几条语句时，线程可能中断，从而导致多个线程把同一对象的内容改乱了。
我们一定要确保，一条线程在修改时，其他线程绝对不能改

如果我们确保balance计算正确，就要change_it()上一把锁，当某个线程开始执行change_it()时，该线程因为获得了锁，
因此其他线程不能同时执行change_it(),只能同时等待，直到所有锁被释放。，获得该锁以后才能改。由于锁只有一个，吴润线程多少，同一时刻，
最多只有一个线程持有该锁。
'''

balance = 0
lock = threading.Lock()

def run_thread(n):
    for i in range(100000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()
'''
当多个线程同时执行lock.acquire()时，只有一个线程能成功地获取锁，然后继续执行代码，其他线程继续等待知道获得锁为止。
获得锁的线程用完提后一定要释放锁，否则那些苦苦等待的线程将会永远等待下去，形成死锁。所以我们用try finally来确保锁一定会释放。
锁的好处就是确保了某段关键代码只能由一个线程从头到尾完整地执行，坏处当然也很多，首先时阻止了多线程并发执行，
包含锁的某段代码实际上只能以单线程模式执行，效率就大大地下降了。其次，由于可以存在多个锁，不同线程持有不同的锁，并试图获取对方持有的锁时，
可能会造成死锁，导致多个线程全部挂起，即不能执行，也无法结束，只能靠操作系统强制终止。
'''

# 多核CPU
'''
如果你不幸拥有一个多核CPU，你肯定在想，多核应该可以同时执行多个线程。
'''
import threading,multiprocessing

def loop():
    x = 0
    while True:
        x = x^1

for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()

'''
IO密集型代码(文件处理、网络爬虫等涉及文件读写的操作)，多线程能够有效提升效率(单线程下有IO操作会进行IO等待，造成不必要的时间浪费，
而开启多线程能在线程A等待时，自动切换到线程B，可以不浪费CPU的资源，从而能提升程序执行效率)。所以python的多线程对IO密集型代码比较友好。
'''



# TreadLocal
'''
在多线程环境下，每个线程都有自己的数据。一个线程使用自己的局部变量比使用全局变量好，因为局部变量只有线程自己能看见，不会影响其他线程，而全局变量的修改必须加锁。

但是局部变量也有问题，就是在函数调用的时候，传递起来很麻烦：
'''
# def process_student(name):
#     std = Student(name)
#     # std是局部变量，但是每个函数都要用它，因此必须传进去：
#     do_task_1(std)
#     do_task_2(std)
#
#
# def do_task_1(std):
#     do_subtask_1(std)
#     do_subtask_2(std)
#
# def do_task_2(std):
#     do_subtask_2(std)
#     do_subtask_2(std)

'''
每个函数一层一层调用都这么传参数那还得了？用全局变量？也不行，因为每个线程处理不同的Student对象，不能共享。
如果用一个全局dict存放所有的Student对象，然后以thread自身作为key获得线程对应的Student对象如何？
'''
# global_dict = {}
#
# def std_thread(name):
#     std = Student(name)
#     # 把std放到全局变量global_dict中：
#     global_dict[threading.current_thread()] = std
#     do_task_1()
#     do_task_2()
#
# def do_task_1():
#     # 不传入std，而是根据当前线程查找：
#     std = global_dict[threading.current_thread()]
#
#
# def do_task_2():
#     # 任何函数都可以查找出当前线程的std变量：
#     std = global_dict[threading.current_thread()]

'''
上述意思是对应线程获取对应的对象数据，然后操作
有没有更简单的方式？

ThreadLocal应运而生，不用查找dict，ThreadLocal帮你自动做这件事：
'''
import threading

# 创建全局threadLocal对象
local_school = threading.local()

def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()

t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
'''
全局变量local_school就是一个ThreadLocal对象，每个Thread对它都可以读写student属性，但互不影响。你可以把local_school看成全局变量，但每个属性如local_school.student都是线程的局部变量，可以任意读写而互不干扰，也不用管理锁的问题，ThreadLocal内部会处理。

可以理解为全局变量local_school是一个dict，不但可以用local_school.student，还可以绑定其他变量，如local_school.teacher等等。

ThreadLocal最常用的地方就是为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，这样一个线程的所有调用到的处理函数都可以非常方便地访问这些资源。
'''


# 进程 vs. 线程
