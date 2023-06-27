import socket
from _thread import *
import pickle
from game import Game


def threaded_client(conn, player, gameId):
    global idCount

    # If client is connected
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        # If data is recieved
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(player, data)
                        print(f"Game {gameId}: Player {player} Picked {data}")

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break
    
    print(f"Game {gameId}: Lost Connection")
    try:
        del games[gameId]
        print(f"Game {gameId}: Closing Game")
    except:
        pass
    idCount -= 1
    conn.close()


# Initialize server
server = "192.168.12.2"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to start server
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Wait for clients
s.listen()
print("Waiting for a Connection, Server Started")

# Initialize games
connected = set()
games = {}
idCount = 0

currentPlayer = 0
while True:
    # If new client is connected
    conn, addr = s.accept()

    idCount += 1
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1: # If new game needs to be created
        games[gameId] = Game(gameId)
        print(f"Game {gameId}: Creating New Game...")
        p = 0
    else:
        games[gameId].ready = True
        p = 1
    
    print(f"Game {gameId}: Connected to {addr} as Player {p}")
    
    # Start thread
    start_new_thread(threaded_client, (conn, p, gameId))
