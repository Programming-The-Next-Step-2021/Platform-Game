import pygame


pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')


class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha() # how big you want a blank surface to be where individual images will be drawn on
        # take from the image starting from 0,0 and show it on the above specified surface
        image.blit(self.sheet, (0, 0), ((frame * width), height, width, height)) # TODO: changed height third before end
        # resize the image to a certain scale
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        # this takes away the background color of the image (thus making it transparant)
        image.set_colorkey(colour)

        return image

sprite_sheet_image = pygame.image.load('img/enemy/sprite_sheets/1.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (255, 0, 255)


frame_0 = sprite_sheet.get_image(0, 66, 77, 1, BLACK)
frame_1 = sprite_sheet.get_image(1, 66, 77, 1, BLACK)
frame_2 = sprite_sheet.get_image(2, 66, 77, 1, BLACK)
frame_3 = sprite_sheet.get_image(3, 66, 77, 1, BLACK)

run = True
while run:

    #update background
    screen.fill(BG)

    #show frame image
    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (72, 0))
    screen.blit(frame_2, (150, 0))
    screen.blit(frame_3, (250, 0))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()