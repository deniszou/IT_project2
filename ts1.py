import threading
import time
import random
import socket
import sys


def readFile():
    fh = open("PROJ2-DNSTS1.txt")

    for ln in fh:
        rec = ln.split(' ')
        dict1[rec[0]] = (rec[0] + " " + rec[1] + " " + rec[2])
    fh.close()


def checkKey(k, dict1):
    for key in dict1:
        if key == k:
                return (key, dict1[key][0], dict1[key][1])


def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    #server_binding = ('', 50008)
    server_binding = ('', int(sys.argv[1]))
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from ls at {}".format(addr))

    while 1:
        hn = csockid.recv(1024)
        hostname = hn.decode('utf-8')
        #print(hostname)
        readFile()

        # Close the server socket
        if hostname == "end":
            ss.close()
            exit()

        if dict1.get(hostname, "dne") != "dne":
            msg = dict1.get(hostname, "dne")
            csockid.send(msg.encode('utf-8'))



dict1 = {}
t1 = threading.Thread(name='tsServer', target=server)
t1.start()