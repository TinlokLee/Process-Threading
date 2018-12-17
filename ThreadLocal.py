'''
    ThreadLocal 
    每个线程都有自己的数据，使用局部变量，函数调用时麻烦？

    总结：
    一个ThreadLocal虽然是全局变量，但每个线程都只能读写自己线程内
    的独立副本，互不干扰，解决在参数在一个线程中，各个函数间的传递

    多任务处理方案：
    多进程
    多线程
    异步IO编程模型（事件驱动编程）
    单线程的异步编程：协程

    任务分为：
    CPU 密集型：涉及大量计算，音视频处理 ---> 最好用C语言或多进程处理
    IO  密集型：涉及网络，磁盘IO ---> 多线程
    
'''

import threading

local_user = threading.local()

def process_pepo():
    std = local_user.pepo
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    local_user.pepo = name
    process_pepo()

t1 = threading.Thread(target=process_thread, args=('li,'), name="Thread-A")
t2 = threading.Thread(target=process_thread, args=('zhang,'), name="Thread-B")
t1.start()
t2.start()
t1.join()
t2.join()
