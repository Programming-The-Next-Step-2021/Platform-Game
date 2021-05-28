import pygame # to create game functionalities
import csv # to load csv's
from pygame import mixer # to load music and sound effects
from code.world import World
from code.config import *
from code.player_attributes import HealthBar
from code.button import Button

from pygame.locals import *
mixer.init()
pygame.init()

level = 1

# Initiate screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# set the framerate to control speed things
clock = pygame.time.Clock()


# load images
# starting screen background image
start_screen_img = pygame.image.load('img/game_start/background.png').convert_alpha()
start_screen_img = pygame.transform.scale(start_screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# background images in game
maple_img = pygame.image.load(
    'img/background/maplestory1.png').convert_alpha()  # If you add a second image, the order matters, img are put over each other
maple_img = pygame.transform.scale(maple_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # change image to size of window

# pick up boxes images
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
item_boxes = {
    'Health': health_box_img
}
# images for starting screen & exit button
start_img = pygame.image.load('img/game_start/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/game_start/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/game_start/restart_btn.png').convert_alpha()



# play music to instantly
pygame.mixer.music.load('audio/intro.mp3')
pygame.mixer.music.set_volume(0.4) # adapt loudness (percentage of original volume)
pygame.mixer.music.play(-1, 0.0, 5000) # how many times you want to loop over the music, how much delay you want, how much fade you want in miliseconds



# save sound effects & music for later
slash_sound = pygame.mixer.Sound('audio/slash.mp3') # use later in keys section
slash_sound.set_volume(0.1)
lvl2_music = pygame.mixer.Sound('audio/lvl2.mp3') # use later next lvl section
lvl2_music.set_volume(0.6)
finish_music = pygame.mixer.Sound('audio/finish.mp3') # use later
finish_music.set_volume(0.4)



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
# add buttons to game
start_button = Button(SCREEN_WIDTH // 2.2 - 130, SCREEN_HEIGHT // 2 - 50, start_img, 0.7) # x location, y location, and scale
exit_button = Button(SCREEN_WIDTH // 2.2 - 130, SCREEN_HEIGHT // 2 + 50, exit_img, 0.7)
restart_button = Button(SCREEN_WIDTH // 2 - 205, SCREEN_HEIGHT // 2 - 100, restart_img, 1)


# ToDO: Fix update in the loop for itemboxes, healthbar, etc

# Create loop to keep the game running, with keyboard presses
def main_loop() -> None:
    """ The main loop that runs the whole game allowing you to actually play it

    """
    # declare these variables as global so that they can be used later again to recreate the world
    # if the players dies
    global player, enemy_group, decoration_group, water_group, item_box_group, exit_group, world, \
        world_data, health_bar, level

    start_game = False
    run = True
    screen_scroll = 0
    bg_scroll = 0

    # player action variables
    moving_left = False  # to start with you are not moving
    moving_right = False

    # music false by default
    lvl2_music_started = False
    end_music_started = False


    while run:
        clock.tick(FPS)  # runs the game at 60 frames per second

        if start_game == False:
            # create main menu
            screen.fill(BG) # get background color
            screen.blit(start_screen_img, (0, 0))
            # add buttons to screen
            if start_button.draw(screen): # if start is clicked
                start_game = True
            if exit_button.draw(screen): # if exit is clicked
                run = False # stop the game (this main loop)


        else: # if not, run the game:
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

                # # check whether you hit the water, and if so, you die!
                if pygame.sprite.spritecollide(player, water_group, False):
                    player.health = 0

                # check whether you hit the exit sign, thus proceed to next lvl
                lvl_complete = False  # level is not completed by default
                if pygame.sprite.spritecollide(player, exit_group, False):  # until player run into exit sign
                    lvl_complete = True # after hit, lvl is completed
                    if lvl_complete: # if level is complete
                        level += 1 # load the next lvl
                        pygame.mixer.music.stop() # stop intro & lvl 1 music
                        if not lvl2_music_started: # if the song has not started yet
                            lvl2_music.play(-1, 0, 5000) # start new soundtrack
                            lvl2_music_started = True
                        if level <= MAX_LEVELS: # if the level equals or is smaller than the max lvl
                            # load lvl data and create world
                            world = World()  # World class returns player and health bar
                            world_data = read_world_data(level)
                            player, enemy_group, decoration_group, water_group, item_box_group, exit_group = world.process_data(
                                world_data,
                                img_list,
                                item_boxes)
                            health_bar = HealthBar(10, 10, player.health, PLAYER_HEALTH)

                        # if there are no more levels stop the game
                        elif level > MAX_LEVELS:
                            # if finish_music has not started yet, play it
                            if not end_music_started:
                                lvl2_music.fadeout(1000)  # stop and fadeout soundtrack loop
                                # lvl2_music.stop()
                                finish_music.play(-1, 0, 10000)
                                end_music_started = True

                            screen_scroll = 0
                            if restart_button.draw(screen):  # if restart button is clicked
                                level = 1 # reset lvl
                                finish_music.fadeout(5000)
                                # Start music again
                                pygame.mixer.music.load('audio/intro.mp3')
                                pygame.mixer.music.set_volume(0.4)  # adapt loudness (percentage of original volume)
                                pygame.mixer.music.play(-1, 0.0,
                                                        5000)  # how many times you want to loop over the music, how much delay you want, how much fade you want in miliseconds

                                # Reset music
                                lvl2_music_started = False
                                end_music_started = False
                                bg_scroll = 0

                                # load lvl data and create world
                                world = World()  # World class returns player and health bar
                                world_data = read_world_data(level)
                                player, enemy_group, decoration_group, water_group, item_box_group, exit_group = world.process_data(
                                    world_data,
                                    img_list,
                                    item_boxes)
                                health_bar = HealthBar(10, 10, player.health, PLAYER_HEALTH)



            # if player is dead and the restart button is clicked recreate the whole world again
            else:
                screen_scroll = 0
                if restart_button.draw(screen): # if restart button is clicked
                    bg_scroll = 0
                    # load lvl data and create world
                    world = World()  # World class returns player and health bar
                    world_data = read_world_data(level)
                    player, enemy_group, decoration_group, water_group, item_box_group, exit_group = world.process_data(
                        world_data,
                        img_list,
                        item_boxes)
                    health_bar = HealthBar(10, 10, player.health, PLAYER_HEALTH)


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
                slash_sound.play() # add slashing sound
            else:
                # player.attack = False
                ...
            if keys[pygame.K_SPACE] and player.alive:  # if spacebar is pressed
                player.jump = True  # player jumps
                # jump_sound.play() # add jumping sound
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
