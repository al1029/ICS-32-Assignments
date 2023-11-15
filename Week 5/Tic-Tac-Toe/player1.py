"""A module used to play tic-tac-toe as Player 1 using sockets.

Player 1 acts as the client and asks Player 2 (server) for the host information. If 
connection is successful, Player 1 and Player 2 exchange usernames and begin playing 
tic-tac-toe using the BoardClass. Once the game ends, Player 1 is prompted if they want
to play again. If they say yes a new game starts, if they say no the client disconnects 
from the server and Player 1 stats are displayed.
"""

import socket

def start_client():

    client_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the game server
    while True:
        try:
            game_server = input("Please input the server IP: ")
            server_port = input("Please input the server port: ")
            server_port = int(server_port)
            if server_port < 0 or server_port >65535:
                raise ValueError
            server_address = (game_server, server_port)
            client_socket.connect(server_address)
        except ValueError:
            print("Not a valid port number")
        except ConnectionRefusedError:
            print("Could not connect to server")
        else:
            break

    data = client_socket.recv(1024).decode()
    print(data)
    client_socket.send(b"world")
    client_socket.close()

if __name__ == "__main__":
    start_client()