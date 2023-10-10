import psutil
from datetime import datetime


def date_now_log():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def cpu_perc():
    return psutil.cpu_percent(1)


def vmem_perc():
    return psutil.virtual_memory().percent


def disk_perc():
    return psutil.disk_usage('/').percent


if __name__ == "__main__":
    print("Run status-ch.py")
