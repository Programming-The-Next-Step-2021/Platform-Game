import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)

class HealthBar():
    """ Creates and draw a healthbar on the screen

    """
    def __init__(self, x:int, y:int, health: int, max_health: int) -> None:
        """ Initializes health bar

        :param x: x coordinate of the screen depending on where you want the health bar to be
        :param y: y coordinate of the screen depending on where you want the health bar to be
        :param health: Health of the player (int)
        :param max_health: Max health of the player (int)
        """
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, screen: pygame.Surface, health: int) -> None:
        """ Draws the health bar on the screen

        :param screen: The screen that you initialize
        :param health: The amount of health you want to draw
        """
        # update healthbar with new health
        self.health = health

        # calculate the health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


