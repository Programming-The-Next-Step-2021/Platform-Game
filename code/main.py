import pygame
import csv
from code.world import World
from code.config import *
from code.player_attributes import HealthBar

from pygame.locals import *

pygame.init()

level = 1

# Initiate screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# set the framerate to control speed things
clock = pygame.time.Clock()

# load images
import os

print(os.listdir())
maple_img = pygame.image.load(
    'img/background/maplestory1.png').convert_alpha()  # If you add a second image, the order matters, img are put over each other
maple_img = pygame.transform.scale(maple_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # change image to size of window

# pick up boxes
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
item_boxes = {
    'Health': health_box_img
}


# store tiles in list
def read_images() -> list[pygame.Surface]:
    """ Puts all tile images in a list

    :return: A list with all tile images
    """
    img_list = []  # tile images
    for x in range(TILE_TYPES):
        img = pygame.image.load(f'img/tile/{x}.png')  # loop through images in tile folder
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))  # square
        img_list.append(img)  # put images in a list
    return img_list


img_list = read_images()

# define font
font = pygame.font.SysFont('Futura', 30)


# to draw text on screen like health bar
def draw_text(text, font: pygame.font.Font, text_col, x, y) -> None:
    """ Allow you to draw text on the screen

    :param text: Text that you want to type
    :param font: The desired font of the text
    :param text_col: The desired color of the text
    :param x: The x desired coordinate on the screen
    :param y: The y desired coordinate on the screen
    """
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# TODO: Change background to different images you draw (a tree, the sky, etc)
def draw_bg() -> None:  # draw the background
    """ Draws the background

    """
    screen.fill(BG)
    screen.blit(maple_img, (0, 0))


def read_world_data(level: int) -> list[list[int]]:
    """ Reads the data of the world for the chosen level

    :param level: The desired level to display
    :return: The data needed to load the level
    """
    # Create an empty tile list
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS  # creates list of 150 columns with -1
        world_data.append(r)

    # load in level data and create world
    with open(f'level_data/level{level}_data.csv', newline='') as csvfile:  # open csv file with numbers for tile sort
        reader = csv.reader(csvfile, delimiter=',')  # delimiter is how you seperate values (with a comma)
        for x, row in enumerate(reader):  # iterate through rows
            for y, tile in enumerate(row):  # iterate through values in rows
                world_data[x][y] = int(tile)  # set a certain tile of a certain row to the value in the csv

    return world_data


world = World()  # World clas returns player and health bar
world_data = read_world_data(level)
player, enemy_group, decoration_group, water_group, item_box_group, exit_group = world.process_data(world_data,
                                                                                                    img_list,
                                                                                                    item_boxes)
health_bar = HealthBar(10, 10, player.health, PLAYER_HEALTH)


# ToDO: Fix update in the loop for itemboxes, healthbar, etc

# Create loop to keep the game running, with keyboard presses
def main_loop() -> None:
    """ The main loop that runs the whole game allowing you to actually play it

    """
    run = True
    screen_scroll = 0
    bg_scroll = 0

    # player action variables
    moving_left = False  # to start with you are not moving
    moving_right = False

    while run:
        clock.tick(FPS)  # runs the game at 60 frames per second
        # update background
        draw_bg()  # draw the background
        # show health of player
        health_bar.draw(screen, player.health)
        # draw the world map
        world.draw(screen, screen_scroll)
        # update image to draw of the player
        # player.update_animation()
        player.update(player)

        for enemy in enemy_group:
            if enemy.alive:
                enemy.ai(world.obstacle_list)
            enemy.update(player)
            # enemy.update_animation()
            enemy.draw(screen, screen_scroll)

        # draws player, which is a fighter class with a certain position and size
        player.draw(screen, screen_scroll)

        # draw groups
        exit_group.update(screen_scroll)
        decoration_group.update(screen_scroll)
        water_group.update(screen_scroll)
        item_box_group.update(player, screen_scroll)
        exit_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        item_box_group.draw(screen)

        # update action of the player
        if player.alive:  # if the player is alive
            if player.attack: # if you are attacking
                player.update_action(3) # update the action to attacking (3)
            elif player.hit: # if you are being hit
                player.update_action(2) # update action to being hit (2)
                player.animate_hit() # show the animation for being hit
            else:
                if moving_left or moving_right:  # if he's moving
                    player.update_action(1)  # 1: running
                else:
                    player.update_action(0)  # 0: chilling, normal
            screen_scroll = player.move(moving_left, moving_right, world.obstacle_list)




        # screen_scroll = player.move(moving_left, moving_right, world.obstacle_list)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If you click the x
                run = False  # the window will close

            keys = pygame.key.get_pressed()
            # if keys[pygame.K_LEFT] and keys[pygame.K_a]:
            #     player.attack = True
            # if keys[pygame.K_RIGHT] and keys[pygame.K_a]:
            #     player.attack = True

            # # get keypresses from user we will use wasd to move
            # if event.type == pygame.KEYDOWN:  # if key is pressed
            #     if event.key == pygame.K_LEFT and player.alive:  # if the key is left arrow
            #         moving_left = True  # move left
            #     if event.key == pygame.K_RIGHT and player.alive:  # if key is right arrow
            #         moving_right = True  # move right
            #     if event.key == pygame.K_a and player.alive:  # press a to slice
            #         player.attack = True
            #     if event.key == pygame.K_SPACE and player.alive:  # if spacebar is pressed
            #         player.jump = True  # player jumps
            #
            # # when keyboard button is released
            # if event.type == pygame.KEYUP:  # if key is released
            #     if event.key == pygame.K_LEFT:  # if the key is a
            #         moving_left = False  # don't move left
            #     if event.key == pygame.K_RIGHT:  # if key is d
            #         moving_right = False  # don't move right
            #     # if event.key == pygame.K_a:
            #     #     player.attack = False
            #     if event.key == pygame.K_ESCAPE:
            #         run = False  # also end game when escape is pressed
            #     # if event.key == pygame.K_SPACE: # if spacebar is pressed
            #     #     player.jump = True # player jumps

            # get keypresses from user we will use wasd to move
            # if event.type == pygame.KEYDOWN:  # if key is pressed
            if keys[pygame.K_LEFT] and player.alive:  # if the key is left arrow
                moving_left = True  # move left
            else:
                moving_left = False
            if keys[pygame.K_RIGHT] and player.alive:  # if key is right arrow
                moving_right = True  # move right
            else:
                moving_right = False
            if keys[pygame.K_a] and player.alive: # press a to slice
                player.attack = True
            else:
                # player.attack = False
                ...
            if keys[pygame.K_SPACE] and player.alive:  # if spacebar is pressed
                player.jump = True  # player jumps
            else:
                player.jump = False
            if keys[pygame.K_ESCAPE]:
                run = False  # also end game when escape is pressed

            # # when keyboard button is released
            # if event.type == pygame.KEYUP:  # if key is released
            #     if event.key == pygame.K_LEFT:  # if the key is a
            #         moving_left = False  # don't move left
            #     if event.key == pygame.K_RIGHT:  # if key is d
            #         moving_right = False  # don't move right
            #     # if event.key == pygame.K_a:
            #     #     player.attack = False
            #     if event.key == pygame.K_ESCAPE:
            #         run = False  # also end game when escape is pressed
            #     # if event.key == pygame.K_SPACE: # if spacebar is pressed
            #     #     player.jump = True # player jumps

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main_loop()
