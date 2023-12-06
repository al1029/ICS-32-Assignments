import pygame
import sys
from button import Button
from input_box import InputBox

pygame.init()

# Initializing window
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 700
SCREEN = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("Tic-Tac-Toe")

def get_font(size):
    return pygame.font.Font("assets/dpcomic.ttf", size)

def play():

    #Create clock object
    PLAY_CLOCK = pygame.time.Clock()

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the play screen", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(SCREEN_WIDTH//2, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(SCREEN_WIDTH//2, 460), text_input="Back", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.change_color(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.check_for_input(PLAY_MOUSE_POS):
                    main_menu()
    
        pygame.display.update()
        PLAY_CLOCK.tick(30)


def user_info():

    #Creates the input boxes
    PORT_INPUT_BOX = InputBox(x=370, y=300 - 25, width=140, height=50, font=get_font(40), text="")
    IP_INPUT_BOX = InputBox(x=370, y=350 - 25, width=140, height=50, font=get_font(40), text="")
    USERNAME_INPUT_BOX = InputBox(x=370, y =400 - 25, width=140, height=50, font=get_font(40), text="")
    input_boxes = [PORT_INPUT_BOX, IP_INPUT_BOX, USERNAME_INPUT_BOX]

    #Create a clock object
    INFO_CLOCK = pygame.time.Clock()

    while True:
        INFO_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("#4875b7")

        #Creates title text
        INFO_TITLE_TEXT = get_font(45).render("Please enter info", True, "White")
        INFO_TITLE_RECT = INFO_TITLE_TEXT.get_rect(center=(SCREEN_WIDTH//2, 150))
        SCREEN.blit(INFO_TITLE_TEXT, INFO_TITLE_RECT)

        #Creates display text 
        PORT_TEXT = get_font(45).render("Port", True, "White")
        PORT_RECT = PORT_TEXT.get_rect(center=(SCREEN_WIDTH//2 - PORT_INPUT_BOX.width//2, 300))
        SCREEN.blit(PORT_TEXT, PORT_RECT)
        IP_TEXT = get_font(45).render("IP", True, "White")
        IP_RECT = IP_TEXT.get_rect(center=(SCREEN_WIDTH//2 - IP_INPUT_BOX.width//2, 350))
        SCREEN.blit(IP_TEXT, IP_RECT)
        USERNAME_TEXT = get_font(45).render("Username", True, "White")
        USERNAME_RECT = USERNAME_TEXT.get_rect(center=(SCREEN_WIDTH//2 - USERNAME_INPUT_BOX.width//2, 400))
        SCREEN.blit(USERNAME_TEXT, USERNAME_RECT)
        
        #Creates connect button
        INFO_CONNECT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH//2, 500), text_input="CONNECT", font=get_font(75), base_color="White", hovering_color="#b68f40")
        INFO_CONNECT_BUTTON.change_color(INFO_MOUSE_POS)
        INFO_CONNECT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                print("here")
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INFO_CONNECT_BUTTON.check_for_input(INFO_MOUSE_POS):
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

        MENU_TEXT = get_font(120).render("Tic-Tac-Toe", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH//2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH//2, 400), text_input="PLAY", font=get_font(75), base_color="White", hovering_color="#b68f40")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH//2, 550), text_input="QUIT", font=get_font(75), base_color="White", hovering_color="#b68f40")

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
                    user_info()
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        MENU_CLOCK.tick(30)


if __name__ == "__main__":
    main_menu()
