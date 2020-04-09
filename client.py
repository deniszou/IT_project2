import socket
import threading
import time
import sys



def client():
    lsHost = sys.argv[1]
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        # exit()
    # Define the port on which you want to connect to the server
    lsListenPort = int(sys.argv[2])
    port = lsListenPort
    localhost_addr = socket.gethostbyname(lsHost)

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    with open("PROJ2-HNS.txt") as f:
        lines = f.readlines()

    print(lines)

    f = open("RESOLVED.txt", "w+")

    time.sleep(1.5)


    for line in lines:
        line = line.lower()

        # send to RS
        cs.send(line.strip("\n").encode('utf-8'))

        data_from_server = cs.recv(1024)
        d = data_from_server.decode('utf-8')
        print('works', d)

        #if d.endswith("A") or d.endswith("A\n"):
        time.sleep(1.5)
        if d == "Hostname - Error:HOST NOT FOUND":
            print("[C]: Error:HOST NOT FOUND", d)
            f.write(line.strip("\n") + " - Error:HOST NOT FOUND\n")
        else:
            print("[C]: Data matched in RS table and received from server:", d)
            f.write(d)
    #cs.send("end".encode('utf-8'))

    f.close()
    #cs.close()
    #exit()


t2 = threading.Thread(name='client', target=client)
t2.start()

time.sleep(5)
# input("hit ENTER to exit")

exit()
