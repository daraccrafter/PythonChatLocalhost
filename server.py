import socket                                                                           # import the socket library
import sys
import threading                                                                        # import the threading library
import time



class User(object):                                                                     # object for storing user data
    def __init__(self, username, addr, conn):                                           # constructor
        self.username = username
        self.addr = addr
        self.conn = conn



def receiveAll (data,conn):                                                  # function to receive all data independent of buffer size
    while data[len(data) - 1] != 10:                                    # loop until the last byte is equal \n
        data = data + conn.recv(NUM_BYTES)
    return data

def hello_from(addr,conn,msg):

        name = msg[11:len(msg)]                                                         # get name from message

        for x in list_of_users:                                                         # check if name is in the user list already
            if name == x.username:                                                      # if the above case is true
                conn.sendall("[IN-USE]\n".encode('utf-8'))                                   # send to the user that the name is in use
                return

        list_of_users.append(User(name, addr, conn))                                    # add the user  to the list

        response = "[HELLO] " + name + "\n"                                                    # create response text

        conn.sendall(response.encode('utf-8'))                                             # send response

        print(f"{name} connected from {addr}!")

        return name



def who(conn):

    response = "[WHO-OK]"                                                               # create response text

    for x in list_of_users:                                                             # iterate through all the users
        response = response + " " + x.username                                          # add users name to response text

    response = response + "\n"

    conn.sendall(response.encode('utf-8'))                                                 # send response to curr user

    return



def send(conn, msg, curr_addr, name):
    if "echobot" == msg[5:12]:
        echobot(msg,conn)
        print(f"{name} sent a message to echobot")

    else:
        separate_list = msg.split(" ")                                                  # split the msg using whitespace
        response = ""                                                                   # set response text

        for x in list_of_users:                                                         # iterate through the list of users
            if x.addr == curr_addr:                                                     # if the address of the current user and an address in the list match enter if
                response = f"[DELIVERY] {x.username}"                                   # add the DELIVERY + username of user sending msg
                break

        for x in range(2, len(separate_list)):                                          # iterate through msg (for example "SEND somone blablabla kekekeke") -> starts iterating from the blablabla
                response = response + " " + separate_list[x]                            # add each part of msg to response

        response = response + "\n"

        for x in list_of_users:                 # iterate through list of users
            if x.username == separate_list[1]:                                          # if the username of the person that the msg is being sent to corresponds one in the list enter if
                x.conn.sendall(response.encode('utf-8'))                                # send the response message to the recipient
                print(f"{name} sent a message to {x.username}")
                message = "[SEND-OK]\n"                                                 # send "SEND-OK" on succesfull sending
                break

            elif x.username not in separate_list[1]:                                      # if the username doesnt match anything in list
                message = "[UNKNOWN]\n"                                  # send "UNKNOWN" to the sender

        conn.sendall(message.encode('utf-8'))
    return



def clear_list(cur_addr):

    for x in list_of_users:                                                             # iterate through the list of users
        if x.addr == cur_addr:                                                          # if the address of the current user and an address in the list match enter if
            list_of_users.remove(x)                                                     # remove the user

    return



def handle_client(addr, conn):                                                          # function for handling client requests

    flag = False                                                                        # local variable flag

    while True:                                                                         # loop until data is received

        msg = conn.recv(NUM_BYTES)                                                      # receive data from client and decode it
        if not msg:                                                                     # if there is no connection clear user from list and stop thread
            clear_list(addr)
            sys.exit(0)

        msg = receiveAll(msg,conn).decode('utf-8')


        msg = msg.strip('\n')                                                           # removes newline character
        msg_substring_len = len(msg.split(" "))                                         # split with whitespace

        if 'HELLO-FROM' == msg[0:10] and flag == False:                                   # if the data has HELLO-FROM in it call the appropriate function
            if msg_substring_len > 1 and msg_substring_len < 1:                     # if we have more then 2 substrings or less then 2 send bad req body
                conn.sendall("[BAD-RQST-BODY]\n".encode('utf-8'))
            else:
                name = hello_from(addr,conn,msg)
                flag = True

        elif 'WHO' == msg and flag == True:                                         # if the data has HELLO-FROM in it call the appropriate function
            who(conn)

        elif 'SEND' == msg[0:4] and flag == True:                                        # if the data has HELLO-FROM in it call the appropriate function
            if msg_substring_len < 2:                                               # if we have less then 3 substrings send bad req body
                conn.sendall("[BAD-RQST-BODY]\n".encode('utf-8'))
            else:
                send(conn,msg,addr,name)

        else:
            conn.sendall("[BAD-RQST-HDR]\n".encode('utf-8'))                             # if none of the ifs match its a bad header


    return


def echobot(msg,conn):

    msg_array=msg.split(" ")
    msg_array = msg_array[2:len(msg_array)]
    response = "[DELIVERY] echobot"

    for x in msg_array:

            response = response + " " + x

    response= response+"\n"
    conn.sendall("[SEND-OK]\n".encode('utf-8'))
    conn.sendall(response.encode('utf-8'))

    return




def start():                                                                            # function to start listening on the port

    sock.listen()
    print(f"[LISTENING] SERVER LISTENING ON: {socket.gethostbyname(socket.gethostname())}, PORT: {PORT}")

    list_of_users.append(User("echobot", None, None))


    while True:                                                                         # listen until a client connects

        conn, addr = sock.accept()                                                         # accept the connection
                                                                                        # check if the max capacity is reached
        while threading.active_count()-1 == MAX_CLIENTS:                                # loop until a spot on the server frees up
            conn.sendall("[BUSY]\n".encode('utf-8'))                                         # send a BUSY msg if server is full
            time.sleep(3)                                                               # weit for 3 seconds and continue looping


        thread = threading.Thread(target=handle_client, args=(addr, conn))              # set the handle_client function (for the currently connected client) into a new thread

        thread.start()                                                                  # start the thread


    return

###########################################################################################################################################################################################

NUM_BYTES = 4096                                                                        # max number of bytes to receive
PORT = 5050                                                                             # port the server is running on
SERVER = ''                                                                             # getting the ipaddress of localhost
ADDR = (SERVER, PORT)                                                                   # create a tuple containing the server address and port

list_of_users = []                                                                      # global variable list of users
MAX_CLIENTS = 64                                                                        # global variable max clients

sys.tracebacklimit = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                   # specify type of address we are looking for (IPV4)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                                 # override TIME-WAIT state after shutdown
sock.bind(ADDR)                                                                            # binding the socket to the address

start()


