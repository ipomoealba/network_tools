# coding=UTF-8
import optparse
import threading
from pexpect import pxssh


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


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
            print(bcolors.WARNING + "[!] " + str(e) + bcolors.ENDC)
            print(bcolors.FAIL + '[-] Error Connecting' + bcolors.ENDC)

    def send_command(self, cmd="whoami"):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before


class ThreadClass(threading.Thread):
    def __init__(self, host, account, passwd, command):
        super(ThreadClass, self).__init__()
        self.host = host
        self.account = account
        self.passwd = passwd
        self.command = command

    def run(self):
        print(bcolors.OKBLUE + "[o] Connecting to " + str(self.host) +
              ": " + str(self.account) + bcolors.ENDC)
        c = Client(self.host, self.account, self.passwd)
        c.connect()
        print(bcolors.OKGREEN + "[o] " + bcolors.ENDC + bcolors.OKBLUE + str(self.host) +
              ": " + str(self.account) + bcolors.ENDC + bcolors.OKGREEN + c.send_command(self.command) + bcolors.ENDC)
        # sn = serverlist[self.index]
        # print sn
        # same code as before, minus the index = index + 1 bit


def main(register_book, command=None):

    fn = open(register_book, 'r')
    for i in fn.readlines():
        host, account, passwd = i.split(' ')
        t = ThreadClass(host, account, passwd, command)
        t.start()


main("./registerbook.txt", "whoami")
