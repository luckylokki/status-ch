
import subprocess
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
log_dir = config['agent-config']['log_pwd']
subprocess.call("sudo mkdir status-ch", shell=True, cwd='/etc/')
subprocess.call("sudo mkdir status-ch", shell=True, cwd=log_dir)
subprocess.call("sudo cp -r status-ch.service /etc/systemd/system/", shell=True)
subprocess.call("sudo cp -r * /etc/status-ch", shell=True)
subprocess.call("sudo rm -f /etc/status-ch/install.py", shell=True)
subprocess.call("sudo python3 -m venv venv", shell=True, cwd='/etc/status-ch/')
cmd = 'source /etc/status-ch/venv/bin/activate; pip install -r requirements.txt; deactivate'
subprocess.call(cmd, shell=True, executable='/bin/bash')
subprocess.call("sudo systemctl enable status-ch", shell=True)
subprocess.call("sudo systemctl daemon-reload", shell=True)
subprocess.call("sudo systemctl start status-ch", shell=True)