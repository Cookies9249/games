import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.12.2"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()
    
    def get_player(self):
        return self.player
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()  # int (player #) is recv from server
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))  # str (data) is sent to server
            return pickle.loads(self.client.recv(2048))  # object (game) is recv from server
        except socket.error as e:
            print(e)
