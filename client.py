import socket
import threading


PORT = 5050                                                             # set up port to connect to
DISCONNECT_MESSAGE = "!quit"                                            # set up the disconnect message
SERVER = socket.gethostbyname(socket.gethostname())                     # get localhost address
ADDR = (SERVER, PORT)                                                   # tuple of address and port
NUM_BYTES = 4096                                                        # buffer size

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                   # specify type of address we are looking for (IPV4)
s.connect(ADDR)                                                         # binding the socket to the address


def send(msg):
    new_msg = msg.encode('utf-8')                                       # encode the msg we are sending to server
    s.sendall(new_msg)                                                  # sendall python function to keep sending until all data is sent
    return

def send_msg():
    try:                                                                # if CONTROL-C happens jump to exception
        while True:                                                     # keep asking for input
            msg = input("\n")

            if msg == DISCONNECT_MESSAGE:                               # if msg is !quit
                send(msg)                                               # send !quit to server so it removes your from user list
                print("[EXITING]")
                break                                                   # break loop
            send(msg)
    except:
        send(DISCONNECT_MESSAGE)
        print("\n[EXITING]")


def recv_msg():
    while True:
        data = s.recv(NUM_BYTES).decode('utf-8')                        # save data from buffer and decode
        if not data:                                                    # if no data break loop
            break
        print(data+'\n')                                                # print server msg




t = threading.Thread(target=recv_msg,args=())                          # set up a new thread running function recv_msg()
t.start()                                                              # start thread

send_msg()                                                             # start send_msg()





