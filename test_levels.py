import pygame

from graphics.plants import PlantSystem
from graphics.grass import GrassSystem
from graphics.sprite_stacks import SpritestackAsset

from general_game_mechanics.dynamic_objects import DynamicObject, Character # , Vehicle

from world_builder.level_editor import Level
from world_builder.loadpoints import LoadPoint

from presets import particle_presets


pygame.init()


class Game:
    def __init__(self):
        
        """ DISPLAY SETTINGS """
        self.screen_width = 800
        self.screen_height = 600

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.current_level = None

        pygame.display.set_caption("SANDBOX")

        self.clock = pygame.time.Clock()
        self.time = 0


        """ PLAYER ASSETS """
        self.player_asset = SpritestackAsset(type='character', name='dude', hitbox_size=(16, 16), scale=1, movelocked=False)


        """ NPC ASSETS """
        self.npc_assets = []


        """ VEHICLE ASSETS """
        self.vehicle_assets = [
            SpritestackAsset(type='vehicle', name='cop_car', hitbox_size=(64,36), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='vehicle', name='pickup_truck', hitbox_size=(64,36), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='vehicle', name='hippie_van', hitbox_size=(64,36), hitbox_type='circle', movelocked=False),
        ]


        """ NON-INTERACTABLE SPRITE STACK ASSETS """
        self.non_interactable_sprite_stack_assets = [
            SpritestackAsset(type='texture', name='branches_1', hitbox_size=(32,32), hitbox_type='circle', y0_base_offset=-1000),
            SpritestackAsset(type='house_1_interior', name='floor_1', hitbox_size=(32,32), scale=1, hitbox_type='circle', y0_base_offset=-2000),
            SpritestackAsset(type='house_1_interior', name='carpet_1', hitbox_size=(32,32), scale=1, hitbox_type='circle', y0_base_offset=-1500),
        ]


        """ DYNAMIC SPRITE STACK ASSETS """
        self.dynamic_sprite_stack_assets = [

            # BUILDINGS
            SpritestackAsset(type='building', name='house_1', hitbox_size=(128,128), hitbox_type='circle'),
            SpritestackAsset(type='building', name='red_barn', hitbox_size=(128,128), hitbox_type='circle'),
            SpritestackAsset(type='building', name='shed', hitbox_size=(64,45), hitbox_type='circle'),
            SpritestackAsset(type='building', name='toilet', hitbox_size=(45,45), hitbox_type='circle'),

            # FENCES
            SpritestackAsset(type='fence', name='fence_1', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_2', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_3', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_4', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_5', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_6', hitbox_size=(32,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_7', hitbox_size=(10,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_8', hitbox_size=(10,10), hitbox_type='circle'),
            SpritestackAsset(type='fence', name='fence_9', hitbox_size=(10,10), hitbox_type='circle'),

            # WALLS
            SpritestackAsset(type='wall', name='wall_1', hitbox_size=(32,20), hitbox_type='circle'),
            SpritestackAsset(type='wall', name='wall_2', hitbox_size=(32,20), hitbox_type='circle'),
            SpritestackAsset(type='wall', name='wall_3', hitbox_size=(32,20), hitbox_type='circle'),
            SpritestackAsset(type='wall', name='wall_4', hitbox_size=(32,20), hitbox_type='circle'),
            SpritestackAsset(type='wall', name='wall_5', hitbox_size=(32,20), hitbox_type='circle'),

            # WINDMILLS
            SpritestackAsset(type='windmill', name='windmill_1', hitbox_size=(32,32), hitbox_type='circle'),

            # WELLS
            SpritestackAsset(type='well', name='well_1', hitbox_size=(50,50), hitbox_type='circle'),

            # TREES
            SpritestackAsset(type='tree', name='tree_1', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_2', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_3', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_4', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_5', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_6', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_7', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_8', hitbox_size=(20,20), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_9', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_trunk_1', hitbox_size=(25,25), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_trunk_2', hitbox_size=(25,25), hitbox_type='circle'),
            SpritestackAsset(type='tree', name='tree_trunk_3', hitbox_size=(25,25), hitbox_type='circle'),

            # ROCKS
            SpritestackAsset(type='rock', name='rock_1', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_2', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_3', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_4', hitbox_size=(32,32), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_5', hitbox_size=(32,32), hitbox_type='circle'),

            # CRATES
            SpritestackAsset(type='crate', name='crate_1', hitbox_size=(32,20), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='crate', name='crate_2', hitbox_size=(32,32), hitbox_type='circle', movelocked=False),

            # HAY BALES
            SpritestackAsset(type='hay_bale', name='hay_bale_1', hitbox_size=(32,32), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='hay_bale', name='hay_bale_2', hitbox_size=(32,32), hitbox_type='circle', movelocked=False),

            # BARRELS
            SpritestackAsset(type='barrel', name='barrel_1', hitbox_size=(16,16), hitbox_type='circle', movelocked=False),
            SpritestackAsset(type='barrel', name='barrel_2', hitbox_size=(16,16), hitbox_type='circle', movelocked=False),

            # WHEELBARROWS
            SpritestackAsset(type='wheelbarrow', name='wheelbarrow_1', hitbox_size=(25,25), hitbox_type='circle', movelocked=False),

            # WATER TOWERS
            SpritestackAsset(type='water_tower', name='water_tower_1', hitbox_size=(64,64), hitbox_type='circle'),

            # CAMPFIRES
            SpritestackAsset(type='campfire', name='campfire_1', hitbox_size=(32,32), hitbox_type='circle'),

            # INTERIOR
            SpritestackAsset(type='house_1_interior', name='wall_north', hitbox_size=(32,32), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='wall_east', hitbox_size=(32,32), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='wall_south', hitbox_size=(32,32), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='wall_west', hitbox_size=(32,32), scale=1, hitbox_type='circle'),

            # FURNITURE
            SpritestackAsset(type='house_1_interior', name='table_1', hitbox_size=(30,50), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='chair_1', hitbox_size=(20,20), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='cabinet_1', hitbox_size=(20,20), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='shelf_1', hitbox_size=(20,20), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='bed_1', hitbox_size=(20,20), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='chest_1', hitbox_size=(20,20), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='chair_2', hitbox_size=(20,20), scale=1, hitbox_type='circle'),
            SpritestackAsset(type='house_1_interior', name='wardrobe_1', hitbox_size=(32,32), scale=1, hitbox_type='circle'),
            
        ]


        """ PLANT SYSTEM ASSETS """
        self.plant_systems = [
            PlantSystem(
                folder='assets/_plant_assets/bush_1',
                num_branches_range = (4,7),
                base_angle_range = (30, 70),
                stiffness_range = (0.005, 0.02),
                relax_speed=0.2,
                scale=1
            ),
            PlantSystem(
                folder='assets/_plant_assets/bush_2',
                num_branches_range = (1,10),
                base_angle_range = (70, 80),
                stiffness_range = (0.005, 0.02),
                relax_speed=0.2,
                scale=1
            ),
            PlantSystem(
                folder='assets/_plant_assets/bush_3',
                num_branches_range = (1,8),
                base_angle_range = (70, 80),
                stiffness_range = (0.005, 0.02),
                relax_speed=0.2,
                scale=1
            ),
            PlantSystem(
                folder='assets/_plant_assets/bush_4',
                num_branches_range = (1,4),
                base_angle_range = (5, 15),
                stiffness_range = (0.1, 0.03),
                relax_speed=0.2,
                scale=1
            ),
        ]


        """ GRASS SYSTEM ASSETS """
        self.grass_systems = [
            GrassSystem(
                folder = 'assets/_grass_assets/grass_1',
                min_tile_size=20,
                max_tile_size=40,
                min_num_blades=2,
                max_num_blades=10,
                stiffness=0.1,
                num_assets=10,
                scale=0.5
            ),
            GrassSystem(
                folder = 'assets/_grass_assets/grass_2',
                min_tile_size=20,
                max_tile_size=40,
                min_num_blades=2,
                max_num_blades=10,
                stiffness=0.1,
                num_assets=10,
                scale=0.5
            ),
        ]


        """ PARTICLE SYSTEM PRESETS """
        self.particle_system_presets = [
            particle_presets.flame,
        ]


        """ LEVELS """
        # OUTDOORS LEVEL
        self.outdoors_level = Level(
            game=self,
            name='outdoors_level',
            map_size=(1000, 1000),
            background=None,
            fill_colour=(105, 66, 56)
        )
        # HOUSE_1 LEVEL
        self.house_1_level = Level(
            game=self,
            name='house_1_level',
            map_size=(500, 500),
            background=None,
            fill_colour=(20, 0, 20)
            )

        """ LOADPOINTS BETWEEN LEVELS"""
        # OUTDOORS LEVEL
        self.outdoors_level.loadpoint_levels = [
            self.house_1_level,
        ]
        # HOUSE_1 LEVEL
        self.house_1_level.loadpoint_levels = [
            self.outdoors_level,
        ]




    def run(self):
        self.current_level = self.outdoors_level
        self.current_level.load_level()
        while 1 != 0:
            self.handle_events()
            self.update_screen_game()


    def handle_events(self):
        self.events = pygame.event.get()
        keys = pygame.key.get_pressed()
        self.current_level.handle_controls_editing(keys)
        self.current_level.edit_level()
        self.current_level.camera.handle_movement(keys)


    def update_screen_game(self):

        self.current_level.render()
        self.current_level.update()
        pygame.display.update()

        self.clock.tick(110)
        self.time += 1


if __name__ == "__main__":
    game = Game()
    game.run()
