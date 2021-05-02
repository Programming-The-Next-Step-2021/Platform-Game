
import pygame
from config import *

class TerrainObject(pygame.sprite.Sprite):
    """Base class for terrain objects
    """
    # def __init__(self, img, x, y):
    #     pygame.sprite.Sprite.__init__(self)
    #     self.image = img
    #     self.rect = self.image.get_rect()
    #     self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) # devide by 2 because it's in the middle
    # Todo: possibly delete init functions

    def update(self, screen_scroll):
        self.rect.x += screen_scroll # move decoration relative to players movement


# Create decoration class for things like grass etc
class Decoration(TerrainObject):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) # devide by 2 because it's in the middle

# Create water
class Water(TerrainObject):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) # devide by 2 because it's in the middle


# create Exit
class Exit(TerrainObject):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) # devide by 2 because it's in the middle

