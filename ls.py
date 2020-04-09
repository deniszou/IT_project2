import socket
import threading
import time
import sys


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
    ts1.settimeout(5)
    ts2.settimeout(5)
    csockid.settimeout(10)
    while 1:
        time1 = False
        time2 = False
        hn = csockid.recv(1024)
        print(hn.decode('utf-8'))
        ts1.send(hn)
        ts2.send(hn)

        try:
            data_from_ts1 = ts1.recv(1024)
        except socket.timeout as timeout:
            #ts1.send("timeout".encode('utf-8'))
            print("timeout1", timeout)
            data_from_ts1 = "timeout".encode('utf-8')
            time1 = True
            pass

        # except ts1.timeout as timeout1:
        #     #print("ts1 timeout")
        #     print(data_from_ts1 + '\n'.format(timeout1))

        #try:
        try:
            data_from_ts2 = ts2.recv(1024)
        except socket.timeout as timeout:
            #ts2.send("timeout".encode('utf-8'))
            print("timeout2", timeout)
            data_from_ts2 = "timeout".encode('utf-8')
            time2 = True
            pass

        dts1 = data_from_ts1.decode('utf-8')
        dts2 = data_from_ts2.decode('utf-8')

        if dts1 != "timeout":
            print(dts1)
            csockid.send(dts1.encode('utf-8'))
        if dts2 != "timeout":
            print(dts2)
            csockid.send(dts2.encode('utf-8'))
        if time1 and time2:
            csockid.send("Hostname - Error:HOST NOT FOUND".encode('utf-8'))




t2 = threading.Thread(name='lsServer', target=ls)
t2.start()

time.sleep(5)
# input("hit ENTER to exit")

exit()
