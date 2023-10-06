import configparser
from modules import MyService
import time
import urllib3
import json
import traceback
import psutil
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')
name = config['agent-config']['name']
webhook_url = config['slack']['url'] + config['slack']['token']
log_dir = config['agent-config']['log_pwd']
log_name = log_dir + 'status-ch' + datetime.today().strftime('%d-%m-%Y') + '.log'
service_list = []


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


def date_now_log():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def cpu_perc():
    return psutil.cpu_percent(1)

def vmem_perc():
    return psutil.virtual_memory().percent

while True:
    service_list.clear()
    for check in check_services():

        if check[1] == False:
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = str([date_now, name, check[0]])
            print(f'[!] {date_now_log()} Service {name} stopped')
            log_write(log_name, str(f'[!] {date_now_log()} Send {data}\n'))
            slack_notification(f'{name}', f'{date_now_log()} Service {check[0]} stopped','#e01e5a')
        # else:
        #     date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     data = str([date_now, name, check[0]])
        #     print(f'[+] {date_now_log()} Send {name} all is ok')
        #     #slack_notification(f'{name}', f'{date_now_log()} Работает {data}','#f2c744')
    cpu_p = cpu_perc()
    vmem_p = vmem_perc()
    if int(cpu_p) > 60:
        slack_notification(f'{name}', f'{date_now_log()} CPU is over 50% load! {cpu_p}','#e01e5a')

    if int(vmem_p) > 50:
        slack_notification(f'{name}', f'{date_now_log()} RAM is over 70% load! {vmem_p}', '#e01e5a')
    time.sleep(3)