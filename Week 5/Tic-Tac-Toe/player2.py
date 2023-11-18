"""A module for Player 2 that hosts tic-tac-toe on a socket server.

Player 2 acts as the server for player 1 (client). The user is asked to provide the host 
information so the module can accept incoming requests to start a new game. When a 
connection is established, player 2 and player 1 share information and begin to play 
tic-tac-toe. When the game ends, player 2 will wait for player 1 to idicate if they want
to play again. If player 1 wants to play again then player 2 will wait for player 1's
first move. If player 1 does not want to play again then player 2 will print the 
statistics and terminate the server. 
"""

import socket
from gameboard import BoardClass

def start_server() -> socket.socket:
    """Creates a game server socket.
    
    Prompts the user for the IP address and port for the server. Does not
    finish running until both the server address is valid. 

    Returns:
        The game server socket.
    """

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

    return game_server
    

def main() -> None:
    """Runs the game and catches any connection interrupted errors.
    
    If the connection is not interrupted, the game runs as normal. If the 
    connection is interrupted at any point the user is prompted if they would 
    like to wait for the client to reconnect. If they do, the server listens for 
    a connection, else the program is terminated.
    """

    # Creates the game server socket
    game_server = start_server()

    # Runs the game
    while True:
        try:
            play_game(game_server)
        except (ConnectionResetError, ConnectionAbortedError):
            print("Client forcibly disconnected\n")
            response = ""
            while True:
                response = input("Would you like to wait for the client to reconnect? y/n: ").strip().lower()
                if response == "y" or response == "n":
                    break
                else:
                    print("Not a valid response")
            if response == "y":
                continue
            else:
                print("Closing the program")
                break

        # Breaks out of the loop when player 1 decides to leave
        game_server.close()
        break


def play_game(server: socket.socket) -> None:
    """Runs the game loop and logic of the game.
    
    Player 2 takes turns with Player 1 playing tic-tac-toe. Player 1
    always has the first move. Uses the BoardClass to keep score and create
    the tic-tac-toe board.

    Args:
        server: the game server socket.
    """

    # Gets the game server socket
    game_server = server

    # Wait for a connection
    game_server.listen(1)
    print("Waiting for a connection...")
    client_socket, client_address = game_server.accept()
    print(f"Accepted connection from {client_address}")

    # Get Player 1 username and send Player 2 username
    player_1_username = client_socket.recv(1024).decode()
    client_socket.send(b"Player 2")

    # Creates the gameboard
    board = BoardClass("Player 2", player_1_username)

    # Prints the game instructions
    display_instructions()
    
    # Plays the game until the game is over and Player 1 decides to leave
    board.update_games_played()
    while True:
        # Waits for move from Player 1 and places symbol on game board
        print(f"...Awaiting move from {player_1_username}...\n")
        x_coords = int(client_socket.recv(1).decode())
        y_coords = int(client_socket.recv(1).decode())
        board.place_symbol("X", x_coords, y_coords)
        board.update_turn(player_1_username)
        print(f"{player_1_username} just made a move")
        board.display_board()
        print()

        # Wait for player 1 to give game state
        state = client_socket.recv(1024).decode()
        if state != "continue":
            if state == "you lost":
                print(f"!!! {player_1_username} wins !!!\n")
                board.update_losses()
                board.reset_game_board()
            elif state == "tie":
                print("!!! The game has ended in a tie !!!\n")
                board.update_ties()
                board.reset_game_board()

            # Wait to see if player 1 wants to play again
            response = play_again(client_socket, board, player_1_username)
            if response == "continue":
                continue
            else:
                break  

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
        state = check_state(board)
        if state == "continue":
            client_socket.send(b"continue")
        else:
            if state == "win":
                client_socket.send(b"you lost")
                print("!!! Player 2 wins !!!\n")
                board.reset_game_board()
            elif state == "tie":
                client_socket.send(b"tie")
                print("!!! The game has ended in a tie !!!\n")
                board.reset_game_board()

            # Wait to see if player 1 wants to play again
            response = play_again(client_socket, board, player_1_username)
            if response == "continue":
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
                 "achieving a winning alignment, the game is a draw. You are the 'O'\n" +
                 "symbol! Good Luck.\n")
    print("\n!!! Welcome to tic-tac-toe !!!\n")
    print(paragraph)


def play_again(socket: socket.socket, gameboard: BoardClass, username: str) -> str:
    """Checks player 1 wants to play again.
    
    Handles the logic and updates the game board for if player 1 wants to play or not. 
    If they do, the user is prompted so, else the user is prompted they do not want to 
    play again.

    Args:
        socket: the client socket.
        gameboard: the instance of the BoardClass.
        username: the username of player 1.

    Returns:
        'continue' if player 1 wants to play again.
        'break' if the user does not want to play again.
    """

    client_socket = socket
    board = gameboard
    player_1_username = username

    print(f"Waiting if {player_1_username} wants to play again...\n")
    response = client_socket.recv(1024).decode()
    if response == "Play Again":
        print(f"{player_1_username} wants to play again!\n")
        board.update_turn("")
        board.update_games_played()
        return "continue"
    else:
        print(f"{player_1_username} does not want to play again\n")
        board.print_stats()
        print()
        print("Closing game server...\n")
        return "break"


def check_state(board: BoardClass) -> str:
    """Checks if the game is won, tied, or neither
    
    Parameters:
        board (BoardClass): An instance of the board class.

    Returns:
        'win' if the player has won.
        'tie' if the game is tied.
        'continue' if the game is neither won nor tied.
    """
    # Check if someone has won
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


# Used for testing
if __name__ == "__main__":
    main()