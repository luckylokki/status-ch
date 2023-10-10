import psutil
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
name = config['agent-config']['name']
webhook_url = config['slack']['url'] + config['slack']['token']
log_dir = config['agent-config']['log_pwd']
log_name = log_dir + 'status-ch/' + datetime.today().strftime('%d-%m-%Y') + '.log'
pm2_status = config['PM2']['pm2_service']
max_cpu = int(config['percents']['max_cpu'])
max_vram = int(config['percents']['max_vram'])
max_disk = int(config['percents']['max_disk'])
stime = int(config['sleeptime']['stime'])
service_list = []
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
