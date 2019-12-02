'''
用Python来编写脚本简化日常的运维工作是Python的一个重要用途。在Linux下，有许多系统命令可以让我们时刻监控系统运行的状态，如ps，top，free等等。要获取这些系统信息，Python可以通过subprocess模块调用并获取结果。但这样做显得很麻烦，尤其是要写很多解析代码。

在Python中获取系统信息的另一个好办法是使用psutil这个第三方模块。顾名思义，psutil = process and system utilities，它不仅可以通过一两行代码实现系统监控，还可以跨平台使用，支持Linux／UNIX／OSX／Windows等，是系统管理员和运维小伙伴不可或缺的必备模块。
'''

# 获取CPU信息
# 我们先来获取CPU的信息：
import psutil
psutil.cpu_count() # CPU逻辑数量
psutil.cpu_count(logical=False) # CPU物理核心

# 统计CPU的用户／系统／空闲时间：
psutil.cpu_times()

# 再实现类似top命令的CPU使用率，每秒刷新一次，累计10次：
for x in range(10):
    psutil.cpu_percent(interval=1, percpu=True)

'''获取内存信息
使用psutil获取物理内存和交换内存信息，分别使用：'''
psutil.virtual_memory()
psutil.swap_memory()

'''返回的是字节为单位的整数，可以看到，总内存大小是8589934592 = 8 GB，已用7201386496 = 6.7 GB，使用了66.6%。

而交换区大小是1073741824 = 1 GB。'''

# 获取磁盘信息
# 可以通过psutil获取磁盘分区、磁盘使用率和磁盘IO信息：
psutil.disk_partitions() # 磁盘分区信息
psutil.disk_usage('/') # 磁盘使用情况
psutil.disk_io_counters() # 磁盘IO
# 可以看到，磁盘'/'的总容量是998982549504 = 930 GB，使用了39.1%。文件格式是HFS，opts中包含rw表示可读写，journaled表示支持日志。


'''
获取网络信息
psutil可以获取网络接口和网络连接信息：
'''
psutil.net_io_counters() # 获取网络读写字节／包的个数
psutil.net_if_addrs() # 获取网络接口信息
psutil.net_if_stats() # 获取网络接口状态

# 要获取当前网络连接信息，使用net_connections()：
psutil.net_connections()

# 你可能会得到一个AccessDenied错误，原因是psutil获取信息也是要走系统接口，而获取网络连接信息需要root权限，这种情况下，可以退出Python交互环境，用sudo重新启动：

'''
获取进程信息
通过psutil可以获取到所有进程的详细信息：
'''
psutil.pids() # 所有进程ID
p = psutil.Process(3776) # 获取指定进程ID=3776，其实就是当前Python交互环境
p.name() # 进程名称
p.exe() # 进程exe路径
p.cwd() # 进程工作目录
p.cmdline() # 进程启动的命令行
p.ppid() # 父进程ID
p.parent()  # 父进程
p.children() # 子进程列表
p.status() # 进程状态
p.username() # 进程用户名
p.create_time() # 进程创建时间
p.terminal() # 进程终端
p.cpu_times() # 进程使用的CPU时间
p.memory_info() # 进程使用的内存
p.open_files() # 进程打开的文件
p.connections() # 进程相关网络连接
p.num_threads() # 进程的线程数量
p.threads() # 所有线程信息
p.environ() # 进程环境变量
p.terminate() # 结束进程

'''
和获取网络连接类似，获取一个root用户的进程需要root权限，启动Python交互环境或者.py文件时，需要sudo权限。
psutil还提供了一个test()函数，可以模拟出ps命令的效果：
'''
