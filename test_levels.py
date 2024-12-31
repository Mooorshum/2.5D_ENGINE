import pygame

from graphics.plants import PlantSystem
from graphics.grass import GrassSystem
from graphics.sprite_stacks import SpritestackModel

from general_game_mechanics.dynamic_objects import DynamicObject, Vehicle, Character
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

            Vehicle(type='vehicle', name='cop_car', hitbox_size=(64,36)),
            Vehicle(type='vehicle', name='pickup_truck', hitbox_size=(64,36)),
            Vehicle(type='vehicle', name='hippie_van', hitbox_size=(64,36)),

            SpritestackModel(type='filler_object', name='campfire', hitbox_size=(32,32), y0_base_offset=-100),

            DynamicObject(type='building', name='house_1', hitbox_size=(128,128), movelocked=True),
            DynamicObject(type='building', name='red_barn', hitbox_size=(128,128), movelocked=True),
            DynamicObject(type='building', name='shed', hitbox_size=(64,45), movelocked=True),
            DynamicObject(type='building', name='toilet', hitbox_size=(45,45), movelocked=True),
            DynamicObject(type='filler_object', name='tree_1', hitbox_size=(20,20), movelocked=True),
            DynamicObject(type='filler_object', name='tree_2', hitbox_size=(20,20), movelocked=True),
            DynamicObject(type='filler_object', name='tree_3', hitbox_size=(20,20), movelocked=True),
            DynamicObject(type='filler_object', name='tree_4', hitbox_size=(20,20), movelocked=True),
            DynamicObject(type='filler_object', name='tree_5', hitbox_size=(20,20), movelocked=True),
            DynamicObject(type='filler_object', name='tree_6', hitbox_size=(20,20), movelocked=True),
            DynamicObject(type='filler_object', name='tree_7', hitbox_size=(32,32), movelocked=True),
            DynamicObject(type='filler_object', name='tree_8', hitbox_size=(20,20), movelocked=True),
            DynamicObject(type='filler_object', name='tree_9', hitbox_size=(32,32), movelocked=True),
            DynamicObject(type='filler_object', name='tree_trunk_2', hitbox_size=(25,25), movelocked=True),
            DynamicObject(type='filler_object', name='tree_trunk_3', hitbox_size=(25,25), movelocked=True),
            DynamicObject(type='filler_object', name='rock_1', hitbox_size=(32,32), movelocked=True),
            DynamicObject(type='filler_object', name='rock_2', hitbox_size=(32,32), movelocked=True),
            DynamicObject(type='filler_object', name='rock_3', hitbox_size=(32,32), movelocked=True),
            DynamicObject(type='filler_object', name='rock_4', hitbox_size=(32,32), movelocked=True),
            DynamicObject(type='filler_object', name='rock_5', hitbox_size=(32,32), movelocked=True),
            DynamicObject(type='filler_object', name='well', hitbox_size=(50,50), movelocked=True),
            DynamicObject(type='filler_object', name='crate_1', hitbox_size=(32,20), mass=200),
            DynamicObject(type='filler_object', name='hay_bale_1', hitbox_size=(32,32), mass=100),
            DynamicObject(type='filler_object', name='hay_bale_2', hitbox_size=(32,32), mass=500),
            DynamicObject(type='filler_object', name='wheelbarrow', hitbox_size=(25,25), scale=1.2, mass=100),
        ]

        self.plant_systems = [
            PlantSystem(
                folder='assets/branchy_bush',
                num_branches_range = (1,7),
                base_angle_range = (-1.2, 1.2),
                stiffness_range = (0.1, 0.1),
                gravity = 0.1,
                scale=0.3
            ),
            PlantSystem(
                folder='assets/fern',
                num_branches_range = (5,8),
                base_angle_range = (-1.2, 1.2),
                stiffness_range = (0.1, 0.1),
                gravity = 0.1,
                scale=0.3
            ),
        ]

        self.grass_systems = [
            GrassSystem(
                folder = 'assets/grass',
                min_tile_size=5,
                max_tile_size=20,
                min_num_blades=2,
                max_num_blades=10,
                stiffness=0.1,
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
