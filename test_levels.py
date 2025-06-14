import pygame

import os


from graphics.plants import PlantSystem
from graphics.grass import GrassSystem
from graphics.sprite_stacks import SpritestackAsset

from objects.generic import CompositeObject, Vehicle

from world_builder.level_editor import Level

from presets import particle_presets

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()


class Game:
    def __init__(self):
        
        """ DISPLAY SETTINGS """
        scale = 0.75 #0.6 #0.5 # Percentage of max screen
        ratio = 16/9 #4/3 # WIDTH / HEIGHT ratio    ### INTERESTING OBSERVATION: A HORIZONTALLY STRETCHED PICTURE SEEMS TO HAVE MORE DEPTH

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
            SpritestackAsset(type='grave', name='grave_9', hitbox_size=(64,64), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_10', hitbox_size=(64,64), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_11', hitbox_size=(64,64), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_12', hitbox_size=(64,64), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_fence_side', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_fence_corner', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),
            SpritestackAsset(type='grave', name='grave_fence_gate', hitbox_size=(32,32), hitbox_offset=(0,0), hitbox_type='rectangle'),

            # GRASS
            SpritestackAsset(type='texture', name='grass_64', hitbox_size=(64,64)),

            # BEACH BED
            SpritestackAsset(type='pool', name='beach_bed', hitbox_size=(32,64)),

            # UMBRELLA
            SpritestackAsset(type='pool', name='umbrella', hitbox_size=(48,48), hitbox_type='circle'),

            # PICNIC TABLE
            SpritestackAsset(type='pool', name='picnic_table', hitbox_size=(48,64)),

            # POTTED MOTEL PLANT
            SpritestackAsset(type='motel', name='plant', hitbox_size=(32,32)),

            ### TEST BLOCKS
            SpritestackAsset(type='test_shapes', name='test_block_32', hitbox_size=(32,32)),
            SpritestackAsset(type='test_shapes', name='test_block_64', hitbox_size=(64,64)),
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

        # POOL
        pool_side = SpritestackAsset(type='pool', name='pool_side', hitbox_size=(64,64))
        pool_side_ladder = SpritestackAsset(type='pool', name='pool_side_ladder', hitbox_size=(64,64))
        pool_corner = SpritestackAsset(type='pool', name='pool_corner', hitbox_size=(64,64))
        pool_bottom = SpritestackAsset(type='pool', name='pool_bottom', hitbox_size=(64,64))
        pool_surrounding_tile = SpritestackAsset(type='pool', name='pool_surrounding_tile', hitbox_size=(64,64))
        pool_lounge_tile = SpritestackAsset(type='pool', name='pool_lounge_tile', hitbox_size=(64,64))

        # UTILITY POLE

        # SpritestackAsset(type='building_decor', name='utility_pole_top_single', hitbox_size=(32,32), hitbox_type='rectangle'),
        # SpritestackAsset(type='building_decor', name='utility_pole_top_double', hitbox_size=(32,32), hitbox_type='rectangle'),
        # SpritestackAsset(type='building_decor', name='utility_pole_top_triple', hitbox_size=(32,32), hitbox_type='rectangle'),
            
        # BUS STOP


        # LARGE WATER TOWER
        water_tower_bottom = SpritestackAsset(type='water_tower_large', name='bottom', hitbox_size=(64,64))
        water_tower_middle = SpritestackAsset(type='water_tower_large', name='middle', hitbox_size=(64,64))
        water_tower_top = SpritestackAsset(type='water_tower_large', name='top', hitbox_size=(64,64))
        water_tower_roof = SpritestackAsset(type='water_tower_large', name='roof', hitbox_size=(64,64))

        # BEANZ BILLBOARD


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

        # MOTEL FENCE
        motel_fence_side = SpritestackAsset(type='motel', name='fence_side', hitbox_size=(32,32))
        motel_fence_entrance_bottom = SpritestackAsset(type='motel', name='fence_entrance_bottom',  hitbox_size=(32,32))
        motel_fence_entrance_top = SpritestackAsset(type='motel', name='fence_entrance_top',  hitbox_size=(32,32))
        motel_fence_corner = SpritestackAsset(type='motel', name='fence_corner',  hitbox_size=(32,32))

        # CHURCH BUILDING
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

        # CHURCH FENCE
        church_gate_post = SpritestackAsset(type='church', name='gate_post', hitbox_size=(32,32))
        church_fence_middle = SpritestackAsset(type='church', name='fence_middle', hitbox_size=(32,32))
        church_fence_post = SpritestackAsset(type='church', name='fence_post', hitbox_size=(32,32))
        church_fence_corner = SpritestackAsset(type='church', name='fence_corner', hitbox_size=(32,32))
        church_gate_back = SpritestackAsset(type='church', name='gate_back', hitbox_size=(32,32))

        # CHURCH PATH TILES
        church_entrance_path_tile = SpritestackAsset(type='church', name='entrance_path_tile', hitbox_size=(64,64))

        # ROAD




        self.composite_object_assets = [

            # MOTEL FENCE PARTS
            CompositeObject(
                parts_positions_rotations=[
                    (motel_fence_entrance_bottom, [-48,0,0], 180),
                    (motel_fence_side, [-16,0,0], 0),
                    (motel_fence_side, [16,0,0], 0),
                    (motel_fence_side, [48,0,0], 0),
                ],
                hitbox_size=(128, 32),
            ),
            CompositeObject(
                parts_positions_rotations=[
                    (motel_fence_entrance_top, [-16,0,0], 0),
                    (motel_fence_entrance_top, [16,0,0], 180),
                ],
                hitbox_size=(64, 32),
            ),
            CompositeObject(
                parts_positions_rotations=[
                    (motel_fence_side, [-48,0,0], 0),
                    (motel_fence_side, [-16,0,0], 0),
                    (motel_fence_side, [16,0,0], 0),
                    (motel_fence_side, [48,0,0], 0),
                ],
                hitbox_size=(128, 32),
            ),
            CompositeObject(
                parts_positions_rotations=[                    
                    (motel_fence_side, [-48,0,0], 0),
                    (motel_fence_side, [-16,0,0], 0),
                    (motel_fence_side, [16,0,0], 0),
                    (motel_fence_entrance_bottom, [48,0,0], 0),
                ],
                hitbox_size=(128, 32),
            ),
            CompositeObject(
                parts_positions_rotations=[
                    (motel_fence_corner, [-64,0,0], 0),
                    (motel_fence_side, [-32,0,0], 0),
                    (motel_fence_side, [0,0,0], 0),
                    (motel_fence_side, [32,0,0], 0),
                    (motel_fence_side, [64,0,0], 0),
                ],
                hitbox_size=(160, 32),
            ),
            CompositeObject(
                parts_positions_rotations=[
                    (motel_fence_side, [-64,0,0], 0),
                    (motel_fence_side, [-32,0,0], 0),
                    (motel_fence_side, [0,0,0], 0),
                    (motel_fence_side, [32,0,0], 0),
                    (motel_fence_corner, [64,0,0], 90),
                ],
                hitbox_size=(160, 32),
            ),
            CompositeObject(
                parts_positions_rotations=[
                    (motel_fence_side, [-16,0,0], 0),
                    (motel_fence_side, [16,0,0], 0),
                ],
                hitbox_size=(64, 32),
            ),


            # POOL
            CompositeObject(
                parts_positions_rotations=[
                    (pool_corner, [-128,64,-32*2], 0),
                    (pool_side, [-64,64,-32*2], 0),
                    (pool_side, [0,64,-32*2], 0),
                    (pool_side, [64,64,-32*2], 0),
                    (pool_corner, [128,64,-32*2], 90),

                    (pool_corner, [-128,-64,-32*2], -90),
                    (pool_side_ladder, [-64,-64,-32*2], 180),
                    (pool_side, [0,-64,-32*2], 180),
                    (pool_side, [64,-64,-32*2], 180),
                    (pool_corner, [128,-64,-32*2], 180),

                    (pool_side, [-128,0,-32*2], -90),
                    (pool_side, [128,0,-32*2], 90),

                    (pool_bottom, [-64,0,-32*2], 0),
                    (pool_bottom, [0,0,-32*2], 0),
                    (pool_bottom, [64,0,-32*2], 0),
                ],
                hitbox_size=(320, 192),
                type='texture',
            ),

            # POOL SIDE TILES
            CompositeObject(
                parts_positions_rotations=[
                    (pool_surrounding_tile, [-128,0,0], 90),
                    (pool_surrounding_tile, [-64,0,0], 0),
                    (pool_surrounding_tile, [0,0,0], -90),
                    (pool_surrounding_tile, [64,0,0], 180),
                    (pool_surrounding_tile, [128,0,0], 90),
                ],
                hitbox_size=(320, 64),
                type='texture',
            ),

            # POOL LOUNGE AREA
            CompositeObject(
                parts_positions_rotations=[
                    (pool_surrounding_tile, [-192,0,0], 0),
                    (pool_lounge_tile, [-128,0,0], 0),
                    (pool_lounge_tile, [-64,0,0], 0),
                    (pool_lounge_tile, [0,0,0], 0),
                    (pool_lounge_tile, [64,0,0], 0),
                    (pool_lounge_tile, [128,0,0], 0),
                    (pool_surrounding_tile, [192,0,0], 0),
                ],
                hitbox_size=(448, 64),
                type='texture',
            ),

        





            # CHURCH WALLS
            CompositeObject(
                parts_positions_rotations=[
                    (church_wall_front_bottom_left, [-64,128,0], 0),
                    (church_wall_front_bottom_middle, [0,128,0], 0),
                    (church_wall_front_bottom_right, [64,128,0], 0),
                    (church_wall_window, [-64,-64,0], -90),
                    (church_wall_window, [-64,0,0], -90),
                    (church_wall_window, [-64,64,0], -90),
                    (church_wall_window, [64,-64,0], 90),
                    (church_wall_window, [64,0,0], 90),
                    (church_wall_window, [64,64,0], 90),
                    (church_wall_back_bottom_left, [-64,-128,0], 180),
                    (church_wall_back_bottom_middle, [0,-128,0], 180),
                    (church_wall_back_bottom_right, [64,-128,0], 180),
                ],
                hitbox_size=(196, 320),
                hitbox_offset=(0, -32)
            ),

            # CHURCH ROOF
            CompositeObject(
                parts_positions_rotations=[
                    (church_wall_front_top_left, [-64,128,0], 0),
                    (church_wall_front_top_middle, [0,128,0], 0),
                    (church_wall_front_top_right, [64,128,0], 0),
                    (church_wall_back_top_left, [-64,-128,0], 180),
                    (church_wall_back_top_middle, [0,-128,0], 180),
                    (church_wall_back_top_right, [64,-128,0], 180),
                    (church_roof_side_left, [-64,-64,0], 0),
                    (church_roof_side_left, [-64,0,0], 0),
                    (church_roof_side_left, [-64,64,0], 0),
                    (church_roof_side_right, [64,-64,0], 0),
                    (church_roof_side_right, [64,0,0], 0),
                    (church_roof_side_right, [64,64,0], 0),
                    (church_roof_middle, [0,0,64*2], 0),
                    (church_roof_middle, [0,-64,64*2], 0),
                    (church_wall_tower_bottom, [0,64,64*2], 0),
                    (church_wall_tower_top, [0,64,112*2], 0),
                ],
                hitbox_size=(196, 320),
                hitbox_offset=(0, -32)
            ),

            # CHURCH ENTERANCE
            CompositeObject(
                parts_positions_rotations=[
                    (church_wall_entrance, [0,0,0], 0),
                ],
                hitbox_size=(64, 64),
            ),

            # CHURCH FENCE FRONT GATE
            CompositeObject(
                parts_positions_rotations=[
                    (church_gate_post, [32,0,0], 0),
                    (church_fence_middle, [0,0,0], 0),
                    (church_fence_middle, [-32,0,0], 0),
                ],
                hitbox_size=(96, 32),
            ),

            # CHURCH FENCE MIDDLE
            CompositeObject(
                parts_positions_rotations=[
                    (church_fence_middle, [64,0,0], 0),
                    (church_fence_middle, [32,0,0], 0),
                    (church_fence_post, [0,0,0], 0),
                    (church_fence_middle, [-32,0,0], 0),
                    (church_fence_middle, [-64,0,0], 0),
                ],
                hitbox_size=(160, 32),
            ),

            # CHURCH FENCE LEFT CORNER
            CompositeObject(
                parts_positions_rotations=[
                    (church_fence_middle, [32,0,0], 0),
                    (church_fence_middle, [0,0,0], 0),
                    (church_fence_corner, [-32,0,0], 0),
                ],
                hitbox_size=(96, 32),
            ),

            # CHURCH FENCE RIGHT CORNER
            CompositeObject(
                parts_positions_rotations=[
                    (church_fence_corner, [32,0,0], 90),
                    (church_fence_middle, [0,0,0], 0),
                    (church_fence_middle, [-32,0,0], 0),
                ],
                hitbox_size=(96, 32),
            ),

            # CHURCH FENCE BACK GATE
            CompositeObject(
                parts_positions_rotations=[
                    (church_gate_back, [32,0,0], 180),
                    (church_fence_middle, [0,0,0], 0),
                    (church_fence_middle, [-32,0,0], 0),
                ],
                hitbox_size=(96, 32),
            ),

            # CHURCH ENTRANCE PATH
            CompositeObject(
                parts_positions_rotations=[
                    (church_entrance_path_tile, [0,96,0], 90),
                    (church_entrance_path_tile, [0,32,0], -90),
                    (church_entrance_path_tile, [0,-32,0], 180),
                    (church_entrance_path_tile, [0,-96,0], 0),
                ],
                hitbox_size=(64, 256),
                type='texture',
            ),










            # DINER WALLS
            CompositeObject(
                parts_positions_rotations=[
                    (diner_wall_corner, [-128,64,0], 0),
                    (diner_wall_window, [-64,64,0], 0),
                    (diner_wall_front_entrance, [0,64,0], 0),
                    (diner_wall_window, [64,64,0], 0),
                    (diner_wall_corner, [128,64,0], 90),
                    (diner_wall_window, [128,0,0], 90),
                    (diner_wall_corner, [128,-64,0], 180),
                    (diner_wall_back, [64,-64,0], 180),
                    (diner_wall_back, [0,-64,0], 180),
                    (diner_wall_back, [-64,-64,0], 180),
                    (diner_wall_corner, [-128,-64,0], 270),
                    (diner_wall_window, [-128,0,0], 270),
                ],
                hitbox_size=(320, 192),
            ),

            # DINER ROOF
            CompositeObject(
                parts_positions_rotations=[
                    (diner_roof_corner, [-128,64,0], 0),
                    (diner_roof_sign_left, [-64,64,0], 0),
                    (diner_roof_sign_middle, [0,64,0], 0),
                    (diner_roof_sign_right, [64,64,0], 0),
                    (diner_roof_corner, [128,64,0], 90),
                    (diner_roof_side, [128,0,0], 90),
                    (diner_roof_corner, [128,-64,0], 180),
                    (diner_roof_side, [64,-64,0], 180),
                    (diner_roof_side, [0,-64,0], 180),
                    (diner_roof_side, [-64,-64,0], 180),
                    (diner_roof_corner, [-128,-64,0], 270),
                    (diner_roof_side, [-128,0,0], 270),
                    (diner_roof_middle, [-64,0,0], 0),
                    (diner_roof_middle, [0,0,0], 0),
                    (diner_roof_middle, [64,0,0], 0),
                ],
                hitbox_size=(320, 192),
            ),


            # GAS STATION WALLS
            CompositeObject(
                parts_positions_rotations=[
                    (gas_station_wall_corner_door, [64,64,0], 0),
                    (gas_station_wall_corner_window, [128,64,0], 0),
                    (gas_station_wall_side, [128,0,0], 180),
                    (gas_station_wall_corner, [128,-64,0], 180),
                    (gas_station_wall_corner, [64,-64,0], -90),
                    (gas_station_wall_side, [64,0,0], 0),
                    (gas_station_pump, [-128,64,0], 0),
                    (gas_station_pillar, [-128,0,0], 0),
                    (gas_station_pump, [-128,-64,0], 0),
                ],
                hitbox_size=(320, 192),
            ),

            # GAS STATION ROOF
            CompositeObject(
                parts_positions_rotations=[
                    (gas_station_roof_corner, [-128,64,0], 0),
                    (gas_station_roof_side, [-64,64,0], 0),
                    (gas_station_roof_side, [0,64,0], 0),
                    (gas_station_roof_side, [64,64,0], 0),
                    (gas_station_roof_corner, [128,64,0], 90),
                    (gas_station_roof_side, [128,0,0], 90),
                    (gas_station_roof_corner, [128,-64,0], 180),
                    (gas_station_roof_side, [64,-64,0], 180),
                    (gas_station_roof_side, [0,-64,0], 180),
                    (gas_station_roof_side, [-64,-64,0], 180),
                    (gas_station_roof_corner, [-128,-64,0], 270),
                    (gas_station_roof_side, [-128,0,0], 270),
                    (gas_station_roof_middle, [-64,0,0], 0),
                    (gas_station_roof_middle, [0,0,0], 0),
                    (gas_station_roof_middle, [64,0,0], 0),
                    (gas_station_sign, [-64,96,16*2], 0),
                ],
                hitbox_size=(320, 192),
            ),


            # MOTEL FLOOR UNIT
            CompositeObject(
                parts_positions_rotations=[
                    (motel_wall_door, [-64,64,0], 0),
                    (motel_wall_plain, [-64,0,0], 0),
                    (motel_wall_plain, [-64,-64,0], 180),

                    (motel_wall_window, [0,64,0], 0),
                    (motel_wall_window, [0,-64,0], 180),

                    (motel_wall_plain, [64,64,0], 0),
                    (motel_wall_window, [64,-64,0], 180),
                ],
                hitbox_size=(192, 192),
            ),

            # MOTEL RECEPTION BOTTOM FLOOR
            CompositeObject(
                parts_positions_rotations=[
                    (motel_wall_plain, [0,-96,0], 0),
                    (motel_wall_plain, [0,-32,0], 0),
                    (motel_wall_plain, [0,32,0], 0),
                    (motel_wall_reception, [0,96,0], 0),
                ],
                hitbox_size=(64, 256),
            ),

            # MOTEL RECEPTION MIDDLE FLOOR
            CompositeObject(
                parts_positions_rotations=[
                    (motel_wall_plain, [0,-96,0], 0),
                    (motel_wall_plain, [0,-32,0], 0),
                    (motel_wall_plain, [0,32,0], 0),
                    (motel_wall_plain, [0,96,0], 0),
                ],
                hitbox_size=(64, 256),
            ),

            # MOTEL RECEPTION TOP FLOOR
            CompositeObject(
                parts_positions_rotations=[
                    (motel_wall_roof_corner, [0,-96,0], 180),
                    (motel_wall_roof_side, [0,-32,0], 90),
                    (motel_wall_roof_corner, [0,32,0], 90),
                    (motel_roof_reception, [0,96,0], 0),
                ],
                hitbox_size=(64, 256),
            ),

            # MOTEL SIGN
            CompositeObject(
                parts_positions_rotations=[
                    (motel_sign, [0,0,0], 0),
                ],
                hitbox_size=(32, 8),
                hitbox_offset=(0, 4),
            ),      

            # MOTEL ROOF PARTS
            CompositeObject(
                parts_positions_rotations=[
                    (motel_wall_roof_corner, [-64,-64,0], -90),
                    (motel_wall_roof_side, [-64,0,0], -90),
                    (motel_wall_roof_corner, [-64,64,0], 0),
                    (motel_wall_roof_side, [0,-64,0], 180),
                    (motel_wall_roof_middle, [0,0,0], 0),
                    (motel_wall_roof_side, [0,64,0], 0),
                    (motel_wall_roof_side, [64,-64,0], 180),
                    (motel_wall_roof_middle, [64,0,0], 0),
                    (motel_wall_roof_side, [64,64,0], 0),
                ],
                hitbox_size=(192, 192),
            ),
            CompositeObject(
                parts_positions_rotations=[
                    (motel_wall_roof_side, [-64,-64,0], 180),
                    (motel_wall_roof_middle, [-64,0,0], 0),
                    (motel_wall_roof_side, [-64,64,0], 0),
                    (motel_wall_roof_side, [0,-64,0], 180),
                    (motel_wall_roof_middle, [0,0,0], 0),
                    (motel_wall_roof_side, [0,64,0], 0),
                    (motel_wall_roof_side, [64,-64,0], 180),
                    (motel_wall_roof_middle, [64,0,0], 0),
                    (motel_wall_roof_side, [64,64,0], 0),
                ],
                hitbox_size=(192, 192),
            ),

            # MOTEL BALCONY BOTTOM
            CompositeObject(
                parts_positions_rotations=[
                    (motel_balcony_bottom_corner, [-192,0,0], 0),
                    (motel_balcony_bottom_no_pillar, [-128,0,0], 0),
                    (motel_balcony_bottom_no_pillar, [-64,0,0], 0),
                    (motel_balcony_bottom_pillar, [0,0,0], 0),
                    (motel_balcony_bottom_no_pillar, [64,0,0], 0),
                    (motel_balcony_bottom_no_pillar, [128,0,0], 0),
                    (motel_balcony_bottom_pillar, [192,0,0], 0),
                ],
                hitbox_size=(448, 64)
            ),

            # MOTEL BALCONY MIDDLE
            CompositeObject(
                parts_positions_rotations=[
                    (motel_balcony_middle_corner, [-192,0,0], 0),
                    (motel_balcony_middle_no_pillar, [-128,0,0], 0),
                    (motel_balcony_middle_no_pillar, [-64,0,0], 0),
                    (motel_balcony_middle_pillar, [0,0,0], 0),
                    (motel_balcony_middle_no_pillar, [64,0,0], 0),
                    (motel_balcony_middle_no_pillar, [128,0,0], 0),
                    (motel_balcony_middle_pillar, [192,0,0], 0),
                ],
                hitbox_size=(448, 64)
            ),

            # MOTEL BALCONY TOP
            CompositeObject(
                parts_positions_rotations=[
                    (motel_balcony_top_corner, [-192,0,0], 0),
                    (motel_balcony_top_no_pillar, [-128,0,0], 0),
                    (motel_balcony_top_no_pillar, [-64,0,0], 0),
                    (motel_balcony_top_pillar, [0,0,0], 0),
                    (motel_balcony_top_no_pillar, [64,0,0], 0),
                    (motel_balcony_top_no_pillar, [128,0,0], 0),
                    (motel_balcony_top_pillar, [192,0,0], 0),
                ],
                hitbox_size=(448, 64)
            ),

            # MOTEL STAIRS
            CompositeObject(
                parts_positions_rotations=[
                    (motel_stairs_bottom, [0,-64,0], 0),
                    (motel_stairs_top, [0,0,0], 0),
                    (motel_balcony_bottom_stairs, [0,64,0], 0),
                    (motel_balcony_middle_stairs, [0,64,80*2], 0),
                    (motel_balcony_top_stairs, [0,64,160*2], 0),
                ],
                hitbox_size=(64, 192)
            ),


            # MOTEL RECEPTION
            CompositeObject(
                parts_positions_rotations=[
                    (motel_wall_reception, [0,0,0], 0),
                    (motel_wall_plain, [0,0,80*2], 0),
                    (motel_roof_reception, [0,0,160*2], 0),
                    (motel_sign, [0,32,80*2], 0),
                ],
                hitbox_size=(64, 64)
            ),



            # ELECTRIC POLE
            CompositeObject(
                parts_positions_rotations=[
                    (motel_wall_reception, [0,0,0], 0),
                    (motel_wall_plain, [0,0,80*2], 0),
                    (motel_roof_reception, [0,0,160*2], 0),
                    (motel_sign, [0,32,80*2], 0),
                ],
                hitbox_size=(64, 64)
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
