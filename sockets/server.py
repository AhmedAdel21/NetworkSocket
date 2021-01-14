import socket
import threading

ip=socket.gethostbyname(socket.gethostname())
port=9999
Header=64
Format='utf-8'
Disconn_msg="!Disconn"
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create TCP socket ipv4
clients_dict={}
chat_dict = {"hi":"hi", "hello":"hello", "good morning":"good morning!","good night":"good night!","good evening":"good evening!"}
print("Socket created")

s.bind(('localhost',9999)) # define the ip  and the port

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