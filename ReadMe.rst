###############################################################################
                            SERVICES STATUS CHECKER
###############################################################################

This is a training project for checking statuses.

Getting started
===============

#. Download the code base
#. Make sure tha you have installed Python3

Editing config file
=====================
Edit config.ini:

.. code-block::
    [agent-config]
    name = NAME OF SERVER
    log_pwd = /var/log/ #folder where will be folder with logs
    [services]
    service_name_0 = nginx #service you want monitor
    service_name_1 = zabbix-agent
    [slack]
    url = https://hooks.slack.com/services/
    token = YOUR_SLACK_TOKEN

You can add services as much as you like, just add new:
example: service_name_2 = MyService
You need vopy "service_name" and change number this all.
Services means that command will be look - systemctl status "YourService"

After finish edit config-server.ini, you must run
.. code-block::
    python3 install.py

That's create all folders,copy program to /etc/cims-client, create Daemon and run it.