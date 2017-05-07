import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback
import logging
import paramiko
from paramiko.py3compat import b, u, decodebytes


# setup logging
paramiko.util.log_to_file('demo_server.log')

host_key = paramiko.RSAKey(filename='test_rsa.key')
#host_key = paramiko.DSSKey(filename='test_dss.key')

print('Read key: ' + u(hexlify(host_key.get_fingerprint())))


class Server (paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'iotbigdata') and (password == 'xu.6jp6fu/ '):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

# now connect
server = sys.argv[1]
ssh_port = int(sys.argv[2])
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    logging.info('[+] Bind Success!')

except Exception as e:
    logging.warning('[-] Bind failed: ' + str(e))
    traceback.print_exc()
    sys.exit(1)

try:
    sock.listen(100)
    logging.info('[+] Listening for connection ...')
    client, addr = sock.accept()
except Exception as e:
    logging.warning('[-] Listen/accept failed: ' + str(e))
    traceback.print_exc()
    sys.exit(1)

print('Got a connection!')

try:
    t = paramiko.Transport(client)
    t.add_server_key(host_key)
    server = Server()
    try:
        t.start_server(server=server)
    except paramiko.SSHException:
        logging.warning('[-] SSH negotiation failed.')
        sys.exit(1)

    # wait for auth
    chan = t.accept(20)
    if chan is None:
        logging.info('*** No channel.')
    print('Authenticated!')
    chan.send('Welcome to my dirty ssh!')
    chan.send('We are on fire all the time!  Hooray!  Candy corn for everyone!')
    while True:
        try:
            command = raw_input("Enter Command").strip('\n')
            if command != "exit":
                chan.send(command)
                print(chan.recv(1024))
            else:
                chan.send("exit")
                print("exiting..")
                t.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            t.close()
except Exception as e:
    logging.warning('[!] Caught exception: ' +
                    str(e.__class__) + ': ' + str(e))
    traceback.print_exc()
    try:
        t.close()
    except:
        pass
    sys.exit(1)
