import pygame
from pygame.locals import *
pygame.init()

# Create game window size
screen_width = 1000
screen_height = int(screen_width * 0.8)

# Initiate screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Maplestory Platformer')

# set the framerate to control speed things
clock = pygame.time.Clock()
FPS = 60 # frame rate

# player action variables
moving_left = False # to start with you are not moving
moving_right = False


# colors
# back_img = pygame.image.load('img/background1.png') # If you add a second image, the order matters, img are put over each other
BG = (99,68,191)

def draw_bg(): # draw the background
    screen.fill(BG)


# Start with player character
class Fighter(pygame.sprite.Sprite): # Create class for fighters
    """Fighter class"""

    def __init__(self, x, y, scale, speed):
        """Initialises the player

        :param x: x coordinates of the soldier
        :param y: y coordinates of the soldier
        :param scale: scale of the image/character
        :param speed: determines speed of the character
        """
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1 # looking to the right
        img = pygame.image.load('img/char1.png')  # load character image
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))  # change character size
        self.rect = img.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):

        # reset movement of the variables
        dx = 0 # change in x
        dy = 0 # change in y

        # assign movement o the variables if they are moving right or left
        if moving_left: # if moving left is true
            dx = -self.speed # your x coordinate decreases by your speed
        if moving_right: # if moving right is true
            dx = self.speed # your y coordinate increases by your speed

        # update the position of rectangle
        self.rect.x += dx # update position by dx
        self.rect.y += dy # update position by dy



    def draw(self): # last thing you want to happen
        screen.blit(self.image, self.rect)  # Put image of player on screen with coordinates 300 300


player = Fighter(300,300, 0.2, 5) # positioned at 300 width, 300 height, size * 0.2 and speed of 5


# Create loop to keep the game running, with keyboard presses
run = True
while run:


    clock.tick(FPS) # runs the game at 60 frames per second
    draw_bg() # draw the background
    player.draw()  # draws player, which is a fighter class with a certain position and size

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

        # when keyboard button is released
        if event.type == pygame.KEYUP: # if key is released
            if event.key == pygame.K_a: # if the key is a
                moving_left = False # don't move left
            if event.key == pygame.K_d: # if key is d
                moving_right = False # don't move right
            if event.key == pygame.K_ESCAPE:
                run = False # also end game when escape is pressed


    pygame.display.update()

pygame.quit()