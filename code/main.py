import pygame
import csv
from world import World
from config import *

from pygame.locals import *

pygame.init()

level = 1

# Initiate screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# set the framerate to control speed things
clock = pygame.time.Clock()





# load images
maple_img = pygame.image.load('img/background/maplestory1.png').convert_alpha() # If you add a second image, the order matters, img are put over each other
maple_img = pygame.transform.scale(maple_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # change image to size of window

# store tiles in list
def read_images():
    img_list = [] # tile images
    for x in range(TILE_TYPES):
        img = pygame.image.load(f'img/tile/{x}.png') # loop through images in tile folder
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) # square
        img_list.append(img)  # put images in a list
    return img_list

img_list = read_images()

# TODO: Change background to different images you draw (a tree, the sky, etc)
def draw_bg(): # draw the background
    screen.fill(BG)
    screen.blit(maple_img, (0,0))

# IMPORT FIGHTER CLASS

# IMPORT





def read_world_data(level: int):
    # Create an empty tile list
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS # creates list of 150 columns with -1
        world_data.append(r)

    # load in level data and create world
    with open (f'level_data/level{level}_data.csv', newline = '') as csvfile: # open csv file with numbers for tile sort
        reader = csv.reader(csvfile, delimiter = ',') # delimiter is how you seperate values (with a comma)
        for x, row in enumerate(reader): # iterate through rows
            for y, tile in enumerate(row): # iterate through values in rows
                world_data[x][y] = int(tile) # set a certain tile of a certain row to the value in the csv

    return world_data

world = World() # World clas returns player and health bar
world_data = read_world_data(level)
player, enemy_group, decoration_group, water_group, item_box_group, exit_group = world.process_data(world_data, img_list) # add healthbar here later #TODO: add healthbar and don't return enemy, but store in enemy_group (tutorial 6 )



# ToDO: Fix update in the loop for itemboxes, healthbar, etc

# Create loop to keep the game running, with keyboard presses
def main_loop():
    run = True
    screen_scroll = 0
    bg_scroll = 0


    # player action variables
    moving_left = False  # to start with you are not moving
    moving_right = False
    while run:
        clock.tick(FPS) # runs the game at 60 frames per second
        # update background
        draw_bg() # draw the background
        # draw the world map
        world.draw(screen, screen_scroll)
        # draws player, which is a fighter class with a certain position and size
        player.draw(screen, screen_scroll)

        for enemy in enemy_group:
            enemy.ai(world.obstacle_list)
            enemy.update()
            enemy.draw(screen, screen_scroll)

        # draw groups
        exit_group.update(screen_scroll)
        decoration_group.update(screen_scroll)
        water_group.update(screen_scroll)
        exit_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)

        screen_scroll = player.move(moving_left, moving_right, world.obstacle_list)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If you click the x
                run = False # the window will close

            # get keypresses from user we will use wasd to move
            if event.type == pygame.KEYDOWN: # if key is pressed
                if event.key == pygame.K_a: # if the key is a
                    moving_left = True # move left
                if event.key == pygame.K_d: # if key is d
                    moving_right = True # move right
                if event.key == pygame.K_SPACE: # if spacebar is pressed
                    player.jump = True # player jumps

            # when keyboard button is released
            if event.type == pygame.KEYUP: # if key is released
                if event.key == pygame.K_a: # if the key is a
                    moving_left = False # don't move left
                if event.key == pygame.K_d: # if key is d
                    moving_right = False # don't move right
                if event.key == pygame.K_ESCAPE:
                    run = False # also end game when escape is pressed
                # if event.key == pygame.K_SPACE: # if spacebar is pressed
                #     player.jump = True # player jumps


        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main_loop()