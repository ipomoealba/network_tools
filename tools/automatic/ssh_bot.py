# coding=UTF-8
import optparse
import pxssh

class Client:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            print('[-] Error Connecting')

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before


def main(register_book):
    fn = open(register_book, 'r')
    for i in fn.readlines():
        host, account, passwd = i.split(' ')
        c = Client(host, account, passwd)
        c.connect()
        c.send_command(self, "whomai")
