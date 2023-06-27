import socket
from _thread import *


# Convert from string to tuple
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


# Conver from tuple to string
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def threaded_client(conn, player):
    # If client is accepted
    conn.send(str.encode(make_pos(pos[player])))  # Send pos of player

    reply = ""
    while True:
        # If data is sent to server
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Recieved: ", data)  # Output data
                print("Sending: ", reply)
            
            conn.sendall(str.encode(make_pos(reply)))  # Send data back (2)
        except:
            break
    
    print("Lost Connection")
    conn.close()


# Initialize server
server = "192.168.12.2"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pos = [(0,0),(100,100)]

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
