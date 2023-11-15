"""A module for player 2 that hosts tic-tac-toe on a socket server.

Player 2 acts as the server for player 1 (client). The user is asked to provide the host 
information so the module can acept incoming requests to start a new game. When a 
connection is established, player 2 and player 1 share information and begin to play 
tic-tac-toe. When the game ends, player 2 will wait for player 1 to idicate if they want
to play again. If player 1 wants to play again then player 2 will wait for player 1's
first move. If player 1 does not want to play again then player 2 will print the 
statistics and terminate the server.
"""

import socket

def start_server():

    game_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Start a game server
    while True:
        try:
            server_ip = input("Please input the desired server IP (127.0.0.1 recommended): ")
            server_port = input("Please input the desired port number between 0-65535 inclusive (5 digits): ")
            server_port = int(server_port)
            # Bind the socket to a specific address and port
            server_address = (server_ip, server_port)
            game_server.bind(server_address)
        except ValueError:
            print("Not a valid port number")
        except socket.error:
            print("There was an error starting the server with the provided address")
        else:
            if 0 <= server_port <= 65535:
                break
            else:
                print("Port number not in range")

    game_server.listen(1)
    print(f"Server is listening on {server_address}")
   
    # Wait for a connection
    print("Waiting for a connection...")
    client_socket, client_address = game_server.accept()
    print(f"Accepted connection from {client_address}")

    client_socket.send(b"hello")
    client_message = client_socket.recv(1024).decode()
    print(client_message)
    game_server.close()

    

    

if __name__ == "__main__":
    start_server()