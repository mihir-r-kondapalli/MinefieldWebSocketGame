import socket
from _thread import *
from player import Player
from player import Goal
import pickle
import data
import random
from protocol import data_protocol

server = open("ipconfig").read().strip()
port = 5555


s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def gen_min_locs():
    mine_locs = []
    for i in range(0, data.NUM_OF_MINES):
        xr = random.randint(5, data.WINDOW_W-5)
        yr = random.randint(5, data.WINDOW_H-5)

        while (xr<2*Player.GOAL_SIZE and yr<2*Player.GOAL_SIZE) or (xr>data.WINDOW_W-2*Player.GOAL_SIZE and yr>data.WINDOW_H-2*Player.GOAL_SIZE):
            xr = random.randint(5, data.WINDOW_W-5)
            yr = random.randint(5, data.WINDOW_H-5)

        mine_locs.append(xr)
        mine_locs.append(yr)

    text = ''
    for i in range(0, len(mine_locs)):
        text += str(mine_locs[i])
        text += ','
    return text[0: len(text)-1]

goal1 = Goal(data.WINDOW_W-Player.GOAL_SIZE, data.WINDOW_H-Player.GOAL_SIZE, data.WINDOW_W-Player.GOAL_SIZE*2, data.WINDOW_H-Player.GOAL_SIZE*2, data.GOAL_COLOR1)
goal2 = Goal(0, 0, 0, 0, data.GOAL_COLOR2)

player1 = Player("Player 1", data.SX1, data.SY1, data.COLOR1, goal1)
player2 = Player("Player 2", data.SX2, data.SY2, data.COLOR2, goal2)

players = [player1, player2]

datas = [data_protocol(data.SX1, data.SY1, -1, 0), data_protocol(data.SX2, data.SY2, -1, 0)]

num_players = 0

mine_str = ''

def threaded_client(conn, player):

    print('New Player!')

    global num_players
    global datas
    if(player%2 == 0):
        conn.sendall(pickle.dumps(players[0]))
        conn.sendall(pickle.dumps(players[1]))
    else:
        conn.sendall(pickle.dumps(players[1]))
        conn.sendall(pickle.dumps(players[0]))

    print(conn.recv(15).decode())
    # Sending mine map
    conn.sendall(str.encode(mine_str))

    while(num_players < 2):
        pass

    reply = ""
    while True:
        try:
            data = conn.recv(32).decode()

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    datas[1] = data
                    reply = datas[0]
                else:
                    datas[0] = data
                    reply = datas[1]

                #print("Received: ", data)
                #print("Sending : ", reply)

            conn.send(str.encode(reply))
        except:
            break

    print("Lost connection")
    num_players -= 1
    conn.close()

init_conn = False
currentPlayer = 0

s.settimeout(3)

mine_str = gen_min_locs()

while True:

    try:
        conn, addr = s.accept()

        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
        num_players += 1

        init_conn = True

    except socket.timeout:
        if(num_players <= 0):
            print("timeout")
            if(init_conn):
                print("Closing Server")
                break