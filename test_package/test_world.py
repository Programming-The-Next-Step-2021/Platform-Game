import unittest
from code.world import World
from code.main import read_world_data, read_images
import pygame
import code
from code.fighter import Fighter
from code.terrain_objects import Decoration, Water, ItemBox, Exit


# Get necessary things for the test

health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
item_boxes = {
    'Health': health_box_img
}
level = 1
img_list = read_images()
world_data = read_world_data(level)
world = code.world.World()


class TestWorld(unittest.TestCase):
    """
    Tests whether in world.py certain objects (e.g., player) are an instance of a certain class (e.g., Fighter)
    """

    def test_process_data(self):
        """
        Test whether in world.py certain objects (e.g., player) are an instance of a certain class (e.g., Fighter)
        """
        player, enemy_group, decoration_group, water_group, item_box_group, exit_group = \
            world.process_data(world_data, img_list, item_boxes)
        # check whether player is an instance of the Fighter class
        self.assertIsInstance(player, Fighter)
        # test whether all enemies are an instance of Fighter class
        self.assertTrue(all([isinstance(enemy, Fighter) for enemy in enemy_group.sprites()]))
        # test whether all decoration is an instance of Decoration class
        self.assertTrue(all([isinstance(decoration, Decoration) for decoration in decoration_group.sprites()]))
        # test whether all water is an instance of Water class
        self.assertTrue(all([isinstance(water, Water) for water in water_group.sprites()]))
        # test whether all item boxes are an instance of ItemBox class
        self.assertTrue(all([isinstance(item_box, ItemBox) for item_box in item_box_group.sprites()]))
        # test whether all exits are an instance of Exit class
        self.assertTrue(all([isinstance(exit, Exit) for exit in exit_group.sprites()]))



if __name__ == '__main__':
    unittest.main()