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