import sys
import socket
import selectors
import types
import pymongo


sel = selectors.DefaultSelector()

## connect to database and make the chatbot data

myclient = pymongo.MongoClient("mongodb://localhost:27017/") #connect to MongoDB

mydb = myclient["networkDB"] # create a database

mydb.drop_collection("ChatBot") # drop the previous data base

userData = mydb["ChatBot"] # create a new collection 

replies = open("replies.txt") #open th file that contain all replies

## doing some processing to the data in file to be ready to insert it into our database

repliesData = replies.read()
data = []
fisrt = repliesData.split("\n")
for i in fisrt:
    data.append(i.split(":"))

sendingData = []
for i in data:
    sendingData.append({i[0]:' '.join(map(str, i[1:]))})

# inserting the data to our databese
userData.insert_many(sendingData) 



HOST = socket.gethostbyname(socket.gethostname())    # getting the Host name
print("host : ",HOST) 

PORT = 9999         # the port that we will run the server on

FORMAT = 'utf-8'    # the formate we use to incode the message sent

DISCONN_MSG = "!Disconn"    #disconnect message that will be sent from the client

mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create TCP socket ipv4

mySocket.bind((HOST, PORT))

mySocket.listen()

clientsList=[]      # making a list to store all the conn objects

print("listening on", (HOST, PORT))

mySocket.setblocking(False)     # to make the server listen to multible conn without stucking in one of them

sel.register(mySocket, selectors.EVENT_READ, data=None) 


def accept_wrapper(sock):

    conn, addr = sock.accept()  # Accept the new connection 

    clientsList.append(conn)    # take this conn socket object and store it to use it when we want to send any message to hime

    # sending the connection message
    conn.send( bytes(str("connect to the Server: "),FORMAT) + bytes(str(addr[0]),FORMAT) + bytes(str(" at the Port: "),FORMAT) + bytes(str(addr[1]),FORMAT))

    print("accepted connection from", addr)

    conn.setblocking(False)

    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"") # make an object to store the data in/out/addr of this connections/socket

    events = selectors.EVENT_READ | selectors.EVENT_WRITE   # making this socket doing read and write operation

    sel.register(conn, events, data=data)   # resgister the socket to monitor it 

def service_connection(key, mask):

    sock = key.fileobj # the socket object

    data = key.data # the data object that we made for this socket

    if mask & selectors.EVENT_READ: # if this is a reading operation go in it

        recv_data = sock.recv(1024)  # read the message came from the client

        print("we received " , recv_data.decode())
        if recv_data: # if there any message go in

            if recv_data.decode() == "!Disconn": # if this message if Disconn. So, close the socket
                print("closing connection to", data.addr)
                clientsList.remove(sock)
                sel.unregister(sock)
                sock.close()
            else:
                #else store it in data object of this socket to resend it
                data.outb += recv_data
        else:
            # if there is no message close the connection
            print("closing connection to", data.addr)
            clientsList.remove(sock)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE: # if it writing operation (we want to send message our clients) go in

        if data.outb: # if there any data in our data object in the outb buffer go in
            if len(clientsList) == 1: # if there is just one client in our list go in
                # now the client will chat with our chatbot 
                sock.send( bytes(str("User "),FORMAT) + bytes(str(key.fd),FORMAT) + bytes(str(": "),FORMAT) + data.outb)
                for x in userData.find({},{ "_id": 0, data.outb.decode(): 1,}):
                    if x:
                        print(x[data.outb.decode()])
                        sock.send( bytes(str("\n"),FORMAT) +bytes(str("DoLaBot "),FORMAT) + bytes(str(": "),FORMAT) + bytes(str(x[data.outb.decode()]),FORMAT))
            else:
                # so there are many clients connected to the server. So, there will chat with each other
                # any message sent form any client will be resend to this clients and all other clients
                for client in clientsList:
                    client.send( bytes(str("User "),FORMAT) + bytes(str(key.fd),FORMAT) + bytes(str(": "),FORMAT) + data.outb)       
            data.outb = b''

while True:
    # be there and waite the selectore to tell us if there is a new connection 
    # or there is a connection want some services
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            # if it is none so this is a new connection. So, accept it
            accept_wrapper(key.fileobj)
        else:
            # if it is not none so this is an accepted connection and the socket is established already 
            service_connection(key, mask)

sel.close()
userData.drop()
