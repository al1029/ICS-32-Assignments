"""A module used to play tic-tac-toe as Player 1 using sockets.

Player 1 acts as the client and asks Player 2 (server) for the host information. If 
connection is successful, Player 1 and Player 2 exchange usernames and begin playing 
tic-tac-toe using the BoardClass. Once the game ends, Player 1 is prompted if they want
to play again. If they say yes a new game starts, if they say no the client disconnects 
from the server and Player 1 stats are displayed.
"""

import socket
import sys
from gameboard import BoardClass

def start_client() -> socket.socket:
    """Creates a client socket and connects the the game server.

    Prompts the user for the IP address and port of the host. Does 
    not finish running until both the server address is valid and 
    the player is connected to the game server. If the client fails
    to connect to the server the user is prompted if they would like 
    to try again. If they do not the program is closed, otherwise the 
    function runs again.

    Returns:
        The client socket
    """

    # Create the client socket
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
        except (ConnectionRefusedError, socket.gaierror):
            print("Could not connect to server")
            # Asks the user if they would like to try again
            while True:
                try_again = input("Try again? (y/n): ").strip().lower()
                if try_again == "y":
                    break
                elif try_again == "n":
                    # Safely terminates the program
                    print("Closing the program...")
                    sys.exit(1)
                print("Please provide a valid response")
        else:
            break
    print(f"Successfully connected to {server_address}")
    return client_socket


def start_game() -> None:

    # Creates the client socket
    client_socket = start_client()

    # Prompts the user for an alphanumerical username
    player_username, opponent_username = get_user_names(client_socket)

    # Creates the gameboard
    board = BoardClass(player_username, opponent_username)

    # Prints the game instructions
    display_instructions()
    
    # Plays the game until the game is over and the user decides to leave
    while True:
        # Prompt user for coordinates and places symbol on game board
        print(f"Your ({player_username}) turn to make a move. Inputs should be integers in range 1-3 (inclusive).")
        x_coords, y_coords = (0,0)
        while True:
            x_coords, y_coords = get_coords()
            # Check if the play is valid
            if board.valid_play(x_coords, y_coords):
                break
            print("Not a valid play")
        board.place_symbol("X", x_coords, y_coords)
        board.update_turn(player_username)
        board.display_board()
        print()
        # Send coords to player 2
        client_socket.send(str(x_coords).encode())
        client_socket.send(str(y_coords).encode())

        # Check the state of the game
        state = check_state(board, True)
        if state != "continue":
            if state == "win":
                print(f"!!!{player_username} wins !!!\n")
                board.reset_game_board()
            elif state == "lose":
                print("!!! Player 2 wins !!!\n")
                board.reset_game_board()
            elif state == "tie":
                print("!!! The game has ended in a tie !!!\n")
                board.reset_game_board()

            # Check if the player wants to play again
            response = play_again(client_socket)
            client_socket.send(response.encode())
            if response == "y":
                board.update_turn("")
                continue
            else:
                print("Leaving game...\n")
                board.print_stats()
                client_socket.close()
                sys.exit(1)

        # Wait for move from player 2
        print("...Awaiting move from Player 2...\n")
        x_coords = int(client_socket.recv(1024).decode())
        y_coords = int(client_socket.recv(1024).decode())
        board.place_symbol("O", x_coords, y_coords)
        board.update_turn("Player 2")
        print("Player 2 just made a move")
        board.display_board()
        print()

        # Check the state of the game
        state = check_state(board, False)
        if state != "continue":
            if state == "win":
                print(f"!!!{player_username} wins !!!\n")
                board.reset_game_board()
            elif state == "lose":
                print("!!! Player 2 wins !!!\n")
                board.reset_game_board()
            elif state == "tie":
                print("!!! The game has ended in a tie !!!\n")
                board.reset_game_board()

            # Check if the player wants to play again
            response = play_again(client_socket)
            client_socket.send(response.encode())
            if response == "y":
                board.update_turn("")
                continue
            else:
                print("Leaving game...\n")
                board.print_stats()
                client_socket.close()
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


def get_user_names(client_socket: socket.socket) -> tuple:
    player_username = ""
    while True:
        player_username = input("Please enter an alphanumerical username: ").strip()
        if player_username.isalnum():
            break
        else:
            print("Not a valid username")
    
    # Send Player 1 username and receive Player 2 username
    client_socket.send(player_username.encode())
    opponent_username = client_socket.recv(1024).decode()

    return player_username, opponent_username


def play_again(client_socket: socket.socket) -> str:
    while True:
        response = input("Play again? y/n: ").strip().lower()
        print()
        if response == "y" or response == "n":
            return response
        print("Not a valid response")


def check_state(board: BoardClass, player_1: bool) -> str:
    """Checks if the game is won, tied, or neither
    
    Parameters:
        - board (BoardClass): An instance of the board class
        - player_1 (bool): A boolean used to tell if Player 1 has won or lost

    Returns:
        str:
            - 'win' if player 1 has won
            - 'lose' if player 1 has lost
            - 'tie' if the game is tied
            - 'continue' if the game is neither won, lost, nor tied
    """
    # Check if someone has won
    if board.is_winner():
        if player_1:
            return "win"
        else:
            return "lose"
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