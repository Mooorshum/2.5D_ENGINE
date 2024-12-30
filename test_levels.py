import pygame

from graphics.plants import PlantSystem
from graphics.grass import GrassSystem

from general_game_mechanics.dynamic_objects import DynamicObject, Vehicle
from graphics.camera import Camera

from world_builder.level_editor import Level


pygame.init()


class Game:
    def __init__(self):

        """ MAP SETTINGS """
        self.map_width = 2000
        self.map_height = 2000
        
        """ DISPLAY SETTINGS """
        self.screen_width = 800
        self.screen_height = 600

        """ RENDER RESOLUTION """
        self.render_width = 400
        self.render_height = 300

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.camera = Camera(
            width=self.render_width,
            height=self.render_height,
            map_width=self.map_width,
            map_height=self.map_height
        )

        pygame.display.set_caption("SANDBOX")

        self.clock = pygame.time.Clock()
        self.time = 0


        """ GAME ASSETS """

        self.sprite_stack_assets = [
            Vehicle(type='vehicle', name='cop_car'),
            Vehicle(type='vehicle', name='pickup_truck'),
            DynamicObject(type='building', name='house_1', movelocked=True),
            DynamicObject(type='building', name='red_barn', movelocked=True),
            DynamicObject(type='building', name='shed', movelocked=True),
            DynamicObject(type='building', name='toilet', movelocked=True),
            DynamicObject(type='filler_object', name='tree_1', movelocked=True),
            DynamicObject(type='filler_object', name='tree_2', movelocked=True),
            DynamicObject(type='filler_object', name='tree_3', movelocked=True),
            DynamicObject(type='filler_object', name='tree_4', movelocked=True),
            DynamicObject(type='filler_object', name='tree_5', movelocked=True),
            DynamicObject(type='filler_object', name='tree_6', movelocked=True),
            DynamicObject(type='filler_object', name='tree_7', movelocked=True),
            DynamicObject(type='filler_object', name='tree_8', movelocked=True),
            DynamicObject(type='filler_object', name='tree_trunk_2', movelocked=True),
            DynamicObject(type='filler_object', name='tree_trunk_3', movelocked=True),
            DynamicObject(type='filler_object', name='rock_1', movelocked=True),
            DynamicObject(type='filler_object', name='rock_2', movelocked=True),
            DynamicObject(type='filler_object', name='rock_3', movelocked=True),
            DynamicObject(type='filler_object', name='rock_4', movelocked=True),
            DynamicObject(type='filler_object', name='rock_5', movelocked=True),
            DynamicObject(type='filler_object', name='well', movelocked=True),
            DynamicObject(type='filler_object', name='campfire', movelocked=True),
            DynamicObject(type='filler_object', name='crate_1', mass=200),
            DynamicObject(type='filler_object', name='hay_bale_1', mass=100),
            DynamicObject(type='filler_object', name='hay_bale_2', mass=500),
            DynamicObject(type='filler_object', name='wheelbarrow', scale=1.2, mass=100),
        ]

        self.plant_systems = [
            PlantSystem(
                folder='assets/branchy_bush',
                num_branches_range = (1,7),
                base_angle_range = (-1.2, 1.2),
                stiffness_range = (0.01, 0.2),
                gravity = 0.1,
                scale=0.5
            ),
            PlantSystem(
                folder='assets/fern',
                num_branches_range = (5,8),
                base_angle_range = (-1.2, 1.2),
                stiffness_range = (0.01, 0.2),
                gravity = 0.1,
                scale=0.75
            ),
        ]

        self.grass_systems = [
            GrassSystem(
                folder = 'assets/grass',
                min_tile_size=5,
                max_tile_size=20,
                min_num_blades=2,
                max_num_blades=10,
                stiffness=0.03,
                scale=0.5,
                num_assets=10
            ),
        ]

        self.particle_systems = [

        ]


        """ TEST LEVEL """
        self.test_level = Level(self)


    def run(self):
        while 1 != 0:
            self.handle_events()
            self.update_screen_game()


    def handle_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        self.test_level.handle_controls_editing(keys, events)
        self.test_level.edit_level()
        self.camera.handle_movement(keys)


    def update_screen_game(self):

        self.test_level.render()
        self.test_level.update()
        pygame.display.update()

        self.clock.tick(110)
        self.time += 1


if __name__ == "__main__":
    game = Game()
    game.run()
