import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, screen, health):
        # update healthbar with new health
        self.health = health

        # calculate the health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


