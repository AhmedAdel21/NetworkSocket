from sys import argv
from gui import *
import threading
import socket
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
import cv2 as cv
import selectors
import types

Format ='utf-8'


class Yahoo(Ui_MainWindow):
    def __init__(self,mainwindow):
        super(Yahoo,self).setupUi(mainwindow)
        self.Message.returnPressed.connect(self.append_text)
        self.send.clicked.connect(self.append_text)
        self.connect.clicked.connect(self.connecting)
        self.disconnect.clicked.connect(self.disconnecting)
        self.isConnected=False
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.listenToServer)
        self.sel = selectors.DefaultSelector()
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 9999
    def start_connections(self):
        server_addr = (self.HOST, self.PORT)
        print('starting connection','to', server_addr)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex(server_addr)
        self.timer.start()
        # events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # data = types.SimpleNamespace(
        #                                 msg_total = 0 ,
        #                                 recv_total = 0,
        #                                 messages= b'' ,
        #                                 outb = b'')
        # self.sel.register(self.sock, events, data=data)
        # events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # data = types.SimpleNamespace(
        #                             msg_total = 0 ,
        #                             recv_total = 0,
        #                             messages= 0 ,
        #                             outb = b'')
        # self.sel.register(sock, events, data=data)
        # events = self.sel.select(timeout=None)
        # for key, mask in events:
        #     #if it's not none So, it’s a client socket that’s already been accepted
        #     self.service_connection(key, mask)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            print("we are in read")
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print('received', repr(recv_data))
                # data.recv_total += len(recv_data)
            # if not recv_data or data.recv_total == data.msg_total:
            #     print('closing connection', data.connid)
            #     self.sel.unregister(sock)
            #     sock.close()
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages
                data.messages = b''
            if data.outb:
                print('sending', repr(data.outb), 'to the server')
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
                self.receive()

                
    def connecting(self):
        if not self.isConnected:
            self.isConnected=True
            # self.client=socket.socket()
            # self.client.connect(('localhost',9999))
            self.start_connections()
            print("connected")

            # self.server_text.append(self.client.recv(1024).decode())
            self.state.setText("Connected")
            self.state.setStyleSheet("color: green")
            self.image.setPixmap(QtGui.QPixmap("conn.png")) 
            # self.thread=threading.Thread(target=self.recv,args=(self.client,"c")) 
            # self.thread.start()
    def disconnecting(self):
        if self.isConnected:
            self.isConnected=False
            # self.thread.close()
            # self.client.send(bytes(str(len("!Disconn")),Format))
            # self.client.send(bytes("!Disconn",Format))
            # self.server_text.append(self.client.recv(1024).decode())
            self.state.setText("Disconnected")
            self.state.setStyleSheet("color: red")   
            self.image.setPixmap(QtGui.QPixmap("disconn.png"))

    def listenToServer(self):
        try:
            message = self.sock.recv(1024).decode()
            self.chatting_text.append(message)
        except BlockingIOError :
            print("idle")

    def append_text(self):
        if self.isConnected:
            text=self.Message.text()
            # self.client.send(bytes(str(len(text)),Format))
            # self.client.send(bytes(text,Format))
            self.sock.send(bytes(text,Format))
            
            # events = selectors.EVENT_READ | selectors.EVENT_WRITE
            # data = types.SimpleNamespace(
            #                             msg_total = len(text) ,
            #                             recv_total = 0,
            #                             messages= bytes(text,Format) ,
            #                             outb = b'')
            # events = self.sel.select(timeout=None)
            # for key, mask in events:
            #     #if it's not none So, it’s a client socket that’s already been accepted
            #     self.service_connection(key, mask)

            text = '<div style=\" color: black; text-align: left; \" ><p style=\" background-color: white;\">%s</p></div>' % text
            # self.chatting_text.append(self.client.recv(1024).decode())
            self.Message.clear()

if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Yahoo(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())