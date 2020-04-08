import socket
import threading
import time
import sys


def connectTs(host):
    try:
        tcs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Connect to TS")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
    tsListenPort = int(sys.argv[3])
    port = tsListenPort
    localhost_addr = socket.gethostbyname(host)

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    #print(localhost_addr)
    tcs.connect(server_binding)
    return tcs


def ls():
    #create server socket to communicate with cs
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    # server_binding = ('', 50007)
    server_binding = ('', int(sys.argv[1]))
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    #create ts1 socket
    try:
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Connect to TS1")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
    ts1ListenPort = int(sys.argv[3])
    ts1Hostname = sys.argv[2]
    ts1IP = socket.gethostbyname(ts1Hostname)
    ts1_binding = (ts1IP, ts1ListenPort)
    ts1.connect(ts1_binding)

    #create ts2 socket
    try:
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Connect to TS2")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
    ts2ListenPort = int(sys.argv[5])
    ts2Hostname = sys.argv[4]
    ts2IP = socket.gethostbyname(ts2Hostname)
    ts2_binding = (ts2IP, ts2ListenPort)
    ts2.connect(ts2_binding)


    while 1:
        hn = csockid.recv(1024)
        ts1.send(hn)
        ts2.send(hn)
        data_from_ts1 = ts1.recv(1024)
        data_from_ts2 = ts2.recv(1024)
        dts1 = data_from_ts1.decode('utf-8')
        dts2 = data_from_ts2.decode('utf-8')
        msg = ''


        #replace this code with timeout
        # if dts1 == "nf" and dts2 == "nf":
        #     msg = "Hostname - Error:HOST NOT FOUND"
        #     csockid.send(msg.encode('utf-8'))
        # # print(hostname)
        csockid.send(dts1.encode('utf-8'))
        csockid.send(dts2.encode('utf-8'))




t2 = threading.Thread(name='client', target=client)
t2.start()

time.sleep(5)
# input("hit ENTER to exit")

exit()
