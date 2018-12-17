'''



    总结：
    分布式进程接口简单，封装良好，适合把繁重任务分布到多台机器的环境下

    Queue 作用：
    传递任务和接受结果，每个任务数据量尽量小
    进程稳，managers模块可以子进程分布到多台机器
    一Master--多worker
    线程只能分布到同一台机器的多个CPU上

    Master/Worker模型作用：
    分布式计算，可以启动多个worker，将任务分布到几台甚至几千台机器上
    比如：邮件信息队列形式异步发送
    Queue对象存储在task_master.py进程中
    task_worker.py只执行任务
    通过queueManager实现queue网络访问，需要给queue网络接口起名：get_task_queue
    authkey：保证了不同机器的正常通信，不被其它机器恶意干扰
    

'''
# 原有的Queue继续调用，使用Managers模块把queue通过网络暴露出去。
# 其它机器就可以通过进程访问Queue
from multiprocessing.managers import BaseManager
import queue, time, random

task_queue = queue.Queue()
reslut_queue = queue.Queue()

class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_reslut_queue', callable=lambda: reslut_queue)
manager = QueueManager(address=('', 5000), authkey=b'abc')
manager.start()
task = manager.get_task_queue()
reslut = manager.get_reslut_queue()
for i in range(10):
    n = random.randint(0, 10000)
    print('Put task %d' % n)
    task.put(n)
print('Try get reslut')
for i in range(10):
    r = reslut.get(timeout=10)
    print('Reslut : %s' % r)

manager.shutdown()
print('Master exit')
