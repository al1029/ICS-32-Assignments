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
import sys
from gameboard import BoardClass

def start_server() -> tuple:

    # Creates the game server socket
    game_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Starts the game server
    while True:
        try:
            server_ip = input("Please input the desired server IP (127.0.0.1 recommended): ")
            server_port = input("Please input the desired port number between 0-65535 inclusive (5 digits): ")
            server_port = int(server_port)
            if server_port < 0 or server_port >65535:
                raise ValueError
            # Bind the socket to a specified address and port
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
   
    # Wait for a connection
    game_server.listen(1)
    print(f"Server is listening on {server_address}")
    print("Waiting for a connection...")
    client_socket, client_address = game_server.accept()
    print(f"Accepted connection from {client_address}")

    return game_server, client_socket
    
def start_game() -> None:

    # Creates the game server socket
    game_server, client_socket = start_server()

    # Get Player 1 username and send Player 2 username
    player_1_username = client_socket.recv(1024).decode()
    print("got to here")
    client_socket.send(b"Player 2")

    # Creates the gameboard
    board = BoardClass("Player 2", player_1_username)

    # Prints the game instructions
    display_instructions()
    
    # Plays the game until the game is over and Player 1 decides to leave
    board.update_games_played()
    while True:
        # Wait for move from Player 1
        print(f"...Awaiting move from {player_1_username}...\n")
        x_coords = int(client_socket.recv(1024).decode())
        y_coords = int(client_socket.recv(1024).decode())
        board.place_symbol("X", x_coords, y_coords)
        board.update_turn(player_1_username)
        print(f"{player_1_username} just made a move")
        board.display_board()
        print()

        # Check the state of the game
        state = check_state(board, True)
        if state != "continue":
            if state == "win":
                print("!!! Player 2 wins !!!\n")
                board.update_wins()
                board.reset_game_board()
            elif state == "lose":
                print(f"!!! {player_1_username} wins !!!\n")
                board.update_losses()
                board.reset_game_board()
            elif state == "tie":
                print("!!! The game has ended in a tie !!!\n")
                board.update_ties()
                board.reset_game_board()

            # Wait to see if player 1 wants to play again
            response = client_socket.recv(1024).decode()
            if response == "y":
                board.update_turn("")
                board.update_games_played()
                continue
            else:
                print("Closing game server...")
                board.print_stats()
                game_server.close()
                sys.exit(1)

        # Prompt user for coordinates and places symbol on game board
        print(f"Your (Player 2) turn to make a move. Inputs should be integers in range 1-3 (inclusive).")
        x_coords, y_coords = (0,0)
        while True:
            x_coords, y_coords = get_coords()
            # Check if the play is valid
            if board.valid_play(x_coords, y_coords):
                break
            print("Not a valid play")
        board.place_symbol("O", x_coords, y_coords)
        board.update_turn("Player 2")
        board.display_board()
        print()
        # Send coords to player 1
        client_socket.send(str(x_coords).encode())
        client_socket.send(str(y_coords).encode())

        # Check the state of the game
        state = check_state(board, False)
        if state != "continue":
            if state == "win":
                print("!!! Player 2 wins !!!\n")
                board.reset_game_board()
            elif state == "lose":
                print(f"!!! {player_1_username} wins !!!\n")
                board.reset_game_board()
            elif state == "tie":
                print("!!! The game has ended in a tie !!!\n")
                board.reset_game_board()

            # Wait to see if player 1 wants to play again
            response = client_socket.recv(1024).decode()
            if response == "y":
                board.update_turn("")
                continue
            else:
                print("Closing game server...")
                board.print_stats()
                game_server.close()
                sys.exit(1)


def display_instructions() -> None:
    paragraph = """The objective of the game is to align your symbol vertically,
                   horizontally, or diagonally on a 3x3 grid. The grid is accessed
                   using x and y coordinates. x is for the rows and y is for the columns.
                   For example, an input of x: 1 and y: 1 will place yor symbol in the
                   top left corner. The game is one by the first player to align their
                   symbol on the board. If the entire grid is filled without a player
                   achieving a winning alignment, the game is a draw. You are the 'X'
                   symbol! Good Luck.\n
                """
    print("\n!!! Welcome to tic-tac-toe !!!\n")
    print(paragraph)


def check_state(board: BoardClass, player_1: bool) -> str:
    """Checks if the game is won, tied, or neither
    
    Parameters:
        - board (BoardClass): An instance of the board class
        - player_1 (bool): A boolean used to tell if Player 1 has won or lost

    Returns:
        str:
            - 'lose' if player 1 has won
            - 'win' if player 1 has lost
            - 'tie' if the game is tied
            - 'continue' if the game is neither won, lost, nor tied
    """
    # Check if someone has won
    if board.is_winner():
        if player_1:
            return "lose"
        else:
            return "win"
    # Check if the game is tied
    elif board.board_is_full():
        return "tie"
    # Continue the game
    else:
        return "continue"


def get_coords() -> tuple:
    x = 0
    y = 0
    while True:
        x = input("Input x coord: ")
        y = input("Input y coord: ")
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            print("Not valid coordinates")
        else:
            if 0 < x < 4 and 0 < y < 4:
                break
            else:
                print("Not valid coordinates")
    return x, y


if __name__ == "__main__":
    start_game()