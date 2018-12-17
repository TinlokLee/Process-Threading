'''
    多任务处理--多线程 threading 模块
    线程锁
    Lock.acquire()  lock.release()
    GIL 每个线程执行100条字节码，Python解释器就自动释放GIL锁

    总结：
    多线程编程，模型复杂，容易发生冲突，必须枷锁隔离，小心死锁发生
    多线程无法利用多核，目前Python只能通过多进程利用多核
    多线程即交替执行，而非并发执行！历史遗留问题！


'''

import threading, time

def task():
    print('Thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n += 1
        print('Thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(2)
    print('Thread %s end' % threading.current_thread().name)

print('Thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=task, name='LoopThread')
t.start()
t.join()
print('Thread %s end' % threading.current_thread().name)

# 线程锁
balance = 0
lock = threading.Lock()

def run_thread(n):
    for i in range(100000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()

# 多核CPU
def loop():
    '''死循环慎用'''
    x = 0
    while True:
        x = x ^ 1
for i  in range(multiprocess.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()