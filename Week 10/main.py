import pygame
import sys
from button import Button
from input_box import InputBox

pygame.init()

# Initializing window
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

def get_font(size):
    return pygame.font.Font("assets/dpcomic.ttf", size)


def play():

    #Create clock object
    PLAY_CLOCK = pygame.time.Clock()

    #Get background image
    PLAY_BACKGROUND = pygame.image.load("assets/Board.png")
    X_IMG = pygame.image.load("assets/X.png")
    O_IMG = pygame.image.load("assets/O.png")
    EMPTY_CELL = pygame.image.load("assets/Empty_Cell.png")
    PLAYER_TEXT = get_font(50).render("", True, "White")
    player_turn = True


    #Set 3 x 3 rect grid
    GRID = [[Button(EMPTY_CELL, (100, 100), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (300, 100), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (500, 100), "", get_font(5), "Black", "White")], 
            [Button(EMPTY_CELL, (100, 300), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (300, 300), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (500, 300), "", get_font(5), "Black", "White")],
            [Button(EMPTY_CELL, (100, 500), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (300, 500), "", get_font(5), "Black", "White"), Button(EMPTY_CELL, (500, 500), "", get_font(5), "Black", "White")]]

    while True:

        """Check if there is a winner, if there is then wait 1 second so the player can see and then move to play again? screen
        If there is no winner then continue
        If there is a draw then same as if there was a winner
        """
        #TODO
        #if game_over:
        #   PLAYER_TEXT = get_font(50).render("GAME OVER", True, "White")
        #   SCREEN.blit(PLAYER_TEXT, PLAYER_TEXT_RECT)
        #   pygame.display.update()
        #   make the clock wait one second
        #   play_again()


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
        else:
            PLAYER_TEXT = get_font(50).render("Player 2's Turn...", True, "White")
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
                            if button.check_for_input(PLAY_MOUSE_POS) and button.image is not X_IMG and button.image is not O_IMG :
                                button.change_image(X_IMG)
                                button.update(SCREEN)
                                #TODO
                                #Send player coordinates
                                player_turn = not player_turn
            
        if not player_turn:
            pass
            #TODO
            """wait for player 2 to make a move and send their coordinates.

            """
        """Check if there is a winner, if there is then move to play again? screen
        If there is no winner then continue"""

        pygame.display.update()
        PLAY_CLOCK.tick(30)


def play_again():

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
                    #send to host to play again
                    #TODO
                    play()
                if NO_BUTTON.check_for_input(PLAY_AGAIN_MOUSE_POS):
                    #send to host to not play again
                    #TODO
                    stats()

        pygame.display.update()
        PLAY_AGAIN_CLOCK.tick(30)


def stats():

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


def user_info():

    #Creates the input boxes
    PORT_INPUT_BOX = InputBox(x=320, y=250 - 25, width=140, height=50, font=get_font(40), text="")
    IP_INPUT_BOX = InputBox(x=320, y=300 - 25, width=140, height=50, font=get_font(40), text="")
    USERNAME_INPUT_BOX = InputBox(x=320, y =350 - 25, width=140, height=50, font=get_font(40), text="")
    input_boxes = [PORT_INPUT_BOX, IP_INPUT_BOX, USERNAME_INPUT_BOX]

    #Create a clock object
    INFO_CLOCK = pygame.time.Clock()

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
        
        #Creates connect button
        INFO_CONNECT_BUTTON = Button(image=pygame.image.load("assets/Button.png"), pos=(SCREEN_WIDTH//2, 500), text_input="CONNECT", font=get_font(75), base_color="White", hovering_color="#b68f40")
        INFO_CONNECT_BUTTON.change_color(INFO_MOUSE_POS)
        INFO_CONNECT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INFO_CONNECT_BUTTON.check_for_input(INFO_MOUSE_POS):
                    #TODO
                    #Check if valid username first, then connect
                    #If not a valid username, prompt as such
                    #wait a second since it'll get deleted
                    #if connection is successful:
                    #   create rect that says "Connection successful"
                    #   clock.wait for 1 second
                    #   play()
                    #else:
                    #   create rect that says "Connection unsuccessful"
                    #   clock.wait for 1 second since it'll get deleted
                    #   continue running user_info() (probably just a pass)
                    play()

        for box in input_boxes:
            box.update()
            box.draw(SCREEN)

        #Update the window
        pygame.display.update()
        INFO_CLOCK.tick(30)


def main_menu():

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
                    play()
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        MENU_CLOCK.tick(30)


if __name__ == "__main__":
    main_menu()
