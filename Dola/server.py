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
    print(clientsList)
    conn.send( bytes(str("connect to the Server: "),FORMAT) + bytes(str(addr[0]),FORMAT) + bytes(str(" at the Port: "),FORMAT) + bytes(str(addr[1]),FORMAT))
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        print("we received " , recv_data.decode())
        if recv_data:
            if recv_data.decode() == "!Disconn":
                print("closing connection to", data.addr)
                clientsList.remove(sock)
                sel.unregister(sock)
                sock.close()
            else:
                data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            clientsList.remove(sock)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            for client in clientsList:
                client.send( bytes(str("User "),FORMAT) + bytes(str(key.fd),FORMAT) + bytes(str(": "),FORMAT) + data.outb)
            data.outb = b''

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)

sel.close()
