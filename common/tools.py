import os
import sys
import time
from threading import Thread, Event


def get_current_time(fmt='%Y-%m-%d-%H-%M-%S'):
    now = time.time()
    now_local = time.localtime(now)
    return time.strftime(fmt, now_local)


def get_program_directory():
    app_dir = os.getcwd()
    if not app_dir:
        cmd = sys.argv[0]
        app_dir = None
        if cmd:
            app_dir, filename = os.path.split(cmd)

    return os.path.abspath(app_dir)


def check_path(path):
    if not os.path.isabs(path):
        path = os.path.join(get_program_directory(), path)
    return path


def get_current_path(current_path, path):
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.realpath(current_path)), path)
    return path


def is_above_3_4():
    import sys
    major, minor = sys.version_info[:2]
    return major > 3 or (major == 3 and minor > 4)


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class _Timer(Thread):
    """
    Call a function after a specified number of seconds:

    t = Timer(30.0, f, args=[], kwargs={})
    t.start()
    t.cancel() # stop the timer's action if it's still waiting

    """

    def __init__(self, interval, function, *args, **kwargs):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    def cancel(self):
        """
        Stop the timer if it hasn't finished yet
        """
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()


class RepeatingTimer(_Timer):
    """
    周期定时器
    """
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


def set_priority(pid=None, priority=1):

    """ 设置程序运行优先级
    Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """

    import win32api,win32process,win32con

    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])

if __name__ == '__main__':
    print(get_host_ip())