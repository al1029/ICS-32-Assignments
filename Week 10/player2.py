import pygame
import sys
import socket
import threading
from button import Button
from input_box import InputBox
from gameboard import BoardClass
from socket_handler import SocketHandler


def get_font(size):
    return pygame.font.Font("assets/dpcomic.ttf", size)


def play(SCREEN, SCREEN_WIDTH, BOARD, HANDLER, CLIENT_SOCKET):

    #Create clock object
    PLAY_CLOCK = pygame.time.Clock()

    #Get background image
    PLAY_BACKGROUND = pygame.image.load("assets/Board.png")
    X_IMG = pygame.image.load("assets/X.png")
    O_IMG = pygame.image.load("assets/O.png")
    EMPTY_CELL = pygame.image.load("assets/Empty_Cell.png")
    PLAYER_TEXT = get_font(50).render("", True, "White")

    #Player 1 gets first turn
    player_turn = False

    #Set 3 x 3 rect grid
    GRID = [[Button(EMPTY_CELL, (100, 100), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (300, 100), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (500, 100), "", get_font(5), "Black", "White")], 
            [Button(EMPTY_CELL, (100, 300), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (300, 300), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (500, 300), "", get_font(5), "Black", "White")],
            [Button(EMPTY_CELL, (100, 500), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (300, 500), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (500, 500), "", get_font(5), "Black", "White")]]

    #Resets the HANDLER variables
    HANDLER.reset_variables()

    #Create variable for winner
    display_winner = ""

    while True:

        if BOARD.is_winner():
            winner = BOARD.find_winner()
            if winner == "O":
                BOARD.update_wins()
                BOARD.reset_game_board()
                display_winner = BOARD.get_username()
                break
            if winner == "X":
                BOARD.update_losses()
                BOARD.reset_game_board()
                display_winner = BOARD.get_opponent_username()
                break
        if BOARD.board_is_full():
            display_winner = "tie"
            BOARD.reset_game_board()
            break

        #Get mouse position
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        #Set background
        SCREEN.fill("#4875b7")
        SCREEN.blit(PLAY_BACKGROUND, (0,0))

        #Set rect buttons
        for block in GRID:
            for button in block:
                button.update(SCREEN)

        if not player_turn and HANDLER.get_message_state() == False and HANDLER.get_wait_state() == False:
            threading.Thread(target=HANDLER.handle_message, args=(CLIENT_SOCKET,)).start()

        if not player_turn and HANDLER.get_message_state():
            row = HANDLER.get_row()
            col = HANDLER.get_col()
            GRID[row][col].change_image(X_IMG)
            GRID[row][col].update(SCREEN)
            BOARD.place_symbol_ui("X", row, col)
            BOARD.update_turn(BOARD.get_opponent_username())
            HANDLER.reset_variables()
            player_turn = not player_turn

        if not player_turn:
            PLAYER_TEXT = get_font(50).render(f"{BOARD.get_opponent_username()}'s turn...", True, "White")
            PLAYER_TEXT_RECT = PLAYER_TEXT.get_rect(center=(SCREEN_WIDTH//2, 700))
            SCREEN.blit(PLAYER_TEXT, PLAYER_TEXT_RECT)

        if player_turn:
            PLAYER_TEXT = get_font(50).render("Your Turn", True, "White")
            PLAYER_TEXT_RECT = PLAYER_TEXT.get_rect(center=(SCREEN_WIDTH//2, 700))
            SCREEN.blit(PLAYER_TEXT, PLAYER_TEXT_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if player_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for row in range(len(GRID)):
                        for col in range(len(GRID)):
                            button = GRID[row][col]
                            if button.check_for_input(PLAY_MOUSE_POS) and button.image is not X_IMG and button.image is not O_IMG:
                                button.change_image(O_IMG)
                                button.update(SCREEN)
                                CLIENT_SOCKET.send(str(row).encode())
                                CLIENT_SOCKET.send(str(col).encode())
                                BOARD.place_symbol_ui("O", row, col)
                                BOARD.update_turn(BOARD.get_username())
                                player_turn = not player_turn

        pygame.display.update()
        PLAY_CLOCK.tick(30)

    #Wait for 1 second and then move to next screen
    threading.Thread(target=HANDLER.wait_for_time, args=(1,)).start()
    while HANDLER.get_keep_running():

        SCREEN.fill("#4875b7")

        if display_winner == "tie":
            TIE_TEXT = get_font(60).render("The game has tied!", True, "#b68f40")
            TIE_RECT = TIE_TEXT.get_rect(center=(SCREEN_WIDTH//2, 100))
            SCREEN.blit(TIE_TEXT, TIE_RECT)
        else:
            WINNER_TEXT = get_font(60).render(f"{display_winner} has won!", True, "#b68f40")
            WINNER_RECT = WINNER_TEXT.get_rect(center=(SCREEN_WIDTH//2, 100))
            SCREEN.blit(WINNER_TEXT, WINNER_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        PLAY_CLOCK.tick(30)

    HANDLER.reset_variables()
    return "play_again"


def play_again(SCREEN, SCREEN_WIDTH, HANDLER, CLIENT_SOCKET, SERVER_SOCKET):

    #Initialize clock object
    PLAY_AGAIN_CLOCK = pygame.time.Clock()

    #Handle response on new thread
    threading.Thread(target=HANDLER.handle_response, args=(CLIENT_SOCKET,)).start()

    while HANDLER.response_received == False:

        #Set background
        SCREEN.fill("#4875b7")

        #Set title text
        PLAY_AGAIN_TEXT = get_font(70).render(f"Waiting to play again", True, "#b68f40")
        PLAY_AGAIN_RECT = PLAY_AGAIN_TEXT.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(PLAY_AGAIN_TEXT, PLAY_AGAIN_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        PLAY_AGAIN_CLOCK.tick(30)
        
    response = HANDLER.get_response()
    HANDLER.reset_variables()
    if response == "Play Again":
        return "play"
    else:
        SERVER_SOCKET.close()
        return "stats"


def stats(SCREEN, SCREEN_WIDTH, BOARD):

    STATS_CLOCK = pygame.time.Clock()

    username, opponent, num_games, num_wins, num_losses, num_ties = BOARD.compute_stats()

    while True:
        SCREEN.fill("#4875b7")

        STATS_MOUSE_POS = pygame.mouse.get_pos()

        #TODO
        #create text boxes for stats

        QUIT_BUTTON = Button(image=pygame.image.load("assets/Button.png"), pos=(SCREEN_WIDTH//2, 450), text_input="QUIT", font=get_font(75), base_color="White", hovering_color="#b68f40")
        QUIT_BUTTON.change_color(STATS_MOUSE_POS)
        QUIT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.check_for_input(STATS_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        STATS_CLOCK.tick(30)


def user_info(SCREEN, SCREEN_WIDTH, BOARD):

    #Creates the input boxes
    PORT_INPUT_BOX = InputBox(x=320, y=250 - 25, width=140, height=50, font=get_font(40), text="")
    IP_INPUT_BOX = InputBox(x=320, y=300 - 25, width=140, height=50, font=get_font(40), text="")
    input_boxes = [PORT_INPUT_BOX, IP_INPUT_BOX]

    #Create a clock object
    INFO_CLOCK = pygame.time.Clock()

    #Create variable to store socket
    server_socket = ""

    #Creates variable to store error
    error = ""

    while True:
        INFO_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("#4875b7")

        #Creates title text
        INFO_TITLE_TEXT = get_font(80).render("Please enter info", True, "#b68f40")
        INFO_TITLE_RECT = INFO_TITLE_TEXT.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(INFO_TITLE_TEXT, INFO_TITLE_RECT)

        #Creates display text 
        PORT_TEXT = get_font(45).render("Port", True, "White")
        PORT_RECT = PORT_TEXT.get_rect(center=(SCREEN_WIDTH//2 - PORT_INPUT_BOX.width//2, 250))
        SCREEN.blit(PORT_TEXT, PORT_RECT)
        IP_TEXT = get_font(45).render("IP", True, "White")
        IP_RECT = IP_TEXT.get_rect(center=(SCREEN_WIDTH//2 - IP_INPUT_BOX.width//2, 300))
        SCREEN.blit(IP_TEXT, IP_RECT)

        #Creates error text
        ERROR_TEXT = get_font(45).render(error, True, "Red")
        ERROR_RECT = ERROR_TEXT.get_rect(center=(SCREEN_WIDTH//2, 150))
        SCREEN.blit(ERROR_TEXT, ERROR_RECT)
        
        #Creates connect button
        INFO_CONNECT_BUTTON = Button(image=pygame.image.load("assets/Button.png"), pos=(SCREEN_WIDTH//2, 500), text_input="CONNECT", font=get_font(75), base_color="White", hovering_color="#b68f40")
        INFO_CONNECT_BUTTON.change_color(INFO_MOUSE_POS)
        INFO_CONNECT_BUTTON.update(SCREEN)

        #Creates back button
        INFO_BACK_BUTTON = Button(image=pygame.image.load("assets/Button.png"), pos=(SCREEN_WIDTH//2, 650), text_input="BACK", font=get_font(75), base_color="White", hovering_color="#b68f40")
        INFO_BACK_BUTTON.change_color(INFO_MOUSE_POS)
        INFO_BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INFO_CONNECT_BUTTON.check_for_input(INFO_MOUSE_POS):
                    #Attempt to connect to server using info from input boxes
                    ip = IP_INPUT_BOX.get_text()
                    port = PORT_INPUT_BOX.get_text()
                    #Attempts to connect to server
                    try:
                        server_socket = start_server(ip, port)
                    except ValueError:
                        error = "Not a valid port"
                    except socket.error:
                        error = "Could not start server"
                    else:
                        #Sets username
                        BOARD.set_username("Player 2")

                        return ["waiting_for_connection", server_socket]
                if INFO_BACK_BUTTON.check_for_input(INFO_MOUSE_POS):
                    #Returns "" for the client socket since it was not created
                    return ["main_menu", ""]

        for box in input_boxes:
            box.update()
            box.draw(SCREEN)

        #Update the window
        pygame.display.update()
        INFO_CLOCK.tick(30)


def main_menu(SCREEN, SCREEN_WIDTH):

    #Create clock object
    MENU_CLOCK = pygame.time.Clock()

    while True:
        SCREEN.fill("#4875b7")

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(110).render("Tic-Tac-Toe", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH//2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Button.png"), pos=(SCREEN_WIDTH//2, 300), text_input="PLAY", font=get_font(75), base_color="White", hovering_color="#b68f40")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Button.png"), pos=(SCREEN_WIDTH//2, 450), text_input="QUIT", font=get_font(75), base_color="White", hovering_color="#b68f40")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                    return "user_info"
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        MENU_CLOCK.tick(30)


def wait_screen(SCREEN, SCREEN_WIDTH, BOARD, HANDLER, SERVER_SOCKET):

    #Initialize clock
    WAIT_CLOCK = pygame.time.Clock()

    #Handle connection on new thread
    threading.Thread(target=HANDLER.wait_for_connection, args=(SERVER_SOCKET,)).start()

    #Display screen
    while HANDLER.get_connection_state() == False:
        SCREEN.fill("#4875b7")
        CONNECTION_TEXT = get_font(50).render("Waiting for connection...", True, "#b68f40")
        CONNECTION_RECT = CONNECTION_TEXT.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(CONNECTION_TEXT, CONNECTION_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()
        WAIT_CLOCK.tick(30)

    #Set the username of the opponent
    BOARD.set_opponent_username(HANDLER.get_opponent_username())

    return ["play", HANDLER.get_client_socket()]


def start_server(ip, port) -> socket.socket:
    """Creates a server.

    Returns:
        The server socket.
    """

    # Create the server socket
    server_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the game server
    if int(port) < 0 or int(port) > 65535:
        raise ValueError
    server_socket.bind((ip, int(port)))
    return server_socket


def run():

    #Initializing window
    pygame.init()
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe")

    #Creating variable for socket
    SERVER_SOCKET = ""
    CLIENT_SOCKET = ""

    #Initializing game board
    BOARD = BoardClass("Placeholder", "Placeholder")

    #Initializing socket handler
    HANDLER = SocketHandler()

    #Creating variable for screen state
    screen_state = "main_menu"

    #Running game loop
    while True:
        if screen_state == "main_menu":
            screen_state = main_menu(SCREEN, SCREEN_WIDTH)

        if screen_state == "user_info":
            screen_state, SERVER_SOCKET = user_info(SCREEN, SCREEN_WIDTH, BOARD)

        if screen_state == "waiting_for_connection":
            #screen_state, CLIENT_SOCKET = waiting_for_connection(SCREEN, SCREEN_WIDTH, BOARD, SERVER_SOCKET)
            screen_state, CLIENT_SOCKET = wait_screen(SCREEN, SCREEN_WIDTH, BOARD, HANDLER, SERVER_SOCKET)

        if screen_state == "play":
            BOARD.update_games_played()
            screen_state = play(SCREEN, SCREEN_WIDTH, BOARD, HANDLER, CLIENT_SOCKET)

        if screen_state == "play_again":
            screen_state = play_again(SCREEN, SCREEN_WIDTH, HANDLER, CLIENT_SOCKET, SERVER_SOCKET)

        if screen_state == "stats":
            stats(SCREEN, SCREEN_WIDTH, BOARD)


if __name__ == "__main__":
    run()
