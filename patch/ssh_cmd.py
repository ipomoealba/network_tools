import threading
import paramiko
import subprocess

def ssh_cmd(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.load_host_keys('/.ssh/known_host')
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))
    return

if __name__ == '__main__':
    # ssh_cmd('140.119.19.21', 'iotbigdata', 'xu.6jp6fu/ ', 'id')
    pass
