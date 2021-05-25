import pygame


class Button():
    """
    Class for creating buttons for starting and end screen
    """

    def __init__(self, x: int, y: int, image: pygame.Surface, scale: float):
        """

        :param x: x location of the button on the screen
        :param y: y location of the button on the screen
        :param image: image that you want to use for the button
        :param scale: scale factor to resize the button image
        """
        width = image.get_width() # get width of image
        height = image.get_height() # get height of image
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) # scale image
        self.rect = self.image.get_rect() # get rectangle
        self.rect.topleft = (x, y) # put topleft of rectangle at certain position
        self.clicked = False # button is not clicked by default

    def draw(self, screen: pygame.Surface) -> bool:
        """Draws button image on screen and returns whether it is clicked or not

        :param screen: The screen
        :return action: If the button is clicked or not
        """
        action = False # button is not clicked by default

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos): # if image collides with mouse
            # if mouse is pressed and has not been pressed before
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True # button is clicked
                self.clicked = True # button is clicked

        if pygame.mouse.get_pressed()[0] == 0: # if not pressed
            self.clicked = False # button is not pressed

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
