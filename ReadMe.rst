###############################################################################
                            SERVICES STATUS CHECKER
###############################################################################

This is a training project for checking statuses.

Getting started
===============

#. Download the code base
#. Make sure tha you have installed Python3.10 and python3.10-venv

Editing config file
=====================
Edit config.ini:

.. code-block::
    [agent-config]
    name = NAME OF SERVER #It will be used for clask notification, for understanding which server
    log_pwd = /var/log/ #folder where will be folder with logs
    [services] #Example for two services
    service_name_0 = nginx #service you want monitor
    service_name_1 = zabbix-agent
    [PM2]
    pm2_service = On/Off "On if use pm2 Off is dont use it"
    [slack]
    url = https://hooks.slack.com/services/
    token = YOUR_SLACK_TOKEN
    [percents]#integer num % when bot must send notification if server uses more.
    max_cpu = 80
    max_vram = 80
    max_disk = 80
    [sleeptime]
    #Time in seconds, check every 30 sec by default
    stime = 30

You can add services as much as you like, just add new:
example: service_name_2 = MyService
You need copy "service_name" and change number this all.
Services means that command will be look - systemctl status "YourService"

After finish edit config.ini, you must run(sudo mode)
.. code-block::
    sudo python3 install.py

That's create all folders,copy program to /etc/status-ch, create Daemon and run it.

Logs in /var/log/status-ch/ folder
Installed app in /etc/status-ch/ folder
You can control your app with this commands:
service status-ch status
service status-ch stop
service status-ch start
service status-ch restart