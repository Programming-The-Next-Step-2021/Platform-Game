import unittest
import pygame
from main import read_images, read_world_data

level = 1  # to test the read_world_data()
ROWS = 16  # rows of the level needed to test read_world_data()
COLS = 150  # colums of the level needed to test read_world_data()


class TestMain(unittest.TestCase):
    """
    Class to test functions in main file
    """

    # test if img_list has images in it
    def test_read_images(self):
        img_list = read_images()
        # check for all images in img_list whether they are a pygame.Surface
        self.assertTrue(all([isinstance(image, pygame.Surface) for image in img_list]))

    # test whether the world data contains a list of lists with integers (loaded csv file)
    def test_read_world_data(self):
        world_data = read_world_data(level)
        self.assertTrue(all([isinstance(integer, int) for list in world_data for integer in list]))


if __name__ == '__main__':
    unittest.main()
