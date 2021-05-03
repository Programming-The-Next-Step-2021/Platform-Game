
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


# Create item class for items to pick up
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, image, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.item_type = item_type
        self.rect = self.image.get_rect()
        # on the x coordinate its the center, on the y its the top of the rectangle
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, player):
        # see if player has picked up item
        if pygame.sprite.collide_rect(self, player): # if collision of player with box
            # check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                if player.health > PLAYER_HEALTH: # if health of player is bigger than the maximum allowed
                    player.health = PLAYER_HEALTH # put it back to max

            # TODO: add money later in the game
            # elif self.item_type == 'Money':
            #     player.money += 5
            # delete the item box once picked up
            self.kill()



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

