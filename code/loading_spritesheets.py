import pygame

pygame.init()

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')


class SpriteSheet():
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, image) -> None:
        self.sheet = image

    def get_image(self, start_pos_y, frame, width, height, scale, colour) -> pygame.Surface:
        image = pygame.Surface((width, height), pygame.SRCALPHA)  # how big you want a blank surface to be where
        # individual images will be drawn on
        # take from the image starting from 0,0 and show it on the above specified surface
        image.blit(self.sheet, (0, 0), ((frame * width), start_pos_y * height, width, height))
        # resize the image to a certain scale
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        # this takes away the background color of the image (thus making it transparant)
        image.set_colorkey(colour)

        return image


SPRITESHEET_NAME = 'King_Slime_Death4'
BG = (50, 50, 50)
PINK = (255, 0, 255)
TRANS = (0, 0, 0)
RED = (255, 0, 0)

WIDTH = 245
HEIGHT = 244

num_of_frames = 3
start_pos_y = 0

sprite_sheet_image = pygame.image.load(f'../static/img/enemy/sprite_sheets/{SPRITESHEET_NAME}.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)
action = 'death4'

frames = []
for frame_num in range(num_of_frames):
    frame = sprite_sheet.get_image(start_pos_y, frame_num, WIDTH, HEIGHT, 1, TRANS)
    frames.append(frame)
    pygame.image.save(frame, f'../static/img/boss_enemy/{action}/{frame_num}.png')

# pygame.image.save(frame_0, 'static/img/player/normal/0.png')
# pygame.image.save(frame_1, 'static/img/player/1.png')
# pygame.image.save(frame_2, 'static/img/player/2.png')
# pygame.image.save(frame_3, 'static/img/player/3.png')


run = True
scale = 0.5
while run:

    # update background
    screen.fill(BG)

    for frame_num in range(num_of_frames):
        # show frame image
        frame = frames[frame_num]
        frame = pygame.transform.scale(frame, (int(WIDTH * scale), int(HEIGHT * scale)))
        rect = screen.blit(frame, (frame_num * WIDTH * scale, 0))
        pygame.draw.rect(screen, RED, rect, 1)  # draw red rectangle around the character
        # print(bla.get_rect())

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
