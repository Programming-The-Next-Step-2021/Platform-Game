import pygame


pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')



class SpriteSheet():
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, image) -> None:
        self.sheet = image

    def get_image(self, start_pos_y, frame, width, height, scale, colour) -> pygame.Surface:
        image = pygame.Surface((width, height), pygame.SRCALPHA) # how big you want a blank surface to be where individual images will be drawn on
        # take from the image starting from 0,0 and show it on the above specified surface
        image.blit(self.sheet, (0, 0), ((frame * width), start_pos_y*height, width, height)) # TODO: changed height third before end
        # resize the image to a certain scale
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        # this takes away the background color of the image (thus making it transparant)
        image.set_colorkey(colour)

        return image

SPRITESHEET_NAME = 'normal'
BG = (50, 50, 50)
PINK = (255, 0, 255)
TRANS = (0, 0, 0)
RED = (255, 0, 0)

WIDTH = 144
HEIGHT = 142

num_of_frames = 6
start_pos_y = 0

sprite_sheet_image = pygame.image.load(f'img/player/sprite_sheets/{SPRITESHEET_NAME}.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)



frames = []
for frame_num in range(num_of_frames):

    frame = sprite_sheet.get_image(start_pos_y, frame_num, WIDTH, HEIGHT, 1, TRANS)
    frames.append(frame)
    pygame.image.save(frame, f'img/player/{SPRITESHEET_NAME}/{frame_num}.png')

# pygame.image.save(frame_0, 'img/player/normal/0.png')
# pygame.image.save(frame_1, 'img/player/1.png')
# pygame.image.save(frame_2, 'img/player/2.png')
# pygame.image.save(frame_3, 'img/player/3.png')


run = True
while run:

    #update background
    screen.fill(BG)

    for frame_num in range(num_of_frames):
        #show frame image
        frame = frames[frame_num]
        rect = screen.blit(frame, (frame_num * WIDTH, 0))
        pygame.draw.rect(screen, RED, rect, 1)  # draw red rectangle around the character
        # print(bla.get_rect())


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()