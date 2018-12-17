'''
    多进程 multiprocessing 跨平台的多进程模块

    Linux, Mac系统提供fork()函数，调用一次，返回两次
    把当前进程作为父进程克隆一份子进程，分别在进程中返回
    子进程返回0，父进程返回子进程ID
    fork()创建多个子进程


    start() 启动进程
    join()  用于进程同步，等待子进程结束再继续往下执行

    Pool 进程池
    控制子进程的输入输出 subprocess 模块


    进程间通信：
    Queue pipes等方式实现数据交互



'''

'''
import os

print('Process %s start...' %  os.getpid())
pid = os.fork()
if pid == 0:
    print('child process %s and parent process is %s' % (os.getpid(), os.getpid()))
else:
    print('%s just created a child process %s' % (os.getpid(), pid))
# Windown系统不支持 fork()

'''

from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')


# 启用大量子进程，需要Pool
from multiprocessing import Pool
import os
import time
import random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random()*3)
    end = time.time()
    print('Task %s run %0.2f s' % (name, (end - start)))

if __name__ == "__main__":
    print('Parent [rocess %s' % os.getpid())
    p = Pool()
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waitting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done')


# subprocess 模块
import subprocess

print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code', r)


# 子进程还需要输入
print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)


# 进程间通信
from multiprocessing import Process, Queue
import os, time, random

def write(q):
    print('Process to write: %s' % os.getpgid())
    for value in ['A','B','C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random()*3)

def read(q):
    print('Process to read: %s' % os.getpgid())
    while True:
        value = q.get(True)
        print('Get %s from queue' % value)

if __name__ == "__main__":
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate() # read是死循环，只能强制终止








