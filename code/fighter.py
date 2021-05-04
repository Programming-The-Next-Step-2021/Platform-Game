from config import *
import pygame
import random


# Start with player character
class Fighter(pygame.sprite.Sprite):
    """A class that creates a player or an enemy, allows it to move, collide with objects and allows the screen
     to move with the player
     """

    def __init__(self, char_type, x, y, scale, speed):
        """Initialises the player

        :param char_type: determines the type of fighter (player or enemy)
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
        if char_type == 'player': # if player
            self.health = PLAYER_HEALTH # give player health
        elif char_type == 'enemy': # if enemey
            self.health = ENEMY_HEALTH # give enemy health
        self.in_air = True
        self.flip = False # default image is not flipped (thus looking to the right)
        img = pygame.image.load(f'img/{self.char_type}/normal/0.png')  # load character image, dependent on self.char_type an image from a certain directory will be directed
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))  # change character size
        self.rect = self.image.get_rect() # get the rectangle from the scaled image, otherwise the bounding recangle is not scaled with the image
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # ai specific variables
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0


    def move(self, moving_left, moving_right, obstacle_list):
        """Initializes movement of the player, collision with objects and scrolling of the screen

        :param moving_left: True if the player is moving left
        :param moving_right: True if the player is moving right
        :param obstacle_list: List of all obstacles
        :return: Returns screen_scroll if player
        """

        # reset movement of the variables
        screen_scroll = 0 # no scrolling by default
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
        for tile in obstacle_list:
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

        # update scroll based on the position of the player
        if self.char_type == 'player': # only if character is player
            # if you are about to hit border of the screen: right of rect is > screen width - 200 pixels or left side is smaller than the treshold (cause x coordinate star with 0)
            if self.rect.right > SCREEN_WIDTH - SCROLL_TRESH or self.rect.left < SCROLL_TRESH:
                self.rect.x -= dx # the change becomes 0, thus you stay in the same place
                screen_scroll = -dx  # move the screen to the opposite side of where the player is going

            return screen_scroll # we need to use this later thus need to return it

    def update(self): # TODO: ADD UPDATE FUNCTION
       pass

    def ai(self, obstacle_list):
        """Initialises movement for the enemies

         :param obstacle_list: A list with all obstacles
          """

            # if self.alive and player.alive:
            # start idling for 1/200 probability
            if self.idling == False and random.randint(1,200) == 1: # if random number between 1 and 200 == 1

                self.idling = True # idling is true
                self.idling_counter = 50

            if self.idling == False: # if they are not idling -> move
                if self.direction == 1: # if going to right direction
                    ai_moving_right = True # ai is moving right
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right, obstacle_list)
                self.move_counter += 1

                if self.move_counter > TILE_SIZE: # if enemies walk more than 1 tile
                    self.direction *= -1 # flip and walk the other way
                    self.move_counter *= -1

            else: # if they are idling -> don't move
                self.idling_counter -= 1 # start with 50
                if self.idling_counter <= 0: # once counter = 0
                    self.idling = False # start walking again





    def draw(self, screen, screen_scroll): # last thing you want to happen
        """ Draws images on the actual screen

        :param screen: The screen that you initialize
        :param screen_scroll: A variable with a default of 0 to enable scrolling of the screen when the
         player is moving
         """

        if self.char_type == 'enemy': # if enemy
            self.rect.x += screen_scroll  # move x coordinate of enemies relative to players movement
        # screen.blit : Put image of player on screen with coordinates of self.rect
        # first argument (self.image) : what image
        # Second argument (self.flip) : if True, image will be flipped on the x axis
        # Third argument (False) : whether image should be flipped horizontally
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, RED, self.rect, 1) # draw red rectangle around the character

