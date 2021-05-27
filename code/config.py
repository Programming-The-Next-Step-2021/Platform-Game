# Create game window size
SCREEN_WIDTH = 800 # use capslock for constants (you don't want to change values)
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
GAME_TITLE = 'Maplestory Platformer'

FPS = 60 # frame rate


# game variables
GRAVITY = 0.75 # effects how quickly you fall down after jump
SCROLL_TRESH = 200 # if you get within 200 pixels of the edge, the screen will move
ROWS = 16 # rows of the level
COLS = 150 # colums of the level
TILE_SIZE = SCREEN_HEIGHT // ROWS  # size of the tiles to create levels with should be screen height/ number of rows
TILE_TYPES = 39 # there are 21 different tile types
PLAYER_SCALE = 0.47  # control image size of player
ENEMY_SCALE = 0.8 # control image size of enemy
PLAYER_SPEED = 5 # control speed of player
ENEMY_SPEED = 3 # control the speed of the enmey
PLAYER_HEALTH = 100
ENEMY_HEALTH = 50
PLAYER_ANIMATION_COOLDOWN = 100 # control speed of animation
ENEMY_ANIMATION_COOLDOWN = 100 # control speed of animation
ATTACK_RANGE = 50 # size of rectangle used for getting the attack range of the sword
HIT_ANIMATION_DURATION = 300
MAX_LEVELS = 2 # number of available levels TODO: change this to more levels if there are more

start_game = False

# colors
BG = (99, 68, 191)
RED = (255, 0, 0)