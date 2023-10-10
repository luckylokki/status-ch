import configparser
from modules import MyService
import time
import subprocess
import urllib3
import json
import traceback
import psutil
from datetime import datetime
import os

config = configparser.ConfigParser()
config.read('config.ini')
name = config['agent-config']['name']
webhook_url = config['slack']['url'] + config['slack']['token']
log_dir = config['agent-config']['log_pwd']
log_name = log_dir + 'status-ch/' + datetime.today().strftime('%d-%m-%Y') + '.log'
pm2_status = config['PM2']['pm2_service']
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
            print(f'[!] {date_now_log()} Service {check[0]} stopped or not exist, check it!')
            log_write(log_name, str(f'[!] {date_now_log()} Service {check[0]} stopped or not exist, check it!\n'))
            slack_notification(f'{name}', f'{date_now_log()} Service {check[0]} stopped or not exist, check it!', '#e01e5a')

    cpu_p = cpu_perc()
    vmem_p = vmem_perc()
    if int(cpu_p) > 80:
        slack_notification(f'{name}', f'{date_now_log()} CPU is over 80% load! {cpu_p}', '#e01e5a')
        log_write(log_name, str(f'[!] {date_now_log()} Server {name} CPU is over 80% load! {cpu_p}\n'))

    if int(vmem_p) > 70:
        slack_notification(f'{name}', f'{date_now_log()} RAM is over 70% load! {vmem_p}', '#e01e5a')
        log_write(log_name, str(f'[!] {date_now_log()} Server {name} RAM is over 70% load! {vmem_p}\n'))
    time.sleep(15)
    #PM2 status check
    if pm2_status == 'On':
        try:
            if os.path.isfile('/etc/status-ch/l1'):
                subprocess.call("sudo rm -f /etc/status-ch/l1", shell=True)
            subprocess.call('pm2 jlist > l1', shell = True)
            with open('l1', 'r') as log:
                data = json.load(log)
                print(type(data))
            for i in range(len(data)):
                if data[i]["pm2_env"]["status"] != 'online':
                    slack_notification(f'{name}', f'{date_now_log()} PM2 ID: {data[i]["pm2_env"]["pm_id"]}, name: {data[i]["name"]}, status: {data[i]["pm2_env"]["status"]}')
        except:
            print("PM2 Unknown Error")
            log_write(log_name, str(f'[!] {date_now_log()} Server {name} PM2 Unknown Error\n'))
