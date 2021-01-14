from sys import argv
from gui import *
import threading
import socket
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
import cv2 as cv

Format ='utf-8'


class Yahoo(Ui_MainWindow):
    def __init__(self,mainwindow):
        super(Yahoo,self).setupUi(mainwindow)
        self.Message.returnPressed.connect(self.append_text)
        self.send.clicked.connect(self.append_text)
        self.connect.clicked.connect(self.connecting)
        self.disconnect.clicked.connect(self.disconnecting)
        self.isConnected=False
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.recv)
        # self.timer.start()
    def connecting(self):
        if not self.isConnected:
            self.isConnected=True
            self.client=socket.socket()
            self.client.connect(('localhost',9999))
            print("connected")
            self.server_text.append(self.client.recv(1024).decode())
            self.state.setText("Connected")
            self.state.setStyleSheet("color: green")
            self.image.setPixmap(QtGui.QPixmap("conn.png")) 
            self.thread=threading.Thread(target=self.recv,args=(self.client,"c")) 
            self.thread.start()
    def disconnecting(self):
        if self.isConnected:
            self.isConnected=False
            self.thread.close()
            self.client.send(bytes(str(len("!Disconn")),Format))
            self.client.send(bytes("!Disconn",Format))
            self.server_text.append(self.client.recv(1024).decode())
            self.state.setText("Disconnected")
            self.state.setStyleSheet("color: red")   
            self.image.setPixmap(QtGui.QPixmap("disconn.png"))

    def append_text(self):
        if self.isConnected:
            text=self.Message.text()
            self.client.send(bytes(str(len(text)),Format))
            self.client.send(bytes(text,Format))
            text = '<div style=\" color: black; text-align: left; \" ><p style=\" background-color: white;\">%s</p></div>' % text
            self.chatting_text.append(text)
            self.chatting_text.append(self.client.recv(1024).decode())
            self.Message.clear()
   
    def recv(self,client,sttring):
        while True:
            if self.isConnected:
                print("before")
                text=self.client.recv(1024).decode()
                print(text)
if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Yahoo(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())