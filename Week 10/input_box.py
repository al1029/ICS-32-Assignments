import pygame

class InputBox:
    """An input box class that handles the creation of input boxes for users to type into.
    
    Attributes:
        width (int): the width of the input box.
        rect (pygame.Rect): the rectangle object on which the text is drawn on.
        color (pygame.Color): the color of the input box when it is not selected.
        text (str): the text shown on the input box.
        font (pygame.font): the font of the text.
        text_surface (pygame.font): the surface on which the text is placed on.
        active (bool): A boolean to show whether the button has been clicked and currently selected.
    """

    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font, text: str =""):
        """Creates an InputBox object.
        
        Args:
            x: the x position of the input box.
            y: the y position of the input box.
            width: the width of the input box.
            height: the height of the input box.
            font: the font of the input box.
            text: the text on the input box
        """

        self.width = width
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color("#3c6bc3")
        self.text = text
        self.font = font
        self.text_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event: pygame.event) -> None:
        """Handles when an input box is selected and written in.
        
        Args:
            event: the current event on the screen.
        """

        #If the user clicked on the input box
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color("#3145ce") if self.active else pygame.Color("#3c6bc3")

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
        

    def update(self) -> None:
        """Updates the size of the input box if the text is longer than the box.
        
        """

        width = max(200, self.text_surface.get_width()+10)
        self.rect.w = width


    def get_text(self) -> str:
        return self.text


    def draw(self, screen: pygame.display) -> None:
        """Draws the input box on the screen.
        
        Args:
            screen: the display screen.
        """

        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 5)

        
