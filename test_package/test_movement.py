import unittest
import pygame
from code.fighter import Fighter

SCREEN_WIDTH = 800  # use capslock for constants (you don't want to change values)
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
ROWS = 16  # rows of the level
TILE_SIZE = SCREEN_HEIGHT // ROWS

PLAYER_SCALE = 0.47  # control image size of player
PLAYER_SPEED = 5  # control speed of player
GRAVITY = 0.75  # effects how quickly you fall down after jump
SCROLL_TRESH = 200  # if you get within 200 pixels of the edge, the screen will move

x = 100
y = 5


class TestFighter(unittest.TestCase):
    """
    """

    def test_move(self):
        """
        """
        print('tile size: ', TILE_SIZE)
        player = Fighter('player', x * TILE_SIZE, y * TILE_SIZE, PLAYER_SCALE, PLAYER_SPEED, facing_left=True)
        print(player.rect.x)
        player.move(moving_left=False, moving_right=True, obstacle_list=[])
        print(player.rect.x)
        self.assertEqual(x * TILE_SIZE - PLAYER_SPEED, player.rect.x, f"{player.rect.x}")



    def test_collision(self):
        obstacle_list = (0, (x * TILE_SIZE), (y * TILE_SIZE))

        # Check whether you hit/touch something (collision)
        for tile in obstacle_list:
            # check the collision of the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,
                                   self.height):  # colliderect check for collision with other rectangle
                dx = 0  # if your next move would be to hit something, don't do that so put movement to 0
                # if ai has hat a wall, make them turn around and not run into it continuously


#
#  if moving_left:  # if moving left is true
#         dx = -self.speed  # your x coordinate decreases by your speed
#         self.flip = True  # flip layer
#         self.direction = -1  # looking left
#
# def move(self, moving_left: bool, moving_right: bool,
#          obstacle_list: list[tuple[pygame.Surface, pygame.Rect]]) -> int:  #
#     """Initializes movement of the player, collision with objects and scrolling of the screen
#
#     :param moving_left: True if the player is moving left
#     :param moving_right: True if the player is moving right
#     :param obstacle_list: A tuple containing a list of all obstacles. Which is tile information for only things that
#      are seen as obstacles (e.g., things the player can walk into like a wall, or the ground). This info includes
#       an image of the obstacle and a position of the obstacle.
#     :return: Returns screen_scroll if player
#     """
#
#     # reset movement of the variables
#     screen_scroll = 0  # no scrolling by default
#     dx = 0  # change in x
#     dy = 0  # change in y
#
#     # assign movement o the variables if they are moving right or left
#     if moving_left:  # if moving left is true
#         dx = -self.speed  # your x coordinate decreases by your speed
#         self.flip = True  # flip layer
#         self.direction = -1  # looking left
#     if moving_right:  # if moving right is true
#         dx = self.speed  # your y coordinate increases by your speed
#         self.flip = False  # don't flip
#         self.direction = 1  # looking right
#     # change the position of the sword range (forward or behind the center of the player, thus letting it go left
#     # or right)
#     self.attack_range_rect.center = (
#     self.rect.centerx + self.attack_range_rect.width // 2 * self.direction, self.rect.centery)
#
#     # jump
#     if self.jump and self.in_air == False:  # if jump is true and you are not in the air (prevens double jump)
#         self.speed_y = -15  # changes how high the player jumps
#         # add jumping sound
#         jump_sound = pygame.mixer.Sound('audio/jump.wav')  # use later in keys section
#         jump_sound.set_volume(0.5)
#         jump_sound.play()  # add jumping sound
#         self.jump = False  # jump ends
#         self.in_air = True  # you are in the air
#
#     # add gravity for the jump so you come back down after jump
#     self.speed_y += GRAVITY  # jump starts with high number and slowly decreases by gravity making you fall down
#     if self.speed_y > 10:  # if speed > 10
#         self.speed_y  # set it to 10 (never go past limit)
#     dy += self.speed_y  # change in y coordinate
#
#     # Check whether you hit/touch something (collision)
#     for tile in obstacle_list:
#         # check the collision of the x direction
#         if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,
#                                self.height):  # colliderect check for collision with other rectangle
#             dx = 0  # if your next move would be to hit something, don't do that so put movement to 0
#             # if ai has hat a wall, make them turn around and not run into it continuously
#             if self.char_type == 'enemy':  # if enemy (hits something)
#                 self.direction *= -1  # go to the other side
#                 self.move_counter = 0  # reset the movement counter
#         # check collision in y direction
#         if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width,
#                                self.height):  # colliderect check for collision with other rectangle
#             # check if the character is below the obstacle, aka, jumping, aka hitting something above
#             if self.speed_y < 0:  # if the speed is negative you are going up
#                 self.speed_y = 0  # set speed to 0, thus stop once you hit obstacle
#                 dy = tile[
#                          1].bottom - self.rect.top  # change of position will be bottom of the tile - head (top) of character
#             # check if above ground, whether he's falling
#             elif self.speed_y >= 0:  # if you're falling and going to hit an object
#                 self.speed_y = 0  # the speed becomes 0
#                 self.in_air = False  # you are not in air anymore
#                 dy = tile[
#                          1].top - self.rect.bottom  # if the change of position will be top of the tile - feet (bottom) character
#                 self.jump = False  # prevents you from loading a jump while your in air which will be activated when you reach te ground
#
#     # check whether you've fallen of the map and die
#     if self.rect.bottom > SCREEN_HEIGHT:  # if your feet are bigger than the screen height (aka you've fallen of)
#         self.health = 0  # your health is 0
#
#     # fix that the player can't fall of the map
#     if self.char_type == 'player':  # only if character is player
#         if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:  # if you fall of left or right side of lvl
#             dx = 0  # make the movement null: stop the movement
#     # update the position of rectangle
#     self.rect.x += dx  # update position by dx
#     self.rect.y += dy  # update position by dy
#
#     # update scroll based on the position of the player
#     if self.char_type == 'player':  # only if character is player
#         # if you are about to hit border of the screen: right of rect is > screen width - 200 pixels or left side is smaller than the treshold (cause x coordinate star with 0)
#         if self.rect.right > SCREEN_WIDTH - SCROLL_TRESH or self.rect.left < SCROLL_TRESH:
#             self.rect.x -= dx  # the change becomes 0, thus you stay in the same place
#             screen_scroll = -dx  # move the screen to the opposite side of where the player is going
#
#         return screen_scroll  # we need to use this later thus need to return it
#
#
#
#
#
#
#


if __name__ == '__main__':
    unittest.main()
