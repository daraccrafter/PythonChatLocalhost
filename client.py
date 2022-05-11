import socket
import sys
import threading
import time


def socket_connection():                                                #function used to restart the socket connection
    new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # specify type of address we are looking for (IPV4)
    new_sock.connect(ADDR)                                              # binding the socket to the address
    return new_sock

def send(msg):
    new_msg = msg.encode('utf-8')                                       # encode the msg we are sending to server
    sock.sendall(new_msg)                                               # sendall python function to keep sending until all data is sent
    return

def get_flag():                                                         #function to return the state of the flag
    global flag
    return flag

def receiveAll (data):                                                  # function to receive all data independent of buffer size
    while data[len(data) - 1] != 10:                                    # loop until the last byte is equal \n
        data = data + sock.recv(NUM_BYTES)
    return data


def send_msg():
    global flag,sock                                                    # initialize the global variables inside function so we can access them
    try:
        while True:                                                     # keep asking for input
            time.sleep(0.1)                                             # make sure that the global variable flag is updated correctly before every iteration

            if get_flag() == True:                                      # if the flag state is True that means that the username is IN-USE
                sock.close()                                            # close the current socket to restart it

                print("Username taken enter new username: ")
                msg = "HELLO-FROM " + input("")                         # preformat message

                sock = socket_connection()                              # call socket_connection function to start a new socket connection

                flag = False                                            # set the flag back to False

            else:
                msg = input("")

                if msg == "!quit":                                          # if msg is !quit
                    raise Exception("\n[EXITING]")                          # raise exception and jump to catch

                elif "@" == msg[0]:                                         # if the msg contains @
                    msg_substrings = msg.split(" ")                         # split msg (with whitespace) into substrings
                    username = msg_substrings[0][1:len(msg_substrings[0])]  # get the name of the user we want to send to
                    msg = "SEND " + username                                # prepare msg the server will accept

                    for x in range(1, len(msg_substrings)):                 # connect the actual msg from the substrings
                        msg = msg + " " + msg_substrings[x]

                elif "!who" == msg[0:4]:                                    # if user types in !who convert to what server will understand
                    msg = "WHO"

            send(msg + "\n")                                                # send msg to server

    except KeyboardInterrupt and Exception as e:
        print(e)                                                        # print when exiting
        t.join(0.1)                                                     # wait 100ms for thread to finish
        sock.close()                                                    # close socket



def recv_msg():
    global flag                                                         # initialize the global variable flag so we can use it inside function
    while True:
        if get_flag() == True:                                          # if the flag is True that means the connection is not restarted so we basically just loop until the flag is false
            pass
        else:
            data = sock.recv(NUM_BYTES)                                 # recv NUM_BYTES of data to see if there is connection
            if not data:                                                # no connection = break loop
                break
            if NUM_BYTES < 7:                                           # check if the buffer is less then 7 ( needed for inuse)
                data = receiveAll(data)
            if 'IN-USE' in data.decode('utf-8'):                        # check if server sends back IN-USE
                flag = True
            else:                                                       # receiveall function
                data = receiveAll(data).decode('utf-8')
                print(data+"\n")


###########################################################################################################################################################################################

sys.tracebacklimit = 0                                                  # supress traceback information

PORT = 5050                                                             # set up port to connect to
SERVER = socket.gethostbyname(socket.gethostname())                                               # get localhost address
ADDR = (SERVER, PORT)                                                   # tuple of address and port
NUM_BYTES = 2                                                          # buffer size



global flag
global sock
flag = False

sock = socket_connection()                                             # start socket connection

t = threading.Thread(target=recv_msg,args=())                          # set up a new thread running function recv_msg()
t.daemon = True                                                        # if the main thread terminates terminate the others
t.start()                                                              # start thread



send_msg()                                                             # start send_msg()







