from modules.funcs import *
import time
import subprocess
import json
from datetime import datetime
import os

# main loop
while True:
    service_list.clear()
    # CPU RAM DISK check
    check_cpu_ram()
    # Service status check
    if service_s == "On":
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
