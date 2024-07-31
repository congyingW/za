import schedule
from datetime import datetime
import time
import threading


"""
每隔2秒执行一次，每隔3秒执行一次
"""
def task():
    now = datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    print(ts)


def task2():
    now = datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    print(ts + ' task2-666!')


def func():
    # 清空任务
    schedule.clear()
    # 创建一个按3秒间隔执行任务
    schedule.every(3).seconds.do(task)
    # 创建一个按2秒间隔执行任务
    schedule.every(2).seconds.do(task2)
    while True:
        schedule.run_pending()


# func()

"""
schedule方法是串行的，也就是说，如果各个任务之间时间不冲突，那是没问题的；如果时间有冲突的话，会串行的执行命令
"""
def job(name):
    print("her name is : ", name)


name = "张三"
schedule.every(10).minutes.do(job, name)  # 每10分钟
schedule.every().hour.do(job, name)  # 每1小时
schedule.every().day.at("10:30").do(job, name)  # 每天10.30
schedule.every(5).to(10).days.do(job, name)  # 每隔5-10天
schedule.every().monday.do(job, name)  # 每周一这个时候【运行此脚本的时候】
schedule.every().wednesday.at("13:15").do(job, name)  # 每周三13.15执行

while True:
    schedule.run_pending()  # 运行所有可运行的的任务
    time.sleep(1)

"""
使用线程并行任务
"""
def job1():
    print("I'm running on thread %s" % threading.current_thread())


def job2():
    print("I'm running on thread %s" % threading.current_thread())


def job3():
    print("I'm running on thread %s" % threading.current_thread())


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every(10).seconds.do(run_threaded, job1)
schedule.every(10).seconds.do(run_threaded, job2)
schedule.every(10).seconds.do(run_threaded, job3)
while True:
    schedule.run_pending()
    time.sleep(1)
