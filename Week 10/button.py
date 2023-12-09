import pygame

class Button():
    """A button class that handles the creation of a usable button for a pygame display.
    
    Attributes:
        image (pygame.image): an image to display.
        x_pos (int): the x position on the screen.
        y_pos (int): the y position on the screen.
        font (pygame.font): the desired font for the text.
        base_color (pygame.Color): the color of the text.
        hovering_color (pygame.Color): the color displayed when the button is hovered over.
        text_input (str): the text displayed on the button.
        rect (Rect): the rectangle object used to display the image.
        text_rect (Rect): the rectangle object used to display the text.
    """

    def __init__(self, image: pygame.image, pos: tuple, text_input: str, font: pygame.font, base_color: pygame.Color, hovering_color: pygame.Color):
        """Creates a Button class object.
        
        Args:
            image: the image to be displayed.
            pos: the coordinate to display the button on the screen.
            text_input: the text displayed on the screen.
            font: the font of the text.
            base_color: the color of the base text.
            hovering_color: the color displayed when the button is hovered over.
        """
        
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen: pygame.display) -> None:
        """Updates the button on the screen.
        
        Args:
            screen: the display screen.
        """

        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def change_image(self, image):
        self.image = image


    def change_text(self, text):
        self.text = text


    def check_for_input(self, position: tuple) -> bool:
        """Checks if the mouse is hovering over the text.

        Args:
            position: the position of the mouse

        Returns: 
            True if the mouse is hovering over the button.
            False otherwise.
        """

        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def change_color(self, position: tuple)-> None:
        """Changes color to hovering color if mouse if over the button.

        Args:
            position: the position of the mouse
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)