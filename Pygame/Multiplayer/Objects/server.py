import socket
from _thread import *
from player import Player #####
import pickle #####


"""
When client is connected:   Send info from server to client
When client is updated:     Send info from client to server, then info from server to client
"""

def threaded_client(conn, player):
    # If client is connected
    conn.send(pickle.dumps(players[player])) #####

    reply = ""
    while True:
        # If data is recieved
        try:
            data = pickle.loads(conn.recv(2048)) #####
            players[player] = data #####

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0] #####
                else:
                    reply = players[1] #####

                print("Recieved: ", data)
                print("Sending: ", reply)
            
            conn.sendall(pickle.dumps(reply)) #####
        except:
            break
    
    print("Lost Connection")
    conn.close()


# Initialize server
server = "192.168.12.2"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]

# Try to start server
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Wait for clients
s.listen(2)
print("Waiting for a Connection, Server Started")

currentPlayer = 0
while True:
    # If new client is connected
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Start thread
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    currentPlayer %= 2
