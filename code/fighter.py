from __future__ import annotations
from code.config import *
import pygame
import random
import os


# Start with player character
class Fighter(pygame.sprite.Sprite):
    """A class that creates a player or an enemy, allows it to move, collide with objects and allows the screen
     to move with the player
     """

    def __init__(self, char_type: str, x: int, y: int, scale: float, speed: float, facing_left: bool = False) -> None:
        """Initialises the player

        :param char_type: determines the type of fighter (player or enemy)
        :param x: x coordinates of the soldier
        :param y: y coordinates of the soldier
        :param scale: scale of the image/character
        :param speed: determines speed of the character
        :param facing_left: set to True if the image for the character is facing left
            (then it will be flipped the right way when walking)
        """

        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type # what kind of fighter we want to initialize (enemy, player, etc)
        self.speed = speed

        # Later on you should change to sprite sheets
        self.direction = 1 # 1 = looking right, -1 is looking left
        self.speed_y = 0 # no vertical speed
        self.jump = False # you don't jump by default
        if char_type == 'player': # if player
            self.health = PLAYER_HEALTH # give player health
            self.animation_cooldown = PLAYER_ANIMATION_COOLDOWN
        elif char_type == 'enemy': # if enemy
            self.health = ENEMY_HEALTH # give enemy health
            self.animation_cooldown = ENEMY_ANIMATION_COOLDOWN
        elif char_type == 'boss_enemy': # if boss enemy
            self.health = BOSS_ENEMY_HEALTH # give enemy health
            self.animation_cooldown = ENEMY_ANIMATION_COOLDOWN
        self.in_air = True
        self.flip = False # default image is not flipped (thus looking to the right)
        self.animation_list = [] # create empty list to put images in 
        self.frame_index = 0 # index for loading of the images
        self.action = 0 # whether character is moving, or dying or jumping (different animations)
        self.update_time = pygame.time.get_ticks() # to track the time when the animation was last updated
        self.attack = False # you don't attack by default
        self.attack_range_rect = pygame.Rect(0, 0, ATTACK_RANGE, 20) # creat attack range with start coordinates (0,0)
        # and width and height
        self.hit = False


        # load all images for the players, so that animations work, depending on animation type
        animation_types = ['normal', 'run', 'hit', 'attack', 'death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count how many files are in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')  # dependent on self.char_type an
                # image from a certain directory will be directed
                if facing_left: # if the image is facing left, flip it so that it is facing right
                    img = pygame.transform.flip(img, True, False)
                # set transparent background
                if self.char_type == 'enemy':
                    BG = (255, 0, 255) # needed to create transparant background for players and enemeies
                    img = img.convert()
                    img.set_colorkey(BG)
                # if self.char_type == 'boss_enemy':
                #     # BG = (255, 0, 255) # needed to create transparant background for players and enemeies
                #     img = img.convert()
                #     # img.set_colorkey(BG)

                # change character size
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list) # store images in list

        self.image = self.animation_list[self.action][self.frame_index] # give action and use index of images in list
        # get the rectangle from the scaled image, otherwise the bounding rectangle is not scaled with the image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hit_counter = 0

        # ai specific variables
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.hit_animation_counter = pygame.time.get_ticks() # to track the time when the animation was last updated



    def move(self, moving_left: bool, moving_right: bool, obstacle_list: list[tuple[pygame.Surface, pygame.Rect]]) -> int:
        """Initializes movement of the player, collision with objects and scrolling of the screen

        :param moving_left: True if the player is moving left
        :param moving_right: True if the player is moving right
        :param obstacle_list: A tuple containing a list of all obstacles. Which is tile information for only things that
         are seen as obstacles (e.g., things the player can walk into like a wall, or the ground). This info includes
          an image of the obstacle and a position of the obstacle.
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
        # change the position of the sword range (forward or behind the center of the player, thus letting it go left
        # or right)
        self.attack_range_rect.center = (self.rect.centerx + self.attack_range_rect.width//2 * self.direction, self.rect.centery)

        # jump
        if self.jump and self.in_air == False: # if jump is true and you are not in the air (prevents double jump)
            self.speed_y = -15 # changes how high the player jumps
            # add jumping sound
            jump_sound = pygame.mixer.Sound('audio/jump.wav')
            jump_sound.set_volume(0.5)
            jump_sound.play()  # add jumping sound
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
                # if ai has hat a wall, make them turn around and not run into it continuously
                if self.char_type == 'enemy' or self.char_type == 'boss_enemy': # if enemy (hits something)
                    self.direction *= -1 # go to the other side
                    self.move_counter = 0 # reset the movement counter
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


        # check whether you've fallen of the map and die
        if self.rect.bottom > SCREEN_HEIGHT: # if your feet are bigger than the screen height (aka you've fallen of)
            self.health = 0 # your health is 0

        # fix that the player can't fall of the map
        if self.char_type == 'player':  # only if character is player
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH: # if you fall of left or right side of lvl
                dx = 0 # make the movement null: stop the movement
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



    def update(self, player: Fighter) -> None: # TODO: ADD UPDATE FUNCTION
        """ Function that adds damage to the player if he is hit by an enemy

        :param player: Player instance from the Fighter class
        """
        self.update_animation()
        self.check_alive()
        if self.char_type == 'enemy' or self.char_type == 'boss_enemy': # if enemy
            # create damage to player when hit by enemies
            if self.alive:  # if enemy died, he cannot do or take damage anymore
                if self.rect.colliderect(player.rect): # collides with player
                    self.hit_counter +=1 # ad 1 to hitcounter
                    if self.hit_counter % 20 == 0: # if 0 is left after dividing by 20 (every 20 iterations)
                        player.health -= 5 # take health from player
                        # player.update_action(2)
                        player.hit = True
                # create damage to enemies when hit by sword
                if self.rect.colliderect(player.attack_range_rect): # if enemy collides with sword range
                    if player.action == 3: # if player is attacking
                        self.health -= 2 # take 7 health from enemy
                        # self.update_action(2)
                        self.hit = True
                        self.update_action(2)  # update action to being hit (2)
                        self.animate_hit()  # show the animation for being hit



    def ai(self, obstacle_list: list[tuple[pygame.Surface, pygame.Rect]]) -> None:
        """Initialises movement for the enemiesA

         :param obstacle_list: A list with all obstacles
        """

        # if self.alive and player.alive:
        # start idling for 1/200 probability
        if self.idling == False and random.randint(1,200) == 1: # if random number between 1 and 200 == 1
            self.update_action(0)  # 0: idle
            self.idling = True # idling is true
            self.idling_counter = 50
        # chek if the enemy ai is near the player
        if self.idling == False: # if they are not idling -> move
            if self.direction == 1: # if going to right direction
                ai_moving_right = True # ai is moving right
            else:
                ai_moving_right = False
            ai_moving_left = not ai_moving_right
            self.move(ai_moving_left, ai_moving_right, obstacle_list)
            self.update_action(1)  # 1: run
            self.move_counter += 1

            if self.move_counter > TILE_SIZE: # if enemies walk more than 1 tile
                self.direction *= -1 # flip and walk the other way
                self.move_counter *= -1

        else: # if they are idling -> don't move
            self.idling_counter -= 1 # start with 50
            if self.idling_counter <= 0: # once counter = 0
                self.idling = False # start walking again



    def update_animation(self) -> None:
        """
        Loops through images (updates) so that an animation is created of the players movement.
        """
        # update the animation
        # updating of image depending on the current frame image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since last update of image
        if self.action == 3: # speed up the animation for attack because it has more images thus will be animated slower
            animation_cooldown = self.animation_cooldown / 4
        else:
            animation_cooldown = self.animation_cooldown
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            # move the index variable to go to next image
            self.update_time = pygame.time.get_ticks() # reset timer
            self.frame_index += 1 # go to next image
        # if there are no more images (animation has run out), reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]): # if current image index is bigger than lenght of all images of that action
            if self.attack:
                self.attack = False
            # when player/enemy dies, stop looping animation
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0 # the first image is loaded again

    def update_action(self, new_action: int) -> None:
        """
        Updates what action a player is having (moving, or dying or jumping)
        For which frame_index = 0 represents standing still, 1 = running/moving, 2 = jumping
        :param new_action: The next action that the player takes (e.g., jumping)
        :type new_action: int
        """

        # check if new action is different from the last one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.hit_animation_counter = pygame.time.get_ticks()

    def animate_hit(self):
        """
        Lets the animation for being hit last longer
        """
        # if the value of the counter is smaller than the HIT_ANIMATION_DURATION
        if pygame.time.get_ticks() - self.hit_animation_counter > HIT_ANIMATION_DURATION:
            self.hit = False # stop the animation of being hit
            # move the index variable to go to next image
            self.hit_animation_counter = pygame.time.get_ticks() # reset timer


    def check_alive(self):
        """
        Checks whether the player is alive, if not alive, death animation is set in action.
        """
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)

    def draw(self, screen: pygame.Surface, screen_scroll: int) -> None: # last thing you want to happen
        """ Draws images on the actual screen

        :param screen: The screen that you initialize
        :param screen_scroll: A variable with a default of 0 to enable scrolling of the screen when the
         player is moving
         """

        if self.char_type == 'enemy' or self.char_type == 'boss_enemy': # if enemy
            self.rect.x += screen_scroll  # move x coordinate of enemies relative to players movement
        # screen.blit : Put image of player on screen with coordinates of self.rect
        # first argument (self.image) : what image
        # Second argument (self.flip) : if True, image will be flipped on the x axis
        # Third argument (False) : whether image should be flipped horizontally
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # pygame.draw.rect(screen, RED, self.rect, 1) # draw red rectangle around the character to check the collision
        # pygame.draw.rect(screen, RED, self.attack_range_rect, 1)

