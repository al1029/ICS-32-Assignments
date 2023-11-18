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
    """Creates a client socket and connects to the game server.

    Prompts the user for the IP address and port of the host. Does 
    not finish running until both the server address is valid and 
    the player is connected to the game server. If the client fails
    to connect to the server the user is prompted if they would like 
    to try again. If they do not the program is closed, otherwise the 
    function runs again.

    Returns:
        The client socket.
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
                    sys.exit(0)
                print("Please provide a valid response")
        else:
            break
    print(f"Successfully connected to {server_address}")
    return client_socket


def main() -> None:
    """Runs the game and catches any connection interrupted errors.
    
    If the connection is not interrupted, the game runs as normal. If the connection
    is interrupted at any point the user is prompted if they wan to reconnect. if they do,
    they are prompted for the host information to reconnect, else the program is terminated.
    """

    while True:
        # Creates the client socket
        client_socket = start_client()

        # Prompts the user for an alphanumerical username
        player_username, opponent_username = get_user_names(client_socket)
        
        # Begins to play the game
        try:
            play_game(client_socket, player_username, opponent_username)
        except ConnectionResetError:
            print("The server was forcibly closed\n")
            response = ""
            while True:
                response = input("Would you like to reconnect to the server? y/n: ").strip().lower()
                if response == "y" or response == "n":
                    break
                else:
                    print("Not a valid response")
            if response == "y":
                continue
            else:
                print("Closing the program")
                break

        # Breaks out of the loop when player decides to leave
        client_socket.close()
        break


def play_game(socket: socket.socket, username: str, opponent: str) -> None:
    """Runs the game loop and logic of the game.

    Player 1 takes turns with Player 2 playing tic-tac-toe. Uses the BoardClass
    to keep score and create the tic-tac-toe board.

    Args:
        socket: the client socket.
        username: the username of the Player 1.
        opponent: the username of Player 2.
    """

    # Gets the socket, username, and opponent username
    client_socket = socket
    player_username = username
    opponent_username = opponent

    # Creates the gameboard
    board = BoardClass(player_username, opponent_username)

    # Prints the game instructions
    display_instructions()
    
    # Plays the game until the game is over and the user decides to leave
    board.update_games_played()
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
        state = check_state(board)
        if state == "continue":
            client_socket.send(b"continue")
        else:
            if state == "win":
                client_socket.send(b"you lost")
                print(f"!!!{player_username} wins !!!\n")
                board.reset_game_board()
            elif state == "tie":
                client_socket.send(b"tie")
                print("!!! The game has ended in a tie !!!\n")
                board.reset_game_board()

            # Check if the player wants to play again
            response = get_response()
            client_socket.send(response.encode())
            if response == "Play Again":
                board.update_turn("")
                board.update_games_played()
                continue
            else:
                board.print_stats()
                print()
                print("Leaving game...\n")
                break

        # Wait for move from player 2
        print("...Awaiting move from Player 2...\n")
        x_coords = int(client_socket.recv(1024).decode())
        y_coords = int(client_socket.recv(1024).decode())
        board.place_symbol("O", x_coords, y_coords)
        board.update_turn("Player 2")
        print("Player 2 just made a move")
        board.display_board()
        print()

        # Wait for game state from Player 2
        state = client_socket.recv(1024).decode()
        if state != "continue":
            print("In the wrong place")
            if state == "you lost":
                print("!!! Player 2 wins !!!\n")
                board.update_losses()
                board.reset_game_board()
            elif state == "tie":
                print("!!! The game has ended in a tie !!!\n")
                board.update_ties()
                board.reset_game_board()

            # check if player wants to play again
            decision = play_again(client_socket, board)
            if decision == "continue":
                continue
            else:
                break


def display_instructions() -> None:
    paragraph = ("The objective of the game is to align your symbol vertically,\n" + 
                 "horizontally, or diagonally on a 3x3 grid. The grid is accessed\n" + 
                 "using x and y coordinates. x is for the rows and y is for the columns.\n" +
                 "For example, an input of x: 1 and y: 1 will place your symbol in the \n" + 
                 "top left corner. The game is won by the first player to align their\n" +
                 "symbol on the board. If the entire grid is filled without a player\n" +
                 "achieving a winning alignment, the game is a draw. You are the 'X'\n" +
                 "symbol! Good Luck.\n")
    print("\n!!! Welcome to tic-tac-toe !!!\n")
    print(paragraph)


def get_user_names(client_socket: socket.socket) -> tuple:
    """Gets Player 1 username and Player 2 username.

    Prompts the user for an alphanumerical username and retrieves
    Player 2's username.
    
    Args:
        client_socket: the client socket.
    
    Returns:
        A tuple containing the usernames of Player 1 and 2.
    """

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


def get_response() -> str:
    while True:
        response = input("Play again? y/n: ").strip().lower()
        print()
        if response == "y":
            return "Play Again"
        elif response == "n":
            return "Fun Times"
        print("Not a valid response")


def play_again(socket: socket.socket, gameboard: BoardClass) -> str:
    """Checks to see if the player wants to play again.
    
    Handles the logic and updates the game board for if the user wants to 
    play again or not.

    Args:
        socket: the client socket.
        gameboard: the instance of the BoardClass.
    
    Returns:
        'continue' if the user wants to play again.
        'break' if the user does not want to play again.
    """

    board = gameboard
    client_socket = socket

    response = get_response()
    client_socket.send(response.encode())
    if response == "Play Again":
        board.update_turn("")
        board.update_games_played()
        return "continue"
    else:
        board.print_stats()
        print("Leaving game...\n")
        return "break"


def check_state(board: BoardClass) -> str:
    """Checks if the game is won, tied, or neither.
    
    Args:
        board: An instance of the board class

    Returns:
        'win' if player has won.
        'tie' if the game is tied.
        'continue' if the game is neither won nor tied.
    """

    # Check if player has won
    if board.is_winner():
        return "win"
    # Check if the game is tied
    elif board.board_is_full():
        return "tie"
    # Continue the game
    else:
        return "continue"


def get_coords() -> tuple:
    """Retrieves the coordinates from the player.
    
    Prompts the player to input an x and y coordinate within the bounds of the game board.
    Does not stop running until the user inputs a valid coordinate.

    Returns:
        A tuple containing the desired x and y coordinates.
    """

    x = 0
    y = 0
    while True:
        x = input("Input row number: ")
        y = input("Input column number: ")
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
    main()