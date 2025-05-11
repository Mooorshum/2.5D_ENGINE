import pygame

import os


from graphics.plants import PlantSystem
from graphics.grass import GrassSystem
from graphics.sprite_stacks import SpritestackAsset

from general_game_mechanics.dynamic_objects import CompositeObject, Vehicle

from world_builder.level_editor import Level

from presets import particle_presets

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()


class Game:
    def __init__(self):
        
        """ DISPLAY SETTINGS """
        scale = 0.4 #0.6 # 0.75 # Percentage of max screen
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
        self.player_asset = SpritestackAsset(type='character', name='dude', hitbox_size=(16, 16), mass=1000, hitbox_type='circle')


        """ NPC ASSETS """
        self.npc_assets = []


        """ VEHICLE ASSETS """
        self.vehicle_assets = [
            #SpritestackAsset(type='vehicle', name='cop_car', hitbox_size=(64,36), mass=1000, hitbox_type='rectangle'),
            #SpritestackAsset(type='vehicle', name='pickup_truck', hitbox_size=(64,36), mass=1000, hitbox_type='rectangle'),
            #SpritestackAsset(type='vehicle', name='hippie_van', hitbox_size=(64,36), mass=1000, hitbox_type='rectangle'),
        ]


        """ NON-INTERACTABLE SPRITE STACK ASSETS """
        self.texture_assets = [
            SpritestackAsset(type='texture', name='branches_1', hitbox_size=(32,32), hitbox_type='rectangle'),
            SpritestackAsset(type='house_1_interior', name='floor_1', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            SpritestackAsset(type='house_1_interior', name='carpet_1', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            SpritestackAsset(type='tent_1_interior', name='floor_1', hitbox_size=(80,80), scale=1, hitbox_type='rectangle'),
            SpritestackAsset(type='tent_1_interior', name='cow_hide_1', hitbox_size=(80,80), scale=1, hitbox_type='rectangle'),
            SpritestackAsset(type='tent_1_interior', name='bed_1', hitbox_size=(80,80), scale=1, hitbox_type='rectangle'),

            SpritestackAsset(type='water_surface', name='sea_surface_1', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            SpritestackAsset(type='water_surface', name='sea_surface_2', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            SpritestackAsset(type='water_surface', name='sea_surface_4', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),

            SpritestackAsset(type='pier', name='pier_1', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            SpritestackAsset(type='cliff', name='cliff_pier', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),

            SpritestackAsset(type='texture', name='grass_64', hitbox_size=(64,64), hitbox_type='rectangle'),

            SpritestackAsset(type='stone_tile', name='stone_tile_1', hitbox_size=(32,32), hitbox_type='rectangle'),

        ]


        """ DYNAMIC SPRITE STACK ASSETS """
        self.object_assets = [

            # BUILDINGS
            #SpritestackAsset(type='building', name='house_1', hitbox_size=(128,128), hitbox_type='rectangle'),
            #SpritestackAsset(type='building', name='red_barn', hitbox_size=(128,128), hitbox_type='rectangle'),
            #SpritestackAsset(type='building', name='shed', hitbox_size=(64,45), hitbox_type='rectangle'),
            #SpritestackAsset(type='building', name='toilet', hitbox_size=(45,45), hitbox_type='rectangle'),

            # FENCES
            #SpritestackAsset(type='fence', name='fence_1', hitbox_size=(32,10), hitbox_type='rectangle'),
            #SpritestackAsset(type='fence', name='fence_2', hitbox_size=(32,10), hitbox_type='rectangle'),
            #SpritestackAsset(type='fence', name='fence_3', hitbox_size=(32,10), hitbox_type='rectangle'),
            #SpritestackAsset(type='fence', name='fence_4', hitbox_size=(32,10), hitbox_type='rectangle'),
            #SpritestackAsset(type='fence', name='fence_5', hitbox_size=(32,10), hitbox_type='rectangle'),
            #SpritestackAsset(type='fence', name='fence_6', hitbox_size=(32,10), hitbox_type='rectangle'),
            #SpritestackAsset(type='fence', name='fence_7', hitbox_size=(10,10), hitbox_type='rectangle'),
            #SpritestackAsset(type='fence', name='fence_8', hitbox_size=(10,10), hitbox_type='rectangle'),
            #SpritestackAsset(type='fence', name='fence_9', hitbox_size=(10,10), hitbox_type='rectangle'),

            # WALLS
            #SpritestackAsset(type='wall', name='wall_1', hitbox_size=(32,20), hitbox_type='rectangle'),
            #SpritestackAsset(type='wall', name='wall_2', hitbox_size=(32,20), hitbox_type='rectangle'),
            #SpritestackAsset(type='wall', name='wall_3', hitbox_size=(32,20), hitbox_type='rectangle'),
            #SpritestackAsset(type='wall', name='wall_4', hitbox_size=(32,20), hitbox_type='rectangle'),
            #SpritestackAsset(type='wall', name='wall_5', hitbox_size=(32,20), hitbox_type='rectangle'),

            # WINDMILLS
            #SpritestackAsset(type='windmill', name='windmill_1', hitbox_size=(32,32), hitbox_type='rectangle'),

            # WELLS
            #SpritestackAsset(type='well', name='well_1', hitbox_size=(50,50), hitbox_type='circle'),

            # TREES
            #SpritestackAsset(type='tree', name='tree_1', hitbox_size=(20,20), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_2', hitbox_size=(20,20), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_3', hitbox_size=(20,20), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_4', hitbox_size=(20,20), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_5', hitbox_size=(20,20), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_6', hitbox_size=(20,20), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_7', hitbox_size=(32,32), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_8', hitbox_size=(20,20), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_9', hitbox_size=(32,32), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_trunk_1', hitbox_size=(25,25), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_trunk_2', hitbox_size=(25,25), hitbox_type='circle'),
            #SpritestackAsset(type='tree', name='tree_trunk_3', hitbox_size=(25,25), hitbox_type='circle'),

            # ROCKS
            #SpritestackAsset(type='rock', name='rock_1', hitbox_size=(32,32), hitbox_type='circle'),
            #SpritestackAsset(type='rock', name='rock_2', hitbox_size=(32,32), hitbox_type='circle'),
            #SpritestackAsset(type='rock', name='rock_3', hitbox_size=(32,32), hitbox_type='circle'),
            #SpritestackAsset(type='rock', name='rock_4', hitbox_size=(32,32), hitbox_type='circle'),
            #SpritestackAsset(type='rock', name='rock_5', hitbox_size=(32,32), hitbox_type='circle'),

            # CRATES
            #SpritestackAsset(type='crate', name='crate_1', hitbox_size=(32,20), hitbox_type='rectangle'),
            #SpritestackAsset(type='crate', name='crate_2', hitbox_size=(32,32), hitbox_type='rectangle'),

            # HAY BALES
            #SpritestackAsset(type='hay_bale', name='hay_bale_1', hitbox_size=(32,32), hitbox_type='rectangle'),
            #SpritestackAsset(type='hay_bale', name='hay_bale_2', hitbox_size=(32,32), hitbox_type='rectangle'),

            # BARRELS
            #SpritestackAsset(type='barrel', name='barrel_1', hitbox_size=(16,16), hitbox_type='circle'),
            #SpritestackAsset(type='barrel', name='barrel_2', hitbox_size=(16,16), hitbox_type='circle'),

            # WHEELBARROWS
            #SpritestackAsset(type='wheelbarrow', name='wheelbarrow_1', hitbox_size=(25,25), hitbox_type='rectangle'),

            # WATER TOWERS
            #SpritestackAsset(type='water_tower', name='water_tower_1', hitbox_size=(64,64), hitbox_type='rectangle'),

            # CAMPFIRES
            #SpritestackAsset(type='campfire', name='campfire_1', hitbox_size=(32,32), hitbox_type='circle'),

            # HOUSE_1 INTERIOR
            #SpritestackAsset(type='house_1_interior', name='wall_north', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='wall_east', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='wall_south', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='wall_west', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='table_1', hitbox_size=(30,50), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='chair_1', hitbox_size=(20,20), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='cabinet_1', hitbox_size=(20,20), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='shelf_1', hitbox_size=(20,20), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='bed_1', hitbox_size=(20,20), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='chest_1', hitbox_size=(20,20), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='chair_2', hitbox_size=(20,20), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='wardrobe_1', hitbox_size=(45,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='fireplace_front_1', hitbox_size=(45,5), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='fireplace_back_1', hitbox_size=(45,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='house_1_interior', name='cactus_1', hitbox_size=(20,20), scale=1, hitbox_type='rectangle'),

            # TENT_1
            #SpritestackAsset(type='tent', name='tent_1', hitbox_size=(80,80), scale=1, hitbox_type='rectangle'),

            # CLIFFS
            #SpritestackAsset(type='slope', name='slope_1', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='slope', name='slope_2', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='slope', name='slope_3', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='slope', name='slope_4', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='slope', name='slope_5', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='slope', name='slope_6', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='slope', name='slope_7', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='slope', name='slope_8', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),

            #SpritestackAsset(type='cliff', name='cliff_1', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='cliff', name='cliff_2', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='cliff', name='cliff_3', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),
            #SpritestackAsset(type='cliff', name='cliff_4', hitbox_size=(32,32), scale=1, hitbox_type='rectangle'),



            ### WOODEN HOUSE PARTS

            # front walls
            SpritestackAsset(type='wooden_house_parts', name='wall_simple_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='wooden_house_parts', name='wall_small_window_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='wooden_house_parts', name='wall_door_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),

            SpritestackAsset(type='wooden_house_parts', name='wall_simple_beams_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='wooden_house_parts', name='wall_small_window_beams_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='wooden_house_parts', name='wall_door_beams_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),

            SpritestackAsset(type='wooden_house_parts', name='wall_roof_left_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='wooden_house_parts', name='wall_roof_right_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='wooden_house_parts', name='wall_roof_double_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),

            # side walls
            SpritestackAsset(type='wooden_house_parts', name='wall_simple_64', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='wooden_house_parts', name='wall_small_window_64', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='wooden_house_parts', name='wall_door_64', hitbox_size=(64,64), hitbox_type='rectangle'),

            SpritestackAsset(type='wooden_house_parts', name='wall_roof_64', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='wooden_house_parts', name='wall_roof_double_64', hitbox_size=(64,64), hitbox_type='rectangle'),




            ### BRICK HOUSE PARTS

            # front walls
            SpritestackAsset(type='brick_house_parts', name='wall_simple_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_small_window_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_door_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),

            SpritestackAsset(type='brick_house_parts', name='wall_roof_left_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_roof_right_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_roof_double_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),

            # side walls
            SpritestackAsset(type='brick_house_parts', name='wall_simple_64', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_small_window_64', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_door_64', hitbox_size=(64,64), hitbox_type='rectangle'),

            SpritestackAsset(type='brick_house_parts', name='wall_roof_64', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_roof_double_64', hitbox_size=(64,64), hitbox_type='rectangle'),


            # SET THE RIGHT RENDER BOX SIZES !!!!!!!!!
            ### BUILDING DECOR
            SpritestackAsset(type='building_decor', name='flag_1', hitbox_size=(4,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='poster_1', hitbox_size=(22,1), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='poster_2', hitbox_size=(32,1), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='poster_stand', hitbox_size=(32,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='ladder', hitbox_size=(22,16), hitbox_offset=(0,-8), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='large_crate', hitbox_size=(64,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='medium_crate', hitbox_size=(32,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='blue_canopy', hitbox_size=(32,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='metal_bench', hitbox_size=(50,20), hitbox_offset=(0,-10), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='utility_pole_bottom', hitbox_size=(10,10), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='utility_pole_middle', hitbox_size=(10,10), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='utility_pole_top_single', hitbox_size=(32,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='utility_pole_top_double', hitbox_size=(32,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='utility_pole_top_triple', hitbox_size=(32,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='utility_pole_top_multiple', hitbox_size=(32,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='wires_straight', hitbox_size=(10,32), hitbox_type='rectangle'),

            ### BRICK HOUSE FLAT ROOF BLOCKS
            SpritestackAsset(type='brick_house_parts', name='wall_garage_door_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_roof_flat_full_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_roof_flat_middle_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_roof_flat_left_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_roof_flat_right_32', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_roof_flat_middle_64', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_roof_flat_64', hitbox_size=(64,64), hitbox_type='rectangle'),

            ### SCAFFOLDING
            SpritestackAsset(type='building_decor', name='scaffolding_1', hitbox_size=(64,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='scaffolding_2', hitbox_size=(64,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='scaffolding_3', hitbox_size=(64,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='scaffolding_4', hitbox_size=(64,32), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='scaffolding_5', hitbox_size=(64,32), hitbox_type='rectangle'),

            # DUMPSTER
            SpritestackAsset(type='building_decor', name='dumpster', hitbox_size=(64,40), hitbox_offset=(0,-10), hitbox_type='rectangle'),

            # WIRE FENCES
            SpritestackAsset(type='building_decor', name='wire_fence_right', hitbox_size=(32,4), hitbox_offset=(0,2), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='wire_fence_left', hitbox_size=(32,4), hitbox_offset=(0,2), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='wire_fence_middle', hitbox_size=(32,4), hitbox_offset=(0,2), hitbox_type='rectangle'),

            # VENDING MACHINES
            SpritestackAsset(type='building_decor', name='vending_machine_cola', hitbox_size=(32,24), hitbox_offset=(0,-5), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='vending_machine_kodak', hitbox_size=(32,16), hitbox_offset=(0,-8), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='vending_machine_pepsi', hitbox_size=(32,24), hitbox_offset=(0,-5), hitbox_type='rectangle'),

            # SHOP PIECES
            SpritestackAsset(type='brick_house_parts', name='wall_shop_window_barber', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_shop_door_barber', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_shop_window_butcher_front', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_shop_window_butcher_side', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='brick_house_parts', name='wall_shop_door_butcher', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle'),

            # FLOWER POTS
            SpritestackAsset(type='building_decor', name='flower_pot_1', hitbox_size=(16,16), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='flower_pot_2', hitbox_size=(16,16), hitbox_type='rectangle'),

            # SIDEWALK
            SpritestackAsset(type='texture', name='sidewalk_1', hitbox_size=(64,64), hitbox_type='rectangle'),

            # KERB
            SpritestackAsset(type='texture', name='kerb_1', hitbox_size=(64,8), hitbox_offset=(0,4), hitbox_type='rectangle'),

            # ROAD
            SpritestackAsset(type='texture', name='road_1', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='texture', name='road_2', hitbox_size=(64,64), hitbox_type='rectangle'),
            SpritestackAsset(type='texture', name='road_3', hitbox_size=(64,64), hitbox_type='rectangle'),

            # STONE TILES
            SpritestackAsset(type='texture', name='tiles_1', hitbox_size=(64,64), hitbox_type='rectangle'),

            # AC VENTS
            SpritestackAsset(type='building_decor', name='ac_vent_1', hitbox_size=(32,16), hitbox_offset=(0,-8), hitbox_type='rectangle'),

            # ROAD CORNER TILE
            SpritestackAsset(type='texture', name='road_4', hitbox_size=(64,64), hitbox_type='rectangle'),

            # DRAIN PIPE
            SpritestackAsset(type='building_decor', name='drain_top', hitbox_size=(32,10), hitbox_offset=(0,5), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='drain_intersection', hitbox_size=(32,10), hitbox_offset=(0,5), hitbox_type='rectangle'),
            SpritestackAsset(type='building_decor', name='drain_pipe', hitbox_size=(10,10), hitbox_offset=(0,5), hitbox_type='rectangle'),

            # CACTI
            SpritestackAsset(type='cactus', name='cactus_1', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_2', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_3', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_4', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_5', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_6', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_7', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_8', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_9', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_10', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_11', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='cactus', name='cactus_12', hitbox_size=(20,20), hitbox_offset=(0,0), hitbox_type='circle'),

            # RED ROCKS
            SpritestackAsset(type='rock', name='rock_red_1', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_red_2', hitbox_size=(40,40), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_red_3', hitbox_size=(60,60), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_red_4', hitbox_size=(60,60), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_red_5', hitbox_size=(60,60), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_red_6', hitbox_size=(50,50), hitbox_offset=(0,0), hitbox_type='circle'),
            SpritestackAsset(type='rock', name='rock_red_7', hitbox_size=(64,40), hitbox_offset=(0,0), hitbox_type='rectangle'),

            # NEW FENCE
            SpritestackAsset(type='fence', name='fence_long', hitbox_size=(64,8), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='fence', name='fence_pole', hitbox_size=(8,8), hitbox_offset=(0,0), hitbox_type='rectangle'),

            # DIRT ROAD
            SpritestackAsset(type='texture', name='dirt_road_straight', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='texture', name='dirt_road_turn', hitbox_size=(64,64), hitbox_offset=(0,0), hitbox_type='rectangle'),

            # HOTDOG STAND
            SpritestackAsset(type='hot_dog_stand', name='wagon', hitbox_size=(64,64), hitbox_offset=(0,0), hitbox_type='rectangle'),
            
            # TRASH CAN
            SpritestackAsset(type='trash_can', name='trash_can_1', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),

            # FIRE HYDRANT
            SpritestackAsset(type='fire_hydrant', name='fire_hydrant_1', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='circle'),

            # GRAVESTONES
            SpritestackAsset(type='grave', name='grave_1', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_2', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_3', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_4', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_5', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_6', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_7', hitbox_size=(64,64), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_8', hitbox_size=(64,64), hitbox_offset=(0,0), hitbox_type='rectangle'),

            # CHURCH FENCE
            SpritestackAsset(type='church', name='gate_post', hitbox_size=(32,32)),
            SpritestackAsset(type='church', name='fence_middle', hitbox_size=(32,32)),
            SpritestackAsset(type='church', name='fence_post', hitbox_size=(32,32)),
            SpritestackAsset(type='church', name='fence_corner', hitbox_size=(32,32)),
            SpritestackAsset(type='church', name='gate_back', hitbox_size=(32,32)),

            # GRASS
            SpritestackAsset(type='texture', name='grass_64', hitbox_size=(64,64)),

            ### TEST BLOCKS
            #SpritestackAsset(type='test_shapes', name='test_corner', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle', interactable=False),
            #SpritestackAsset(type='test_shapes', name='test_corner_roof', hitbox_size=(64,32), hitbox_offset=(0,-16), hitbox_type='rectangle', interactable=False),
            #SpritestackAsset(type='test_shapes', name='test_wall', hitbox_size=(64,64), hitbox_type='rectangle', interactable=False),
            #SpritestackAsset(type='test_shapes', name='test_roof', hitbox_size=(64,64), hitbox_type='rectangle', interactable=False),
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
                min_tile_size=32,
                max_tile_size=32,
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
        self.particle_system_assets = [
            particle_presets.flame_front,
            particle_presets.flame_fireplace,
            particle_presets.fog_cloud,
        ]


        """ VEHICLE ASSETS """
        self.vehicle_assets = [

            # MINIVAN
            Vehicle(
                parts_positions_rotations=[
                    (SpritestackAsset(type='minivan', name='back', hitbox_size=(64,64)), [-32,0,0], 0),
                    (SpritestackAsset(type='minivan', name='front', hitbox_size=(64,64)), [32,0,0], 0),
                ],
                hitbox_size=(128, 64)
            ),

            # DELIVERY TRUCK
            Vehicle(
                parts_positions_rotations=[
                    (SpritestackAsset(type='delivery_truck', name='front', hitbox_size=(64,64)), [64,0,0], 0),
                    (SpritestackAsset(type='delivery_truck', name='middle', hitbox_size=(64,64)), [0,0,0], 0),
                    (SpritestackAsset(type='delivery_truck', name='back', hitbox_size=(64,64)), [-64,0,0], 0),
                ],
                hitbox_size=(192, 64),
            ),

        ]


        """ COMPOSITE OBJECTS """
        # INITIALIZING PART ASSETS TO AVOID CREATING DUPLICATE OBJECTS IN MEMORY

        # BUS STOP
        bus_stop_bottom_left = SpritestackAsset(type='bus_stop', name='bottom_left', hitbox_size=(64,64))
        bus_stop_bottom_right = SpritestackAsset(type='bus_stop', name='bottom_right', hitbox_size=(64,64))
        bus_stop_roof_left = SpritestackAsset(type='bus_stop', name='roof_left', hitbox_size=(64,64))
        bus_stop_roof_right = SpritestackAsset(type='bus_stop', name='roof_right', hitbox_size=(64,64))

        # LARGE WATER TOWER
        water_tower_bottom = SpritestackAsset(type='water_tower_large', name='bottom', hitbox_size=(64,64))
        water_tower_middle = SpritestackAsset(type='water_tower_large', name='middle', hitbox_size=(64,64))
        water_tower_top = SpritestackAsset(type='water_tower_large', name='top', hitbox_size=(64,64))
        water_tower_roof = SpritestackAsset(type='water_tower_large', name='roof', hitbox_size=(64,64))

        # BEANZ BILLBOARD
        beanz_billboard_pillar_bottom = SpritestackAsset(type='billboard_beans', name='pillar_bottom', hitbox_size=(64,64))
        beanz_billboard_pillar_top = SpritestackAsset(type='billboard_beans', name='pillar_top', hitbox_size=(64,64))
        beanz_billboard_sign_left = SpritestackAsset(type='billboard_beans', name='sign_left', hitbox_size=(64,64))
        beanz_billboard_sign_middle = SpritestackAsset(type='billboard_beans', name='sign_middle', hitbox_size=(64,64))
        beanz_billboard_sign_right = SpritestackAsset(type='billboard_beans', name='sign_right', hitbox_size=(64,64))

        # DINER
        diner_wall_corner = SpritestackAsset(type='diner', name='wall_corner', hitbox_size=(64,64))
        diner_wall_window = SpritestackAsset(type='diner', name='wall_window', hitbox_size=(64,64))
        diner_wall_front_entrance = SpritestackAsset(type='diner', name='wall_front_entrance', hitbox_size=(64,64))
        diner_wall_back = SpritestackAsset(type='diner', name='wall_back', hitbox_size=(64,64))
        diner_roof_corner = SpritestackAsset(type='diner', name='roof_corner', hitbox_size=(64,64))
        diner_roof_side = SpritestackAsset(type='diner', name='roof_side', hitbox_size=(64,64))
        diner_roof_middle = SpritestackAsset(type='diner', name='roof_middle', hitbox_size=(64,64))
        diner_roof_sign_left = SpritestackAsset(type='diner', name='roof_sign_left', hitbox_size=(64,64))
        diner_roof_sign_middle = SpritestackAsset(type='diner', name='roof_sign_middle', hitbox_size=(64,64))
        diner_roof_sign_right = SpritestackAsset(type='diner', name='roof_sign_right', hitbox_size=(64,64))

        # GAS STATION
        gas_station_wall_corner_door = SpritestackAsset(type='gas_station', name='wall_corner_door', hitbox_size=(64,64))
        gas_station_wall_corner_window = SpritestackAsset(type='gas_station', name='wall_corner_window', hitbox_size=(64,64))
        gas_station_wall_side = SpritestackAsset(type='gas_station', name='wall_side', hitbox_size=(64,64))
        gas_station_wall_corner = SpritestackAsset(type='gas_station', name='wall_corner', hitbox_size=(64,64))
        gas_station_pump = SpritestackAsset(type='gas_station', name='pump', hitbox_size=(64,64))
        gas_station_pillar = SpritestackAsset(type='gas_station', name='pillar', hitbox_size=(64,64))
        gas_station_roof_corner = SpritestackAsset(type='gas_station', name='roof_corner', hitbox_size=(64,64))
        gas_station_roof_side = SpritestackAsset(type='gas_station', name='roof_side', hitbox_size=(64,64))
        gas_station_roof_middle = SpritestackAsset(type='gas_station', name='roof_middle', hitbox_size=(64,64))
        gas_station_sign = SpritestackAsset(type='gas_station', name='sign', hitbox_size=(64,64))

        # MOTEL
        motel_wall_door = SpritestackAsset(type='motel', name='wall_door', hitbox_size=(64,64))
        motel_wall_window = SpritestackAsset(type='motel', name='wall_window', hitbox_size=(64,64))
        motel_wall_plain = SpritestackAsset(type='motel', name='wall_plain', hitbox_size=(64,64))
        motel_stairs_top = SpritestackAsset(type='motel', name='stairs_top', hitbox_size=(64,64))
        motel_stairs_bottom = SpritestackAsset(type='motel', name='stairs_bottom', hitbox_size=(64,64))
        motel_balcony_bottom_stairs = SpritestackAsset(type='motel', name='balcony_bottom_stairs', hitbox_size=(64,64))
        motel_balcony_middle_stairs = SpritestackAsset(type='motel', name='balcony_middle_stairs', hitbox_size=(64,64))
        motel_balcony_top_stairs = SpritestackAsset(type='motel', name='balcony_top_stairs', hitbox_size=(64,64))
        motel_balcony_bottom_corner = SpritestackAsset(type='motel', name='balcony_bottom_corner', hitbox_size=(64,64))
        motel_balcony_middle_corner = SpritestackAsset(type='motel', name='balcony_middle_corner', hitbox_size=(64,64))
        motel_balcony_top_corner = SpritestackAsset(type='motel', name='balcony_top_corner', hitbox_size=(64,64))
        motel_balcony_bottom_pillar = SpritestackAsset(type='motel', name='balcony_bottom_pillar', hitbox_size=(64,64))
        motel_balcony_middle_pillar = SpritestackAsset(type='motel', name='balcony_middle_pillar', hitbox_size=(64,64))
        motel_balcony_top_pillar = SpritestackAsset(type='motel', name='balcony_top_pillar', hitbox_size=(64,64))
        motel_balcony_bottom_no_pillar = SpritestackAsset(type='motel', name='balcony_bottom_no_pillar', hitbox_size=(64,64))
        motel_balcony_middle_no_pillar = SpritestackAsset(type='motel', name='balcony_middle_no_pillar', hitbox_size=(64,64))
        motel_balcony_top_no_pillar = SpritestackAsset(type='motel', name='balcony_top_no_pillar', hitbox_size=(64,64))
        motel_wall_roof_corner = SpritestackAsset(type='motel', name='wall_roof_corner', hitbox_size=(64,64))
        motel_wall_roof_side = SpritestackAsset(type='motel', name='wall_roof_side', hitbox_size=(64,64))
        motel_wall_roof_middle = SpritestackAsset(type='motel', name='wall_roof_middle', hitbox_size=(64,64))
        motel_wall_reception = SpritestackAsset(type='motel', name='wall_reception', hitbox_size=(64,64))
        motel_roof_reception = SpritestackAsset(type='motel', name='wall_roof_reception', hitbox_size=(64,64))
        motel_sign = SpritestackAsset(type='motel', name='sign', hitbox_size=(64,64))

        # CHURCH
        church_wall_front_bottom_left = SpritestackAsset(type='church', name='wall_front_bottom_left', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_front_bottom_middle = SpritestackAsset(type='church', name='wall_front_bottom_middle', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_front_bottom_right = SpritestackAsset(type='church', name='wall_front_bottom_right', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_entrance = SpritestackAsset(type='church', name='wall_entrance', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_window = SpritestackAsset(type='church', name='wall_window', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_back_bottom_left = SpritestackAsset(type='church', name='wall_back_bottom_left', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_back_bottom_right = SpritestackAsset(type='church', name='wall_back_bottom_right', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_back_bottom_middle = SpritestackAsset(type='church', name='wall_back_bottom_middle', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_front_top_left = SpritestackAsset(type='church', name='wall_front_top_left', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_front_top_middle = SpritestackAsset(type='church', name='wall_front_top_middle', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_front_top_right = SpritestackAsset(type='church', name='wall_front_top_right', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_roof_side_left = SpritestackAsset(type='church', name='roof_side_left', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_roof_side_right = SpritestackAsset(type='church', name='roof_side_right', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_tower_bottom = SpritestackAsset(type='church', name='wall_tower_bottom', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_tower_top = SpritestackAsset(type='church', name='wall_tower_top', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_roof_middle = SpritestackAsset(type='church', name='roof_middle', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_back_top_left = SpritestackAsset(type='church', name='wall_back_top_left', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_back_top_right = SpritestackAsset(type='church', name='wall_back_top_right', hitbox_size=(64,64), hitbox_offset=(0,0))
        church_wall_back_top_middle = SpritestackAsset(type='church', name='wall_back_top_middle', hitbox_size=(64,64), hitbox_offset=(0,0))

        # ROAD
        road_edge = SpritestackAsset(type='texture', name='road_1', hitbox_size=(64,64))
        road_centre = SpritestackAsset(type='texture', name='road_2', hitbox_size=(64,64))
        road_midway = SpritestackAsset(type='texture', name='road_3', hitbox_size=(64,64))

        self.composite_object_assets = [

            # NARROW TWO WAY ROAD
            CompositeObject(
                parts_positions_rotations=[
                    (road_edge, [-128,-64,0], 0),
                    (road_centre, [-128,0,0], 0),
                    (road_edge, [-128,64,0], 180),

                    (road_edge, [-64,-64,0], 0),
                    (road_centre, [0-64,0,0], 0),
                    (road_edge, [-64,64,0], 180),

                    (road_edge, [0,-64,0], 0),
                    (road_centre, [0,0,0], 0),
                    (road_edge, [0,64,0], 180),

                    (road_edge, [64,-64,0], 0),
                    (road_centre, [64,0,0], 0),
                    (road_edge, [64,64,0], 180),

                    (road_edge, [128,-64,0], 0),
                    (road_centre, [128,0,0], 0),
                    (road_edge, [128,64,0], 180),
                ],
                type='texture',
                hitbox_size=(320, 192),
            ),

            # CHURCH
            CompositeObject(
                parts_positions_rotations=[
                    (church_wall_entrance, [0,128,0*2], 0),
                    (church_wall_front_bottom_left, [-64,64,0*2], 0),
                    (church_wall_front_bottom_middle, [0,64,0*2], 0),
                    (church_wall_front_bottom_right, [64,64,0*2], 0),
                    (church_wall_front_top_left, [-64,64,96*2], 0),
                    (church_wall_front_top_middle, [0,64,96*2], 0),
                    (church_wall_front_top_right, [64,64,96*2], 0),
                    (church_wall_window, [-64,0,0*2], -90),
                    (church_wall_window, [-64,-64,0*2], -90),
                    (church_wall_window, [-64,-128,0*2], -90),
                    (church_roof_side_left, [-64,0,96*2], 0),
                    (church_roof_side_left, [-64,-64,96*2], 0),
                    (church_roof_side_left, [-64,-128,96*2], 0),
                    (church_wall_window, [64,0,0*2], 90),
                    (church_wall_window, [64,-64,0*2], 90),
                    (church_wall_window, [64,-128,0*2], 90),
                    (church_roof_side_right, [64,0,96*2], 0),
                    (church_roof_side_right, [64,-64,96*2], 0),
                    (church_roof_side_right, [64,-128,96*2], 0),
                    (church_wall_back_bottom_left, [-64,-192,0*2], 180),
                    (church_wall_back_bottom_middle, [0,-192,0*2], 180),
                    (church_wall_back_bottom_right, [64,-192,0*2], 180),
                    (church_wall_back_top_left, [-64,-192,96*2], 180),
                    (church_wall_back_top_middle, [0,-192,96*2], 180),
                    (church_wall_back_top_right, [64,-192,96*2], 180),
                    (church_roof_middle, [0,-64,160*2], 0),
                    (church_roof_middle, [0,-128,160*2], 0),
                    (church_wall_tower_bottom, [0,0,160*2], 0),
                    (church_wall_tower_top, [0,0,208*2], 0),

                ],
                hitbox_size=(196, 320),
            ),

            # BUS STOP
            CompositeObject(
                parts_positions_rotations=[
                    (bus_stop_bottom_left, [-32,0,0*2], 0),
                    (bus_stop_bottom_right, [32,0,0*2], 0),
                    (bus_stop_roof_left, [-32,0,64*2], 0),
                    (bus_stop_roof_right, [32,0,64*2], 0),
                ],
                hitbox_size=(128, 64),
            ),


            # LARGE WATER TOWER
            CompositeObject(
                parts_positions_rotations=[
                    (water_tower_bottom, [-32,32,0*2], 0),
                    (water_tower_bottom, [-32,-32,0*2], -90),
                    (water_tower_bottom, [32,-32,0*2], -180),
                    (water_tower_bottom, [32,32,0*2], -270),
                    (water_tower_middle, [-32,32,128*2], 0),
                    (water_tower_middle, [-32,-32,128*2], -90),
                    (water_tower_middle, [32,-32,128*2], -180),
                    (water_tower_middle, [32,32,128*2], -270),
                    (water_tower_top, [-32,32,256*2], 0),
                    (water_tower_top, [-32,-32,256*2], -90),
                    (water_tower_top, [32,-32,256*2], -180),
                    (water_tower_top, [32,32,256*2], -270),
                    (water_tower_roof, [-32,32,384*2], 0),
                    (water_tower_roof, [-32,-32,384*2], -90),
                    (water_tower_roof, [32,-32,384*2], -180),
                    (water_tower_roof, [32,32,384*2], -270),
                ],
                hitbox_size=(128, 128),
            ), 


            # BEANZ BILLBOARD
            CompositeObject(
                parts_positions_rotations=[
                    (beanz_billboard_pillar_bottom, [0,0,0*2], 0),
                    (beanz_billboard_pillar_top, [0,0,64*2], 0),
                    (beanz_billboard_sign_left, [-64,0,128*2], 0),
                    (beanz_billboard_sign_middle, [0,0,128*2], 0),
                    (beanz_billboard_sign_right, [64,0,128*2], 0),
                ],
                hitbox_size=(32, 32),
            ),


            # DINER
            CompositeObject(
                parts_positions_rotations=[
                    (diner_wall_corner, [-128,64,0*2], 0),
                    (diner_wall_window, [-64,64,0*2], 0),
                    (diner_wall_front_entrance, [0,64,0*2], 0),
                    (diner_wall_window, [64,64,0*2], 0),
                    (diner_wall_corner, [128,64,0*2], 90),
                    (diner_wall_window, [128,0,0*2], 90),
                    (diner_wall_corner, [128,-64,0*2], 180),
                    (diner_wall_back, [64,-64,0*2], 180),
                    (diner_wall_back, [0,-64,0*2], 180),
                    (diner_wall_back, [-64,-64,0*2], 180),
                    (diner_wall_corner, [-128,-64,0*2], 270),
                    (diner_wall_window, [-128,0,0*2], 270),
                    (diner_roof_corner, [-128,64,64*2], 0),
                    (diner_roof_sign_left, [-64,64,64*2], 0),
                    (diner_roof_sign_middle, [0,64,64*2], 0),
                    (diner_roof_sign_right, [64,64,64*2], 0),
                    (diner_roof_corner, [128,64,64*2], 90),
                    (diner_roof_side, [128,0,64*2], 90),
                    (diner_roof_corner, [128,-64,64*2], 180),
                    (diner_roof_side, [64,-64,64*2], 180),
                    (diner_roof_side, [0,-64,64*2], 180),
                    (diner_roof_side, [-64,-64,64*2], 180),
                    (diner_roof_corner, [-128,-64,64*2], 270),
                    (diner_roof_side, [-128,0,64*2], 270),
                    (diner_roof_middle, [-64,0,64*2], 0),
                    (diner_roof_middle, [0,0,64*2], 0),
                    (diner_roof_middle, [64,0,64*2], 0),
                ],
                hitbox_size=(320, 192),
            ),


            # GAS STATION
            CompositeObject(
                parts_positions_rotations=[
                    (gas_station_wall_corner_door, [64,64,0*2], 0),
                    (gas_station_wall_corner_window, [128,64,0*2], 0),
                    (gas_station_wall_side, [128,0,0*2], 180),
                    (gas_station_wall_corner, [128,-64,0*2], 180),
                    (gas_station_wall_corner, [64,-64,0*2], -90),
                    (gas_station_wall_side, [64,0,0*2], 0),
                    (gas_station_pump, [-128,64,0*2], 0),
                    (gas_station_pillar, [-128,0,0*2], 0),
                    (gas_station_pump, [-128,-64,0*2], 0),
                    (gas_station_roof_corner, [-128,64,64*2], 0),
                    (gas_station_roof_side, [-64,64,64*2], 0),
                    (gas_station_roof_side, [0,64,64*2], 0),
                    (gas_station_roof_side, [64,64,64*2], 0),
                    (gas_station_roof_corner, [128,64,64*2], 90),
                    (gas_station_roof_side, [128,0,64*2], 90),
                    (gas_station_roof_corner, [128,-64,64*2], 180),
                    (gas_station_roof_side, [64,-64,64*2], 180),
                    (gas_station_roof_side, [0,-64,64*2], 180),
                    (gas_station_roof_side, [-64,-64,64*2], 180),
                    (gas_station_roof_corner, [-128,-64,64*2], 270),
                    (gas_station_roof_side, [-128,0,64*2], 270),
                    (gas_station_roof_middle, [-64,0,64*2], 0),
                    (gas_station_roof_middle, [0,0,64*2], 0),
                    (gas_station_roof_middle, [64,0,64*2], 0),
                    (gas_station_sign, [-64,96,80*2], 0),
                ],
                hitbox_size=(320, 192),
            ),


            # MOTEL
            CompositeObject(
                parts_positions_rotations=[
                    (motel_wall_door, [-160,64,0*2], 0),
                    (motel_wall_door, [-160,64,80*2], 0),
                    (motel_wall_roof_corner, [-160,64,160*2], 0),
                    (motel_wall_window, [-96,64,0*2], 0),
                    (motel_wall_window, [-96,64,80*2], 0),
                    (motel_wall_roof_side, [-96,64,160*2], 0),
                    (motel_wall_plain, [-32,64,0*2], 0),
                    (motel_wall_plain, [-32,64,80*2], 0),
                    (motel_wall_roof_side, [-32,64,160*2], 0),
                    (motel_wall_door, [32,64,0*2], 0),
                    (motel_wall_door, [32,64,80*2], 0),
                    (motel_wall_roof_side, [32,64,160*2], 0),
                    (motel_wall_window, [96,64,0*2], 0),
                    (motel_wall_window, [96,64,80*2], 0),
                    (motel_wall_roof_side, [96,64,160*2], 0),
                    (motel_wall_plain, [160,64,0*2], 0),
                    (motel_wall_plain, [160,64,80*2], 0),
                    (motel_wall_roof_side, [160,64,160*2], 0),
                    (motel_stairs_top, [-224,0,0*2], 0),
                    (motel_stairs_bottom, [-224,-64,0*2], 0),
                    (motel_balcony_bottom_stairs, [-224,64,0*2], 0),
                    (motel_balcony_middle_stairs, [-224,64,80*2], 0),
                    (motel_balcony_top_stairs, [-224,64,160*2], 0),
                    (motel_balcony_bottom_corner, [-224,128,0*2], 0),
                    (motel_balcony_middle_corner, [-224,128,80*2], 0),
                    (motel_balcony_top_corner, [-224,128,160*2], 0),
                    (motel_balcony_bottom_no_pillar, [-160,128,0*2], 0),
                    (motel_balcony_middle_no_pillar, [-160,128,80*2], 0),
                    (motel_balcony_top_no_pillar, [-160,128,160*2], 0),
                    (motel_balcony_bottom_no_pillar, [-96,128,0*2], 0),
                    (motel_balcony_middle_no_pillar, [-96,128,80*2], 0),
                    (motel_balcony_top_no_pillar, [-96,128,160*2], 0),
                    (motel_balcony_bottom_pillar, [-32,128,0*2], 0),
                    (motel_balcony_middle_pillar, [-32,128,80*2], 0),
                    (motel_balcony_top_pillar, [-32,128,160*2], 0),
                    (motel_balcony_bottom_no_pillar, [32,128,0*2], 0),
                    (motel_balcony_middle_no_pillar, [32,128,80*2], 0),
                    (motel_balcony_top_no_pillar, [32,128,160*2], 0),
                    (motel_balcony_bottom_no_pillar, [96,128,0*2], 0),
                    (motel_balcony_middle_no_pillar, [96,128,80*2], 0),
                    (motel_balcony_top_no_pillar, [96,128,160*2], 0),
                    (motel_balcony_bottom_pillar, [160,128,0*2], 0),
                    (motel_balcony_middle_pillar, [160,128,80*2], 0),
                    (motel_balcony_top_pillar, [160,128,160*2], 0),
                    (motel_wall_plain, [-160,0,0*2], -90),
                    (motel_wall_plain, [-160,0,80*2], -90),
                    (motel_wall_roof_side, [-160,0,160*2], -90),
                    (motel_wall_plain, [-160,-64,0*2], -90),
                    (motel_wall_plain, [-160,-64,80*2], -90),
                    (motel_wall_roof_corner, [-160,-64,160*2], -90),
                    (motel_wall_window, [-96,-64,0*2], 180),
                    (motel_wall_window, [-96,-64,80*2], 180),
                    (motel_wall_roof_side, [-96,-64,160*2], 180),
                    (motel_wall_window, [-32,-64,0*2], 180),
                    (motel_wall_window, [-32,-64,80*2], 180),
                    (motel_wall_roof_side, [-32,-64,160*2], 180),
                    (motel_wall_plain, [32,-64,0*2], 180),
                    (motel_wall_plain, [32,-64,80*2], 180),
                    (motel_wall_roof_side, [32,-64,160*2], 180),
                    (motel_wall_window, [96,-64,0*2], 180),
                    (motel_wall_window, [96,-64,80*2], 180),
                    (motel_wall_roof_side, [96,-64,160*2], 180),
                    (motel_wall_window, [160,-64,0*2], 180),
                    (motel_wall_window, [160,-64,80*2], 180),
                    (motel_wall_roof_side, [160,-64,160*2], 180),
                    (motel_wall_plain, [224,-64,0*2], 180),
                    (motel_wall_plain, [224,-64,80*2], 180),
                    (motel_wall_roof_corner, [224,-64,160*2], 180),
                    (motel_wall_plain, [224,0,0*2], 90),
                    (motel_wall_plain, [224,0,80*2], 90),
                    (motel_wall_roof_side, [224,0,160*2], 90),
                    (motel_wall_plain, [224,64,0*2], 90),
                    (motel_wall_plain, [224,64,80*2], 90),
                    (motel_wall_roof_corner, [224,64,160*2], 90),
                    (motel_wall_reception, [224,128,0*2], 0),
                    (motel_wall_plain, [224,128,80*2], 0),
                    (motel_roof_reception, [224,128,160*2], 0),
                    (motel_wall_roof_middle, [-96,0,160*2], 0),
                    (motel_wall_roof_middle, [-32,0,160*2], 0),
                    (motel_wall_roof_middle, [32,0,160*2], 0),
                    (motel_wall_roof_middle, [96,0,160*2], 0),
                    (motel_wall_roof_middle, [160,0,160*2], 0),
                    (motel_sign, [224,160,80*2], 0),
                ],
                hitbox_size=(512, 256),
            ),

        ]




        """ LEVELS """
        # OUTDOORS LEVEL
        self.outdoors_level = Level(
            game=self,
            name='outdoors_level',
            map_size=(5000, 5000),
            #background='assets/texture/grass_64/sprite_stacks/stack_0.png',
            #fill_colour=(105, 66, 56)
            background='assets/texture/cracked_desert/sprite_stacks/stack_0.png',
            fill_colour=(168, 78, 50)
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
