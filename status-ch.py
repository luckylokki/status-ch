from modules import MyService
from modules.funcs import *
import time
import subprocess
import urllib3
import json
import traceback
from datetime import datetime
import os


def log_write(file, data):
    with open(file, 'a') as log:
        log.write(data)


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


def check_services():
    for key in config['services']:
        service_list.append(MyService(config['services'][key]).check_service_status())
    return service_list


def check_cpu_ram():
    cpu_p = cpu_perc()
    vmem_p = vmem_perc()
    disk_p = disk_perc()
    if int(cpu_p) > max_cpu:
        slack_notification(f'{name}', f'{date_now_log()} {cpu_p}% of CPU used is over 80% load!', '#e01e5a')
        log_write(log_name, str(f'[!] {date_now_log()} Server {name}: {cpu_p}% of CPU used is over 80% load!\n'))

    if int(vmem_p) > max_vram:
        slack_notification(f'{name}', f'{date_now_log()} {vmem_p}% of RAM used is over 80% load!', '#e01e5a')
        log_write(log_name, str(f'[!] {date_now_log()} Server {name}: {vmem_p}% of RAM used is over 80% load!\n'))

    if int(disk_p) > max_disk:
        slack_notification(f'{name}', f'{date_now_log()} {disk_p}% of DISK space used is over 80% load!', '#e01e5a')
        log_write(log_name,
                  str(f'[!] {date_now_log()} Server {name}: {disk_p}% of DISK space used is over 80% load!\n'))


# main loop
while True:
    service_list.clear()
    # CPU RAM DISK check
    check_cpu_ram()
    # Service status check
    for check in check_services():
        if check[1] == False:
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = str([date_now, name, check[0]])
            print(f'[!] {date_now_log()} Service {check[0]} stopped or not exist, check it!')
            log_write(log_name, str(f'[!] {date_now_log()} Service "{check[0]}" stopped or not exist, check it!\n'))
            slack_notification(f'{name}', f'{date_now_log()} Service "{check[0]}" stopped or not exist, check it!',
                               '#e01e5a')
    # PM2 status check
    if pm2_status == 'On':
        if os.path.isfile('/etc/status-ch/l1'):
            subprocess.call("sudo rm -f /etc/status-ch/l1", shell=True)
        subprocess.call('pm2 jlist > l1', shell=True)
        try:
            with open('l1', 'r') as log:
                data = json.load(log)
                print(type(data))
            for i in range(len(data)):
                if data[i]["pm2_env"]["status"] != 'online':
                    slack_notification(f'{name}',
                                       f'{date_now_log()} PM2 ID: "{data[i]["pm2_env"]["pm_id"]}", name: "{data[i]["name"]}", status: "{data[i]["pm2_env"]["status"]}" stopped, check it!',
                                       '#e01e5a')
        except:
            slack_notification(f'{name}',
                               f'{date_now_log()} Cant read "l1" file with pm2 statuses!',
                               '#e01e5a')
    # sleep for 30sec
    time.sleep(stime)
