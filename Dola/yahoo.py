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

                
    def connecting(self):
        if not self.isConnected:
            # self.isConnected=True
            self.start_connections()
            # print("connected")
            # self.server_text.append("connect with the SERVER ["+str(self.HOST)+ "] at PORT ["+str(self.PORT)+"]")
            # self.state.setText("Connected")
            self.state.setStyleSheet("color: green")
            self.image.setPixmap(QtGui.QPixmap("conn.png")) 

    def disconnecting(self):
        if self.isConnected:
            self.isConnected=False
            self.sock.send(bytes("!Disconn",Format))
            self.server_text.append("disconnected with the SERVER ["+str(self.HOST)+ "] at PORT ["+str(self.PORT)+"]")
            self.state.setText("Disconnected")
            self.state.setStyleSheet("color: red")   
            self.image.setPixmap(QtGui.QPixmap("disconn.png"))

    def listenToServer(self):
        if not self.isConnected:
            self.isConnected=True
            print("connected")
            self.server_text.append(self.sock.recv(1024).decode())
            self.state.setText("Connected")
        else:
            try:
                message = self.sock.recv(1024).decode()
                self.chatting_text.append(message)
            except BlockingIOError :
                print("idle")

    def append_text(self):
        if self.isConnected:
            text=self.Message.text()
            self.sock.send(bytes(text,Format))
            text = '<div style=\" color: black; text-align: left; \" ><p style=\" background-color: white;\">%s</p></div>' % text
            self.Message.clear()

if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Yahoo(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())