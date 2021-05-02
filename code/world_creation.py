import pygame
import csv
from pygame.locals import *
pygame.init()

# Create game window size
SCREEN_WIDTH = 800 # use capslock for constants (you don't want to change values)
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Initiate screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maplestory Platformer')

# set the framerate to control speed things
clock = pygame.time.Clock()
FPS = 60 # frame rate

# game variables
GRAVITY = 0.75 # effects how quickly you fall down after jump
ROWS = 16 # rows of the level
COLS = 150 # colums of the level
TILE_SIZE = SCREEN_HEIGHT // ROWS  # size of the tiles to create levels with should be screen height/ number of rows
TILE_TYPES = 21 # there are 21 different tile types
level = 1


# player action variables
moving_left = False # to start with you are not moving
moving_right = False


# load images
# store tiles in list
img_list = [] # tile images
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png') # loop through images in tile folder
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) # square
    img_list.append(img)  # put images in a list



# back_img = pygame.image.load('img/background1.png') # If you add a second image, the order matters, img are put over each other


# colors
BG = (99, 68, 191)
RED = (255, 0, 0)

def draw_bg(): # draw the background
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300)) # draw line in game (display window, color and start and end x & y coordinates)


# Start with player character
class Fighter(pygame.sprite.Sprite): # Create class for fighters
    """Fighter class"""

    def __init__(self, char_type, x, y, scale, speed):
        """Initialises the player

        :param x: x coordinates of the soldier
        :param y: y coordinates of the soldier
        :param scale: scale of the image/character
        :param speed: determines speed of the character
        """
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type # what kind of fighter we want to initialize (enemy, player, etc)
        self.speed = speed

        # Later on you should change to sprite sheets
        self.direction = 1 # 1 = looking right, -1 is looking left
        self.speed_y = 0 # no vertical speed
        self.jump = False # you don't jump by default
        self.in_air = True
        self.flip = False # default image is not flipped (thus looking to the right)
        img = pygame.image.load(f'img/{self.char_type}/normal/0.png')  # load character image, dependent on self.char_type an image from a certain directory will be directed
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))  # change character size
        self.rect = self.image.get_rect() # get the rectangle from the scaled image, otherwise the bounding recangle is not scaled with the image
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def move(self, moving_left, moving_right):

        # reset movement of the variables
        dx = 0 # change in x
        dy = 0 # change in y

        # assign movement o the variables if they are moving right or left
        if moving_left: # if moving left is true
            dx = -self.speed # your x coordinate decreases by your speed
            self.flip = True # flip layer
            self.direction = -1 # looking left
        if moving_right: # if moving right is true
            dx = self.speed # your y coordinate increases by your speed
            self.flip = False  # don't flip
            self.direction = 1  # looking right

        # jump
        if self.jump and self.in_air == False: # if jump is true and you are not in the air (prevens double jump)
            self.speed_y = -11 #changes how how the player jumps
            self.jump = False # jump ends
            self.in_air = True # you are in the air

        # add gravity for the jump so you come back down after jump
        self.speed_y += GRAVITY  # jump starts with high number and slowly decreases by gravity making you fall down
        if self.speed_y > 10: # if speed > 10
            self.speed_y # set it to 10 (never go past limit)
        dy += self.speed_y  # change in y coordinate

        # Check whether you hit/touch something (collision)
        for tile in world.obstacle_list:
        # check the collision of the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): # colliderect check for collision with other rectangle
                dx = 0 # if your next move would be to hit something, don't do that so put movement to 0
            # check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): # colliderect check for collision with other rectangle
                # check if the character is below the obstacle, aka, jumping, aka hitting something above
                if self.speed_y < 0: # if the speed is negative you are going up
                    self.speed_y = 0 # set speed to 0, thus stop once you hit obstacle
                    dy = tile[1].bottom - self.rect.top # change of position will be bottom of the tile - head (top) of character
                # check if above ground, whether he's falling
                elif self.speed_y >= 0: # if you're falling and going to hit an object
                    self.speed_y = 0 # the speed becomes 0
                    self.in_air = False # you are not in air anymore
                    dy = tile[1].top - self.rect.bottom # if the change of position will be top of the tile - feet (bottom) character
                    self.jump = False # prevents you from loading a jump while your in air which will be activated when you reach te ground


        # update the position of rectangle
        self.rect.x += dx # update position by dx
        self.rect.y += dy # update position by dy



    def draw(self): # last thing you want to happen
        # screen.blit : Put image of player on screen with coordinates of self.rect
        # first argument (self.image) : what image
        # Second argument (self.flip) : if True, image will be flipped on the x axis
        # Third argument (False) : whether image should be flipped horizontally
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, RED, self.rect, 1) # draw red rectangle around the character



class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
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
                        player = Fighter('player', x * TILE_SIZE, y * TILE_SIZE, 0.1, 5)
                    elif tile == 16: # create enemies
                        # select 'enemy' image, at tile position * size, image size 1 and speed of 5
                        enemy = Fighter('enemy', x * TILE_SIZE, y * TILE_SIZE, 1, 5)
                        enemy_group.add(enemy)

                    # TODO: FIX THIS LATER: Add boxes and
                    # elif tile == 17: # Itembox ammo boxes and other droppings (DOESNT WORK, YOU ARE MISSING CODE FOR THIS)
                    # elif tile == 18: # Itembox grenade
                    # elif tile == 19: # Itembox Health should be health later
                    elif tile == 20: # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player # later add healthbar

    # draw the tiles, thus map
    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1]) # tile was tuple with image in first index and coordinates in second index



# Create decoration class for things like grass etc
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) # devide by 2 because it's in the middle

# Create water
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) # devide by 2 because it's in the middle

# create Exit
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) # devide by 2 because it's in the middle


# Create groups of sprite
enemy_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


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

world = World() # World clas returns player and health bar
player = world.process_data(world_data) # add healthbar here later #TODO: add healthbar and don't return enemy, but store in enemy_group (tutorial 6 )



# ToDO: Fix update in the loop for itemboxes, healthbar, etc

# Create loop to keep the game running, with keyboard presses
run = True
while run:

    clock.tick(FPS) # runs the game at 60 frames per second
    # update background
    draw_bg() # draw the background
    # draw the world map
    world.draw()
    # draws player, which is a fighter class with a certain position and size
    player.draw()

    for enemy in enemy_group:
        enemy.draw()

    player.move(moving_left, moving_right)

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