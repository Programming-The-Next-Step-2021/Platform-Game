from fighter import Fighter
from terrain_objects import Water, Decoration, Exit, ItemBox
from config import *
import pygame

class World():
    """A class that that creates the world, with all object in it (e.g., players, enemies, environment, trees, etc)"""
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data, img_list, item_boxes):
        """ Processes the data of the world into usable images to draw on the screen.

        :param data: A csv file with integers that correspond to images to create the world with
        :param img_list: The images that correspond to the number in the data file
        :param item_boxes: A dictionary with the type of box and image of the box in it
        :return: A tuple containing: player, enemy_group, decoration_group, water_group, item_box_group, exit_group
        """

        # Create groups of sprite
        enemy_group = pygame.sprite.Group()
        decoration_group = pygame.sprite.Group()
        water_group = pygame.sprite.Group()
        item_box_group = pygame.sprite.Group()
        exit_group = pygame.sprite.Group()

        # iterate through every value in the level data file
        for y, row in enumerate(data): # go through rows of the file
            for x, tile in enumerate(row): # go through tiles of the row
                if tile >= 0: # ignore -1s
                    img = img_list[tile] # tile at position x will become the tile from the image list made earlier
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE # x coordinate of where you put the rectangle of te the image == the
                    # x (tile position) * the size of the image
                    img_rect.y = y * TILE_SIZE # same but for y coordinate
                    tile_data = (img, img_rect) # tuple with info about tile: the image and the position
                    if tile >= 0 and tile <= 8: # 0 to 8 are the tiles that are dirt blocks thus obstacles
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10: # this is water
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14: # decorations, pile of rocks, wooden box, grass, etc
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15: # create player
                        # select 'player' image, positioned at tile position * size, thus dependend on the lvl size * 0.2 and speed of 5
                        player = Fighter('player', x * TILE_SIZE, y * TILE_SIZE, PLAYER_SCALE, PLAYER_SPEED, facing_left = True)
                    elif tile == 16: # create enemies
                        # select 'enemy' image, at tile position * size, image size 1 and speed of 5
                        enemy = Fighter('enemy', x * TILE_SIZE, y * TILE_SIZE, ENEMY_SCALE, ENEMY_SPEED, facing_left = True)
                        enemy_group.add(enemy)

                    # TODO: FIX THIS LATER: Add boxes and
                    # elif tile == 17: # Itembox ammo boxes and other droppings (DOESNT WORK, YOU ARE MISSING CODE FOR THIS)
                    # elif tile == 18: # Itembox grenade
                    elif tile == 19: # Itembox Health should be health later
                        item_type = 'Health'
                        image = item_boxes[item_type]
                        # x = 5
                        # y = 12
                        item_box = ItemBox(image, item_type, x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20: # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, enemy_group, decoration_group, water_group, item_box_group, exit_group # later add healthbar

    # draw the tiles, thus map & fix the movement of the map
    def draw(self, screen, screen_scroll):
        """ Draws images on the actual screen

        :param screen: The screen that you initialize
        :param screen_scroll: A variable with a default of 0 to enable scrolling of the screen (all tiles)
         when the player is moving
        """
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll # move x coordinate of all tiles to the opposite change of direction of the player
            screen.blit(tile[0], tile[1]) # tile was tuple with image in first index and coordinates in second index


