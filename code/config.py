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
TILE_TYPES = 21 # there are 21 different tile types

# colors
BG = (99, 68, 191)
RED = (255, 0, 0)