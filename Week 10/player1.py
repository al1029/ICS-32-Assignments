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
    player_turn = True

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
            if winner == "X":
                BOARD.update_wins()
                BOARD.reset_game_board()
                display_winner = BOARD.get_username()
                break
            if winner == "O":
                BOARD.update_losses()
                BOARD.reset_game_board()
                display_winner = BOARD.get_opponent_username()
                break
        if BOARD.board_is_full():
            BOARD.reset_game_board()
            display_winner = "tie"
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

        if player_turn:
            PLAYER_TEXT = get_font(50).render("Your Turn", True, "White")
            PLAYER_TEXT_RECT = PLAYER_TEXT.get_rect(center=(SCREEN_WIDTH//2, 700))
            SCREEN.blit(PLAYER_TEXT, PLAYER_TEXT_RECT)

        if not player_turn:
            PLAYER_TEXT = get_font(50).render("Player 2's Turn...", True, "White")
            PLAYER_TEXT_RECT = PLAYER_TEXT.get_rect(center=(SCREEN_WIDTH//2, 700))
            SCREEN.blit(PLAYER_TEXT, PLAYER_TEXT_RECT)

        if not player_turn and HANDLER.get_message_state() == False and HANDLER.get_wait_state() == False:
            threading.Thread(target=HANDLER.handle_message, args=(CLIENT_SOCKET,)).start()

        if not player_turn and HANDLER.get_message_state():
            row = HANDLER.get_row()
            col = HANDLER.get_col()
            GRID[row][col].change_image(O_IMG)
            GRID[row][col].update(SCREEN)
            BOARD.place_symbol_ui("O", row, col)
            BOARD.update_turn(BOARD.get_opponent_username())
            HANDLER.reset_variables()
            player_turn = not player_turn

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
                                button.change_image(X_IMG)
                                button.update(SCREEN)
                                CLIENT_SOCKET.send(str(row).encode())
                                CLIENT_SOCKET.send(str(col).encode())
                                BOARD.place_symbol_ui("X", row, col)
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


def play_again(SCREEN, SCREEN_WIDTH, CLIENT_SOCKET):

    PLAY_AGAIN_CLOCK = pygame.time.Clock()

    while True:

        #Get mouse position
        PLAY_AGAIN_MOUSE_POS = pygame.mouse.get_pos()

        #Set background
        SCREEN.fill("#4875b7")

        #Set title text
        PLAY_AGAIN_TEXT = get_font(110).render("Play again?", True, "#b68f40")
        PLAY_AGAIN_RECT = PLAY_AGAIN_TEXT.get_rect(center=(SCREEN_WIDTH//2, 100))

        YES_BUTTON = Button(image=pygame.image.load("assets/Button.png"), pos=(SCREEN_WIDTH//2, 300), text_input="YES", font=get_font(75), base_color="White", hovering_color="#b68f40")
        NO_BUTTON = Button(image=pygame.image.load("assets/Button.png"), pos=(SCREEN_WIDTH//2, 500), text_input="NO", font=get_font(75), base_color="White", hovering_color="#b68f40")
        
        SCREEN.blit(PLAY_AGAIN_TEXT, PLAY_AGAIN_RECT)

        for button in [YES_BUTTON, NO_BUTTON]:
            button.change_color(PLAY_AGAIN_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if YES_BUTTON.check_for_input(PLAY_AGAIN_MOUSE_POS):
                    CLIENT_SOCKET.send(b"Play Again")
                    return "play"
                if NO_BUTTON.check_for_input(PLAY_AGAIN_MOUSE_POS):
                    CLIENT_SOCKET.send(b"Fun Times")
                    CLIENT_SOCKET.close()
                    return "stats"

        pygame.display.update()
        PLAY_AGAIN_CLOCK.tick(30)


def stats(SCREEN, SCREEN_WIDTH):

    STATS_CLOCK = pygame.time.Clock()

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
    USERNAME_INPUT_BOX = InputBox(x=320, y =350 - 25, width=140, height=50, font=get_font(40), text="")
    input_boxes = [PORT_INPUT_BOX, IP_INPUT_BOX, USERNAME_INPUT_BOX]

    #Create a clock object
    INFO_CLOCK = pygame.time.Clock()

    #Create variable to store socket
    client_socket = ""

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
        USERNAME_TEXT = get_font(45).render("Username", True, "White")
        USERNAME_RECT = USERNAME_TEXT.get_rect(center=(SCREEN_WIDTH//2 - USERNAME_INPUT_BOX.width//2, 350))
        SCREEN.blit(USERNAME_TEXT, USERNAME_RECT)

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
                    username = USERNAME_INPUT_BOX.get_text()
                    ip = IP_INPUT_BOX.get_text()
                    port = PORT_INPUT_BOX.get_text()
                    #Checks if username is alphanumerical
                    if username.isalnum():
                        #Attempts to connect to server
                        try:
                            client_socket = start_client(ip, port)
                        except ValueError:
                            error = "Not a valid port"
                        except (ConnectionRefusedError, socket.gaierror, OSError):
                            error = "Could not connect to server"
                        else:
                            #Sets usernames
                            BOARD.set_username(username)
                            client_socket.send(username.encode())
                            BOARD.set_opponent_username(client_socket.recv(1024).decode())

                            return ["play", client_socket]
                    else:
                        error = "Not an alphanumerical username"
                        ERROR_TEXT = get_font(45).render(error, True, "Red")
                        ERROR_RECT = ERROR_TEXT.get_rect(center=(SCREEN_WIDTH//2, 150))
                        SCREEN.blit(ERROR_TEXT, ERROR_RECT)
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


def start_client(ip, port) -> socket.socket:
    """Creates a client socket and connects to the game server.

    Attempts to connect to the server

    Returns:
        The client socket.
    """

    # Create the client socket
    client_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the game server
    if int(port) < 0 or int(port) > 65535:
        raise ValueError
    client_socket.connect((ip, int(port)))
    return client_socket


def run():

    #Initializing window
    pygame.init()
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe")

    #Creating variable for socket
    CLIENT_SOCKET = ""

    #Initializing game board
    BOARD = BoardClass("Placeholder", "Placeholder")

    #Creating variable for screen state
    screen_state = "main_menu"

    HANDLER = SocketHandler()

    #Running game loop
    while True:
        if screen_state == "main_menu":
            screen_state = main_menu(SCREEN, SCREEN_WIDTH)

        if screen_state == "user_info":
            screen_state, CLIENT_SOCKET = user_info(SCREEN, SCREEN_WIDTH, BOARD)

        if screen_state == "play":
            BOARD.update_games_played()
            screen_state = play(SCREEN, SCREEN_WIDTH, BOARD, HANDLER, CLIENT_SOCKET)

        if screen_state == "play_again":
            screen_state = play_again(SCREEN, SCREEN_WIDTH, CLIENT_SOCKET)

        if screen_state == "stats":
            stats(SCREEN, SCREEN_WIDTH)


if __name__ == "__main__":
    run()
