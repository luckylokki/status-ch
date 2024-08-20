import psutil
from datetime import datetime
import configparser
import traceback
import urllib3
from modules import MyService
import json

config = configparser.ConfigParser()
config.read('config.ini')
name = config['agent-config']['name']
webhook_url = config['slack']['url_hook_token']
log_dir = config['agent-config']['log_pwd']
log_name = log_dir + 'status-ch/' + datetime.today().strftime('%d-%m-%Y') + '.log'
pm2_status = config['PM2']['pm2_service']
service_s = config['services-check']['service_s']
max_cpu = int(config['percents']['max_cpu'])
max_vram = int(config['percents']['max_vram'])
max_disk = int(config['percents']['max_disk'])
cpu_s = config['percents']['cpu_s']
vram_s = config['percents']['vram_s']
disk_s = config['percents']['disk_s']
stime = int(config['sleeptime']['stime'])
service_list = []


def slack_notification(who, message, color):
    try:
        slack_data = {
            "attachments": [
                {
                    "color": color,
                    "fields": [
                        {
                            "title": who,
                            "value": message,
                        }
                    ]
                }
            ]
        }
        slack_message = {'text': message}

        http = urllib3.PoolManager()
        response = http.request('POST',
                                webhook_url,
                                body=json.dumps(slack_data),
                                headers={'Content-Type': 'application/json'},
                                retries=False)
    except:
        traceback.print_exc()

    return True


def date_now_log():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def log_write(file, data):
    with open(file, 'a') as log:
        log.write(data)


def cpu_perc():
    return psutil.cpu_percent(1)


def vmem_perc():
    return psutil.virtual_memory().percent


def disk_perc():
    return psutil.disk_usage('/').percent


def check_services():
    for key in config['services']:
        service_list.append(MyService(config['services'][key]).check_service_status())
    return service_list


def check_cpu_ram():
    cpu_p = cpu_perc()
    vmem_p = vmem_perc()
    disk_p = disk_perc()
    if cpu_s == "On":
        if int(cpu_p) > max_cpu:
            slack_notification(f'{name}', f'{date_now_log()} {cpu_p}% of CPU used is over {max_cpu}% load!', '#e01e5a')
            log_write(log_name, str(f'[!] {date_now_log()} Server {name}: {cpu_p}% of CPU used is over {max_cpu}% load!\n'))
    if vram_s == "On":
        if int(vmem_p) > max_vram:
            slack_notification(f'{name}', f'{date_now_log()} {vmem_p}% of RAM used is over {max_vram}% load!', '#e01e5a')
            log_write(log_name, str(f'[!] {date_now_log()} Server {name}: {vmem_p}% of RAM used is over {max_vram}% load!\n'))
    if disk_s == "On":
        if int(disk_p) > max_disk:
            slack_notification(f'{name}', f'{date_now_log()} {disk_p}% of DISK space used is over {max_disk}% load!', '#e01e5a')
            log_write(log_name,
                      str(f'[!] {date_now_log()} Server {name}: {disk_p}% of DISK space used is over {max_disk}% load!\n'))


if __name__ == "__main__":
    print("Run status-ch.py")
