import subprocess
import threading
import time
import schedule


def check_linux():
    print("Check Linux")
    subprocess.run(['chmod', '777', './os/linux_check.sh'], capture_output=True, text=True)
    subprocess.run(['./os/linux_check.sh'], capture_output=True, text=True)


def job2():
    print("I'm running on thread %s" % threading.current_thread())


def job3():
    print("I'm running on thread %s" % threading.current_thread())


def run_threaded(job_func):
    """
    可并行执行任务
    :param job_func:
    :return:
    """
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


# # 定时执行
# schedule.every(1).hours.do(run_threaded, check_linux())
# schedule.every(10).seconds.do(run_threaded, job2)
# schedule.every(10).seconds.do(run_threaded, job3)
# while True:
#     schedule.run_pending()
#     time.sleep(5)


# a = "00:d2:7b:9d:05:1b:43:fc:9b:30:40:66:43:81:bf:68:41:e8:44:a2:ee:40:48:b3:53:01:52:3d:02:69:82:41:30:a3:5f:6f:1b:2c:42:2b:1e:f4:cd:57:a5:72:85:05:de:b4:38:02:90:de:61:05:18:ab:e4:24:9b:c1:87:5b:a7:89:4e:9d:af:ca:e3:58:ed:29:24:2f:24:cf:f0:88:29:be:62:54:5d:4a:1a:6d:1e:d0:1a:56:5b:1c:2f:a6:c1:e7:78:a4:53:62:b7:2c:31:e0:1c:fd:b9:d3:b8:a0:56:3f:d6:f0:a8:50:92:da:36:6b:24:2e:36:97:7e:a7:23:a3:78:8e:c1:8e:35:08:05:6e:58:00:2a:e0:89:9d:3e:0e:2a:35:21:3c:c7:85:d2:eb:86:bd:10:62:77:08:5e:9b:9e:2b:05:bc:7d:3e:95:ab:c3:be:6b:e0:dc:12:6c:eb:dd:ce:c6:8f:b4:ef:78:2b:9b:6d:c6:89:e1:80:95:79:75:22:cc:01:06:20:f1:39:3c:64:4a:24:ec:49:90:c3:0c:d9:86:4e:f1:c6:d3:54:61:68:27:22:3e:15:36:86:4b:c8:74:49:10:30:f1:ff:62:33:a1:49:c8:ba:25:18:63:40:93:f0:72:0b:18:53:4f:f6:4c:a3:ac:c1:51"
# b = "00:d2:7b:9d:05:1b:43:fc:9b:30:40:66:43:81:bf:68:41:e8:44:a2:ee:40:48:b3:53:01:52:3d:02:69:82:41:30:a3:5f:6f:1b:2c:42:2b:1e:f4:cd:57:a5:72:85:05:de:b4:38:02:90:de:61:05:18:ab:e4:24:9b:c1:87:5b:a7:89:4e:9d:af:ca:e3:58:ed:29:24:2f:24:cf:f0:88:29:be:62:54:5d:4a:1a:6d:1e:d0:1a:56:5b:1c:2f:a6:c1:e7:78:a4:53:62:b7:2c:31:e0:1c:fd:b9:d3:b8:a0:56:3f:d6:f0:a8:50:92:da:36:6b:24:2e:36:97:7e:a7:23:a3:78:8e:c1:8e:35:08:05:6e:58:00:2a:e0:89:9d:3e:0e:2a:35:21:3c:c7:85:d2:eb:86:bd:10:62:77:08:5e:9b:9e:2b:05:bc:7d:3e:95:ab:c3:be:6b:e0:dc:12:6c:eb:dd:ce:c6:8f:b4:ef:78:2b:9b:6d:c6:89:e1:80:95:79:75:22:cc:01:06:20:f1:39:3c:64:4a:24:ec:49:90:c3:0c:d9:86:4e:f1:c6:d3:54:61:68:27:22:3e:15:36:86:4b:c8:74:49:10:30:f1:ff:62:33:a1:49:c8:ba:25:18:63:40:93:f0:72:0b:18:53:4f:f6:4c:a3:ac:c1:51"

# print(a==b)
