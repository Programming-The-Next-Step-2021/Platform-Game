
import pygame
from code.config import *
from code.fighter import Fighter

class TerrainObject(pygame.sprite.Sprite):
    """Base class for terrain objects
    """
    # def __init__(self, img, x, y):
    #     pygame.sprite.Sprite.__init__(self)
    #     self.image = img
    #     self.rect = self.image.get_rect()
    #     self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) # devide by 2 because it's in the middle
    # Todo: possibly delete init functions

    def update(self, screen_scroll: int) -> None:
        self.rect.x += screen_scroll # move decoration relative to players movement


# Create item class for items to pick up
class ItemBox(pygame.sprite.Sprite):
    """ Class that creates items to pick up, deletes them when picked up, and allows items to move with the player
     when he moves.
     """

    def __init__(self, image: pygame.Surface, item_type: str, x: int, y: int) -> None:
        """ Creates an item dependent on the type

        :param image: Image of the item
        :param item_type: Type of the item (e.g., health, money, enemy loot)
        :param x: index of the tile column from the data file with tile information
        :param y: index of the tile row from the data file with tile information
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.item_type = item_type
        self.rect = self.image.get_rect()
        # on the x coordinate its the center, on the y its the top of the rectangle
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, player: Fighter, screen_scroll: int) -> None:
        """ Allows the screen to move with the player as he walks and 'deletes' health boxes when they
        are picked up

        :param player: This is a player which is an instance of the Figther Class
        :param screen_scroll: A variable with a default of 0 to enable scrolling of the screen when the player is moving
        """
        self.rect.x += screen_scroll  # move decoration relative to players movement
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
    """ A class that creates decoration like plants, rocks, trees, etc.

    """
    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) # devide by 2 because it's
        # in the middle

# Create water
class Water(TerrainObject):
    """ A class that creates water.

    """
    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


# create Exit
class Exit(TerrainObject):
    """ A class that creates the exit (to enter the next level).
    """
    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) #

