import socket

c=socket.socket()
Format ='utf-8'
c.connect(('localhost',9999))
while True:
    name=input("enter name")
    c.send(bytes(str(len(name)),Format))
    c.send(bytes(name,Format))
    print(c.recv(1024).decode())

# c.send(bytes(str(len("!Disconn")),Format))
# c.send(bytes("!Disconn",Format))