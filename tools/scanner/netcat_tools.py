#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, getopt, subprocess, traceback
import threading
import logging
import socket

logging.basicConfig(level=logging.DEBUG)
listen, cmd, upload, execute, target, des, port = False, False, False, "", "", "", 0


def usage():
    info = """
    ************ IPO version netcat ************
    useage: python netcat_tools.py -t target_host -p port
    -l --listen 
    -e --execute=file_to_run
    -c --command
    -u --upload_destination 
    """
    print(info)
    sys.exit(0)


def run_command(cmd):
    cmd = cmd.rstrip()
    try:
        output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Error to execute code\r\n"
    return output


def handler(client_socket):
    global upload
    global execute
    global cmd
    if len(des):
        file_buf = ""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buf += data
        try:
            f_desciptor = open(des, "wb")
            f_desciptor.write(file_buf)
            f_desciptor.close()
            client_socket.send("Successfully save file to %s\r\n" % des)

        except:
            client_socket.send("Successfully save file to %s\r\n" % des)
    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if cmd:
        while True:
            client_socket.send("<IPO GET:$> ")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            res = run_command(cmd_buffer)
            client_socket.send(res)

def server_wait_loop():
    global target
    global port
    logging.info("start listening %s" % str(target))
    if not len(target):
        target = '0.0.0.0'
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handler, args=(client_socket,))
        client_thread.start()

def client_send(buf):
    
    logging.info("Prepare send something")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((target, port))
        if len(buf):
            print(buf)
            client.send(buf)
        while True:
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            print(response)
            buf = raw_input("")
            buf += '\n'
            client.send(buf)
    except Exception as e:
        logging.warning("Err! Exit!")
        logging.error(str(e))
        traceback.print_exc(file=sys.stdout)
        client.close()




def main():
    
    global listen
    global cmd
    global upload
    global execute
    global target
    global des
    global port
    opt = None
    args = None
    if len(sys.argv) < 2:
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        logging.error(str(err))
        usage()
    
    for o, a in opts:
        
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            logging.debug("this is a listen server")
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
            logging.debug("execute is " + a)
        elif o in ("-t", "--target"):
            target = a
            logging.debug("target is " + target)
        elif o in ("-p", "--port"):
            port = int(a)
            logging.debug("port is " + a)
        elif o in ("-c", "--command"):
            cmd = True
        elif o in ("-u", "--upload"):
            des = a
        else:
            assert False, "There is no match option"

    if not listen and len(target) and port > 0:
        buf = sys.stdin.read()
        logging.debug("input buf: " + str(buf))
        client_send(buf)

    if listen:
        server_wait_loop()


main()
