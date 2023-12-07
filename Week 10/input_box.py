import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
INACTIVE_COLOR = pygame.Color("#3c6bc3")
ACTIVE_COLOR = pygame.Color("#3145ce")

class InputBox:
    def __init__(self, x, y, width, height, font, text=""):
        self.width = width
        self.rect = pygame.Rect(x, y, width, height)
        self.color = INACTIVE_COLOR
        self.text = text
        self.font = font
        self.text_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):

        #If the user clicked on the input box
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = ACTIVE_COLOR if self.active else INACTIVE_COLOR

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.text_surface = self.font.render(self.text, True, self.color)
        

    def update(self):
        width = max(200, self.text_surface.get_width()+10)
        self.rect.w = width


    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 5)

        
