import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

HOST = socket.gethostbyname(socket.gethostname())
print("host : ",HOST)
PORT = 9999
Header = 64
FORMAT = 'utf-8'
DISCONN_MSG = "!Disconn"
mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create TCP socket ipv4
mySocket.bind((HOST, PORT))
mySocket.listen()
clientsList=[]
print("listening on", (HOST, PORT))
mySocket.setblocking(False)
# chat_dict = {"hi":"hi", "hello":"hello", "good morning":"good morning!","good night":"good night!","good evening":"good evening!"}

sel.register(mySocket, selectors.EVENT_READ, data=None)


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    clientsList.append(conn)
    print("accepted connection from", addr)
    conn.setblocking(False)
    # sock.send(bytes(str("connect with the SERVER ["+str(HOST)+ "] at PORT ["+str(PORT))+"]",'utf-8'))
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        print("we received " , recv_data)
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("sending message: ", repr(data.outb), ". to: ", data.addr)
            for client in clientsList:
                client.send(data.outb)
            data.outb = b''

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)

sel.close()

"""
def clients(c,addr):
        print("connected with",addr)
        c.send(bytes(str("connect with the SERVER ["+str(ip)+ "] at PORT ["+str(port))+"]",'utf-8'))
        connected =True
        while connected:
            msg_lenght=c.recv(Header).decode(Format)
            if msg_lenght:
                msg_lenght=int(msg_lenght)
                msg=c.recv(msg_lenght).decode(Format)
                print(msg)
                if msg == Disconn_msg:
                    connected=False 
                    c.send(bytes(str("disconnected with the SERVER ["+str(ip)+ "] at PORT ["+str(port)) +"]",Format))
                    clients_dict.pop(addr[1])
                    print(clients_dict)
                else:
                    response = chat_dict.get(msg)
                    if response:
                        c.send(bytes(str(response),Format))  
                    else:
                          c.send(bytes(str("What?!"),Format))  
        print(f"connection with {addr} is closed ")
        c.close()

def start():
    s.listen(3) # listening to three clients
    print("waiting for connection")
    while True:
        c,addr =s.accept()
        thread=threading.Thread(target=clients,args=(c,addr))
        thread.start()
        clients_dict.update({addr[1]:addr[0]})
        print (clients_dict)
        print(f"Active connection {threading.active_count()-1}")


start()
"""
