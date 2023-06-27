import socket

"""
Initialize: Network.client.connect(addr)
To Recieve: Network.client.recv(2048).decode()
To Send     Network.client.send(str.encode(data))
"""

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.12.2"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()
    
    def get_pos(self):
        return self.pos
    
    def connect(self):
        try:
            self.client.connect(self.addr)  # Try to connect to server
            return self.client.recv(2048).decode()  # Recieve and return pos message (1)
        except:
            pass
    
    def send(self, data):
        # To send encoded data
        try:
            self.client.send(str.encode(data))  # Try to send data
            return self.client.recv(2048).decode()  # Recieve and return original data (2)
        except socket.error as e:
            print(e)
