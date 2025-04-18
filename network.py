import socket
import pickle
import player as Player
import sys

class Network:
    def __init__(self, server):
        self.client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.server = server
        self.port = 5555
        self.addr = (self.server, self.port)
        self.init_connect()
        if self.p == None:
            print('fatal: failed to read player objects')
            self.client.close()

    def getInitData(self):
        return [self.p, self.opp]
    
    def getPosData(self):
        data = self.connect()
        if(data == None):
            return None
        return data.split(",")

    def init_connect(self):
        try:
            self.client.connect(self.addr)
            self.p = pickle.loads(self.client.recv(4096))
            self.opp = pickle.loads(self.client.recv(4096))
            self.client.send(str.encode("hi"))
        except Exception as e:
            print(e)
            self.p = None
            self.opp = None
            print("Can't connect to server!")
            exit()

    def getMineString(self):
        try:
            return self.client.recv(2048).decode()
        except:
            pass

    # x, y, mx, my
    def connect(self):
        try:
            #self.client.connect(self.addr)
            return self.client.recv(48).decode()
        except:
            pass

    # x, y, mx, my
    def send(self, data):
        self.client.send(str.encode(data))

    def close(self):
        self.client.close()