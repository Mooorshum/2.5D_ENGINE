import pygame

import os

from objects.plants import PlantSystem
from objects.grass import GrassSystem
from graphics.sprite_stacks import SpritestackAsset

from world_builder.level_editor import Level

from assets import particle_systems, vehicles, diner, bus_stop, water_tower, road, billboards, utility_poles, cacti, rocks, characters, textures, decor

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()


class Game:
    def __init__(self):
        
        """ DISPLAY SETTINGS """
        scale = 1 #0.75 #0.6 # Percentage of max screen
        ratio = 2 #16/9 #4/3 # WIDTH / HEIGHT ratio    ### INTERESTING OBSERVATION: A HORIZONTALLY STRETCHED PICTURE SEEMS TO HAVE MORE DEPTH

        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        if ratio >= 1:
            self.screen_width = int(screen_height * ratio * scale)
            self.screen_height = int(screen_height * scale)
        else:
            self.screen_width = int(screen_width * scale)
            self.screen_height = int(screen_width / ratio * scale)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.current_level = None

        pygame.display.set_caption("SANDBOX")

        self.clock = pygame.time.Clock()
        self.time = 0


        """ PLAYER ASSETS """
        self.player_asset = characters.DUDE
        self.player_asset.load_asset()

        """ NPC ASSETS """
        self.npc_assets = []

        """ NON-INTERACTABLE SPRITE STACK ASSETS """
        self.texture_assets = [
            textures.STONE_TILE,
        ]
        for asset in self.texture_assets:
            asset.load_asset()

        """ DYNAMIC SPRITE STACK ASSETS """
        self.object_assets = [
            decor.POSTER_STAND,

            cacti.CACTUS_1,
            cacti.CACTUS_2,
            cacti.CACTUS_3,
            cacti.CACTUS_4,
            cacti.CACTUS_5,
            cacti.CACTUS_6,

            rocks.RED_ROCKS_1,
            rocks.RED_ROCKS_2,
            rocks.RED_ROCKS_3,
            rocks.RED_ROCKS_4,
            rocks.RED_ROCKS_5,
            rocks.RED_ROCKS_6,
            rocks.RED_ROCKS_7,

        ]
        for asset in self.object_assets:
            asset.load_asset()


        """ PLANT SYSTEM ASSETS """
        self.plant_systems = [
            PlantSystem(
                folder='asset_files/_plant_assets/bush_1',
                num_branches_range = (4,7),
                base_angle_range = (30, 70),
                stiffness_range = (0.005, 0.02),
                relax_speed=0.2,
                scale=1
            ),
        ]


        """ GRASS SYSTEM ASSETS """
        self.grass_systems = [
            GrassSystem(
                folder = 'asset_files/_grass_assets/grass_1',
                min_tile_size=32,
                max_tile_size=32,
                min_num_blades=2,
                max_num_blades=10,
                stiffness=0.1,
                num_assets=10,
                scale=0.5
            ),
        ]


        """ PARTICLE SYSTEM ASSETS """
        self.particle_system_assets = [
            particle_systems.flame_fireplace,
        ]


        """ VEHICLE ASSETS """
        self.vehicle_assets = [
            vehicles.DELIVERY_TRUCK,
            vehicles.MINIVAN,
        ]
        for asset in self.vehicle_assets:
            asset.load_asset()

        """ COMPOSITE OBJECTS """
        self.composite_object_assets = [
            diner.DINER_WALLS,
            diner.DINER_ROOF,

            water_tower.WATER_TOWER_BOTTOM,
            water_tower.WATER_TOWER_MIDDLE,
            water_tower.WATER_TOWER_TOP,
            water_tower.WATER_TOWER_ROOF,

            bus_stop.BUS_STOP,

            road.TWO_WAY_ROAD,

            billboards.BEANZ_BILLBOARD,

            utility_poles.WOODEN_POLE,
            utility_poles.WIRELINE,
            
        ]
        for asset in self.composite_object_assets:
            asset.load_asset()



        """ LEVELS """
        # OUTDOORS LEVEL
        self.outdoors_level = Level(
            game=self,
            name='outdoors_level',
            map_size=(1024, 1024),
            background='asset_files/texture/cracked_desert/sprite_stacks/stack_0.png',
            fill_colour=(161, 77, 47)#(168, 78, 50)
        )
        self.outdoors_level.composite_object_assets = self.composite_object_assets
        self.outdoors_level.vehicle_assets = self.vehicle_assets
        self.outdoors_level.texture_assets = self.texture_assets
        self.outdoors_level.object_assets = self.object_assets
        self.outdoors_level.plant_systems = self.plant_systems
        self.outdoors_level.grass_systems = self.grass_systems
        self.outdoors_level.particle_system_assets = self.particle_system_assets
        self.outdoors_level.npc_assets = self.npc_assets
        







        """ # HOUSE_1 LEVEL
        self.house_1_level = Level(
            game=self,
            name='house_1_level',
            map_size=(500, 500),
            fill_colour=(20, 0, 20)
            )

        # TENT_1 LEVEL
        self.tent_1_level = Level(
            game=self,
            name='tent_1_level',
            map_size=(128, 80),
            fill_colour=(20, 0, 20)
            ) """



        """ LOADPOINTS BETWEEN LEVELS"""
        """ # OUTDOORS LEVEL
        self.outdoors_level.loadpoint_levels = [
            self.house_1_level,
            self.tent_1_level
        ] """

        """ # HOUSE_1 LEVEL
        self.house_1_level.loadpoint_levels = [
            self.outdoors_level,
        ]

        # TENT_1 LEVEL
        self.tent_1_level.loadpoint_levels = [
            self.outdoors_level,
        ] """



    def run(self):
        self.current_level = self.outdoors_level
        """ self.current_level.load_level() """
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

        self.clock.tick(80)
        self.time += 1


if __name__ == "__main__":
    game = Game()
    game.run()
