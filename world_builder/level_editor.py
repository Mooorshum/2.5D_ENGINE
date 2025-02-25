import pygame
import copy
import json

from math import radians, sin, cos, sqrt, atan2
from itertools import combinations

from graphics.rendering import global_render
from general_game_mechanics.dynamic_objects import DynamicObject, Vehicle, Character, Stairs
from general_game_mechanics.water import WaterBody

from graphics.camera import Camera
from graphics.grass import GrassTile
from graphics.plants import Plant
from graphics.sprite_stacks import SpritestackModel

from world_builder.loadpoints import LoadPoint


pygame.init()

font = pygame.font.SysFont(None, 20)

def display_fps(screen, clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'fps: {fps}', True, pygame.Color("white"))
    screen_width, screen_height = screen.get_size()
    text_rect = fps_text.get_rect(topright=(screen_width - 10, 10))
    screen.blit(fps_text, text_rect)

def display_place_info(screen, font, place_position, rotation):
    info = f'x: {int(place_position[0])},  y: {int(place_position[1])},  z: {int(place_position[2])},  rot: {rotation}'
    info_text = font.render(info, True, pygame.Color("white"))
    screen_width, screen_height = screen.get_size()
    text_rect = info_text.get_rect(topright=(screen_width - 10, 30))
    screen.blit(info_text, text_rect)


def cycle_list(direction, current_index, lst):
    if direction == 'forward':
        return (current_index + 1) % len(lst)
    elif direction == 'backwards':
        return (current_index - 1) % len(lst)
    return current_index



class Level:
    def __init__(self, game, name, map_size, fill_colour=(0, 0, 0)):

        self.game = game

        self.name = name

        """ LEVEL EDITING PARAMETERS """
        self.place_position = [0, 0, 0]
        self.place_height = 0

        self.current_asset = None
        self.current_asset_index = 0
        self.current_asset_rotation = 0

        self.plant_system_index = 0
        self.grass_system_index = 0
        self.particle_system_index = 0

        self.loadpoint_level_index = 0

        self.place_noninteractable_sprite_stack = True
        self.place_dynamic_sprite_stack = False
        self.place_plant = False
        self.place_grass_tile = False
        self.place_vehicle = False
        self.place_particle_system = False

        self.place_loadpoint = False

        self.rotate_clockwise = False
        self.rotate_counterclockwise = False
        self.place = False
        self.next_item = False
        self.prev_item = False
        self.undo = False
        self.save = False
        self.load = False
        self.cache = []

        self.play = False

        self.stairs = [
            Stairs(asset=self.game.stair_asset, asset_index=1, position=[200, 600, 0], rotation=0),
            #Stairs(asset=self.game.stair_asset, asset_index=1, position=[200, 580, 0], rotation=90),
            #Stairs(asset=self.game.stair_asset, asset_index=1, position=[600, 800, -31], rotation=210),
        ]


        """ DISPLAY SETTINGS """
        self.render_width = 400
        self.render_height = 300
        self.map_size = map_size
        self.camera = Camera(
            width=self.render_width,
            height=self.render_height,
            map_width=self.map_size[0],
            map_height=self.map_size[1]
        )


        """ GAME ASSETS """
        self.vehicle_assets = []
        self.non_interactable_sprite_stack_assets = []
        self.dynamic_sprite_stack_assets = []

        self.plant_systems = []
        self.grass_systems = []
     
        self.particle_system_presets = []
        self.npc_assets = []
        self.loadpoint_levels = []

        """ GAME OBJECTS """
        self.vehicles = []
        self.non_interactable_sprite_stack_objects = []
        self.dynamic_sprite_stack_objects = []
        self.water_objects = []
        self.particle_systems = []
        self.loadpoints = []

        """ CONFIGURING PLAYER OBJECT """
        self.player_asset = self.game.player_asset
        player_start_position = [self.map_size[0]//2, self.map_size[1]//2, 0]
        player_start_rotation = 0
        self.player = Character(asset=self.player_asset, asset_index=0, position=player_start_position, rotation=player_start_rotation)
        self.player.movelocked = False
        

        self.fill_colour = fill_colour

        self.rotation_speed = 2
        self.scroll_speed = 0.1


    def handle_controls_editing(self, keys):

        self.player.handle_controls(keys, self.game.events)

        if self.play:
            self.player.handle_aiming_and_shooting(self.place_position)

        ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL
        shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT

        self.place = False
        self.next_item = False
        self.prev_item = False
        self.undo = False
        self.save = False
        self.load = False

        self.rotate_clockwise = False
        self.rotate_counterclockwise = False

        self.next_system = False
        self.prev_system = False

        for event in self.game.events:

            """ KEY PRESSES """
            if event.type == pygame.KEYDOWN:

                # UNDO
                if ctrl_pressed and event.key == pygame.K_z:
                    self.undo = True

                # SWITCH BETWEEN DIFFERENT ASSET TYPES
                elif event.key == pygame.K_1:
                    self.place_noninteractable_sprite_stack = True
                    self.place_dynamic_sprite_stack = False
                    self.place_vehicle = False
                    self.place_plant = False
                    self.place_grass_tile = False
                    self.place_particle_system = False

                    self.place_loadpoint = False

                    self.play = False

                elif event.key == pygame.K_2:
                    self.place_noninteractable_sprite_stack = False
                    self.place_dynamic_sprite_stack = True
                    self.place_vehicle = False
                    self.place_plant = False
                    self.place_grass_tile = False
                    self.place_particle_system = False

                    self.place_loadpoint = False

                    self.play = False

                elif event.key == pygame.K_3:
                    self.place_noninteractable_sprite_stack = False
                    self.place_dynamic_sprite_stack = False
                    self.place_vehicle = True
                    self.place_plant = False
                    self.place_grass_tile = False
                    self.place_particle_system = False

                    self.place_loadpoint = False
                    
                    self.play = False

                elif event.key == pygame.K_4:
                    self.place_noninteractable_sprite_stack = False
                    self.place_dynamic_sprite_stack = False
                    self.place_vehicle = False
                    self.place_plant = True
                    self.place_grass_tile = False
                    self.place_particle_system = False

                    self.place_loadpoint = False

                    self.play = False

                elif event.key == pygame.K_5:
                    self.place_noninteractable_sprite_stack = False
                    self.place_dynamic_sprite_stack = False
                    self.place_vehicle = False
                    self.place_plant = False
                    self.place_grass_tile = True
                    self.place_particle_system = False

                    self.place_loadpoint = False

                    self.play = False

                elif event.key == pygame.K_6:
                    self.place_noninteractable_sprite_stack = False
                    self.place_dynamic_sprite_stack = False
                    self.place_vehicle = False
                    self.place_plant = False
                    self.place_grass_tile = False
                    self.place_particle_system = True

                    self.place_loadpoint = False

                    self.play = False

                elif event.key == pygame.K_7:
                    self.place_noninteractable_sprite_stack = False
                    self.place_dynamic_sprite_stack = False
                    self.place_vehicle = False
                    self.place_plant = False
                    self.place_grass_tile = False
                    self.place_particle_system = False

                    self.place_loadpoint = True
                    
                    self.play = False

                elif event.key == pygame.K_RETURN :
                    self.place_noninteractable_sprite_stack = False
                    self.place_dynamic_sprite_stack = False
                    self.place_vehicle = False
                    self.place_plant = False
                    self.place_grass_tile = False
                    self.place_particle_system = False

                    self.current_asset = None
                    self.place_loadpoint = False

                    self.play = True

                # SAVING AND LOADING LEVEL FROM FILE
                elif ctrl_pressed and event.key == pygame.K_s:
                    self.save = True
                elif ctrl_pressed and event.key == pygame.K_l:
                    self.load = True

            """ MOUSE CLICKS """
            # PLACE OBJECT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.place = True

            """ MOUSE SCROLLING + KEY PRESSES """
            # ZOOM IN, ZOOM OUT
            if keys[pygame.K_LCTRL]:
                    if event.type == pygame.MOUSEWHEEL:
                        if event.y == -1:
                            self.render_width *= 1 + self.scroll_speed
                            self.render_height *= 1 + self.scroll_speed
                            self.camera.width *= 1 + self.scroll_speed
                            self.camera.height *= 1 + self.scroll_speed
                        elif event.y == 1:
                            self.render_width /= 1 + self.scroll_speed
                            self.render_height /= 1 + self.scroll_speed
                            self.camera.width /= 1 + self.scroll_speed
                            self.camera.height /= 1 + self.scroll_speed

            # CHANGE OBJECT PLACEMENT HEIGHT
            if keys[pygame.K_z]:
                    if event.type == pygame.MOUSEWHEEL:
                        if event.y == -1:
                            self.place_height += 1
                        elif event.y == 1:
                            self.place_height -= 1
    
            # ROTATE ASSET
            if self.place_noninteractable_sprite_stack or self.place_dynamic_sprite_stack or self.place_vehicle:
                if keys[pygame.K_LSHIFT]:
                    if event.type == pygame.MOUSEWHEEL:
                        if event.y == -1:
                            self.rotate_clockwise = True
                        elif event.y == 1:
                            self.rotate_counterclockwise = True

            # CYCLE CURRENT SYSTEM ASSETS 
            if event.type == pygame.MOUSEWHEEL:
                if not ( keys[pygame.K_LCTRL] or keys[pygame.K_LSHIFT] or keys[pygame.K_z]):
                    if event.y == 1:
                        self.next_item = True
                    elif event.y == -1:
                        self.prev_item = True

            # CYCLE ASSET SYSTEMS
            if self.place_plant or self.place_grass_tile:
                if keys[pygame.K_LSHIFT]:
                    if event.type == pygame.MOUSEWHEEL:
                        if event.y == 1:
                            self.next_system = True
                        elif event.y == -1:
                            self.prev_system = True


    def edit_level(self):

        """ NON-INTERACTABLE SPRITE STACK ASSETS """
        if len(self.non_interactable_sprite_stack_assets) > 0:
            if self.place_noninteractable_sprite_stack:
                try:
                    asset = self.non_interactable_sprite_stack_assets[self.current_asset_index]
                    self.current_asset = SpritestackModel(asset, self.current_asset_index, self.place_position, self.current_asset_rotation)

                except IndexError:
                    self.current_asset_index = 0
                    asset = self.non_interactable_sprite_stack_assets[self.current_asset_index]
                    self.current_asset = SpritestackModel(asset, self.current_asset_index, self.place_position, self.current_asset_rotation)

                self.current_asset.rotation = self.current_asset_rotation
                self.current_asset.position = self.place_position

                if self.place:
                    self.non_interactable_sprite_stack_objects.append(self.current_asset)

                if self.next_item:
                    self.current_asset_index = cycle_list('forward', self.current_asset_index, self.non_interactable_sprite_stack_assets)

                if self.prev_item:
                    self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.non_interactable_sprite_stack_assets)

                if self.rotate_clockwise:
                    if 'rotation' in vars(self.current_asset).keys():
                        self.current_asset_rotation += 360 / self.current_asset.asset.num_unique_angles * self.rotation_speed

                if self.rotate_counterclockwise:
                    if 'rotation' in vars(self.current_asset).keys():
                        self.current_asset_rotation -= 360 / self.current_asset.asset.num_unique_angles * self.rotation_speed

                if self.undo:
                    if  len(self.non_interactable_sprite_stack_objects) > 0:
                        last_object = self.non_interactable_sprite_stack_objects.pop()


        """ DYNAMIC SPRITE STACK ASSETS """
        if len(self.dynamic_sprite_stack_assets) > 0:
            if self.place_dynamic_sprite_stack:
                try:
                    asset = self.dynamic_sprite_stack_assets[self.current_asset_index]
                    self.current_asset = DynamicObject(asset, self.current_asset_index, self.place_position, self.current_asset_rotation)

                except IndexError:
                    self.current_asset_index = 0
                    asset = self.dynamic_sprite_stack_assets[self.current_asset_index]
                    self.current_asset = DynamicObject(asset, self.current_asset_index, self.place_position, self.current_asset_rotation)

                self.current_asset.rotation = self.current_asset_rotation
                self.current_asset.position = self.place_position

                if self.place:
                    self.dynamic_sprite_stack_objects.append(self.current_asset)

                if self.next_item:
                    self.current_asset_index = cycle_list('forward', self.current_asset_index, self.dynamic_sprite_stack_assets)

                if self.prev_item:
                    self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.dynamic_sprite_stack_assets)

                if self.rotate_clockwise:
                    if 'rotation' in vars(self.current_asset).keys():
                        self.current_asset_rotation += 360 / self.current_asset.asset.num_unique_angles * self.rotation_speed

                if self.rotate_counterclockwise:
                    if 'rotation' in vars(self.current_asset).keys():
                        self.current_asset_rotation -= 360 / self.current_asset.asset.num_unique_angles * self.rotation_speed

                if self.undo:
                    if  len(self.dynamic_sprite_stack_objects) > 0:
                        last_object = self.dynamic_sprite_stack_objects.pop()








        """ VEHICLE ASSETS """
        if len(self.vehicle_assets) > 0:
            if self.place_vehicle:
                try:
                    asset = self.vehicle_assets[self.current_asset_index]
                    self.current_asset = Vehicle(asset, self.current_asset_index, self.place_position, self.current_asset_rotation)

                except IndexError:
                    self.current_asset_index = 0
                    asset = self.vehicle_assets[self.current_asset_index]
                    self.current_asset = Vehicle(asset, self.current_asset_index, self.place_position, self.current_asset_rotation)

                self.current_asset.rotation = self.current_asset_rotation
                self.current_asset.position = self.place_position

                if self.place:
                    self.vehicles.append(self.current_asset)

                if self.next_item:
                    self.current_asset_index = cycle_list('forward', self.current_asset_index, self.vehicle_assets)

                if self.prev_item:
                    self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.vehicle_assets)

                if self.rotate_clockwise:
                    if 'rotation' in vars(self.current_asset).keys():
                        self.current_asset_rotation += 360 / self.current_asset.asset.num_unique_angles * self.rotation_speed

                if self.rotate_counterclockwise:
                    if 'rotation' in vars(self.current_asset).keys():
                        self.current_asset_rotation -= 360 / self.current_asset.asset.num_unique_angles * self.rotation_speed

                if self.undo:
                    if  len(self.vehicles) > 0:
                        last_object = self.vehicles.pop()






        """ PLANT ASSETS """
        if len(self.plant_systems) > 0:
            if self.place_plant:
                try:
                    plant_asset = self.plant_systems[self.plant_system_index].assets[self.current_asset_index]
                except IndexError:
                    self.current_asset_index = 0
                    plant_asset = self.plant_systems[self.plant_system_index].assets[self.current_asset_index]
                plant = Plant(plant_asset, self.place_position)
                self.current_asset = plant
                self.current_asset.position = self.place_position
                for branch in self.current_asset.branches:
                    branch.base_position = self.current_asset.position

                if self.place:
                    self.plant_systems[self.plant_system_index].create_plant(self.current_asset_index, self.current_asset.position)
                    for branch in self.current_asset.branches:
                        branch.base_position = self.current_asset.position

                if self.next_item:
                    self.current_asset_index = cycle_list('forward', self.current_asset_index, self.plant_systems[self.plant_system_index].assets)

                if self.prev_item:
                    self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.plant_systems[self.plant_system_index].assets)

                if self.next_system:
                    self.plant_system_index = cycle_list('forward', self.plant_system_index, self.plant_systems)

                if self.prev_system:
                    self.plant_system_index = cycle_list('backwards', self.plant_system_index, self.plant_systems)

                if self.undo:
                    if  len(self.plant_systems[self.plant_system_index].plants) > 0:
                        last_object = self.plant_systems[self.plant_system_index].plants.pop()


        """ GRASS ASSETS """
        if len(self.grass_systems) > 0:
            if self.place_grass_tile:
                try:
                    grass_tile_asset = self.grass_systems[self.grass_system_index].assets[self.current_asset_index]
                except IndexError:
                    self.current_asset_index = 0
                    grass_tile_asset = self.grass_systems[self.grass_system_index].assets[self.current_asset_index]
                grass_tile = GrassTile(self.place_position, grass_tile_asset)
                self.current_asset = grass_tile
                self.current_asset.position = self.place_position

                if self.place:
                    self.grass_systems[self.grass_system_index].create_tile(self.current_asset_index, self.current_asset.position)

                if self.next_item:
                    self.current_asset_index = cycle_list('forward', self.current_asset_index, self.grass_systems[self.grass_system_index].assets)

                if self.prev_item:
                    self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.grass_systems[self.grass_system_index].assets)

                if self.next_system:
                    self.grass_system_index = cycle_list('forward', self.grass_system_index, self.grass_systems)

                if self.prev_system:
                    self.grass_system_index = cycle_list('backwards', self.grass_system_index, self.grass_systems)

                if self.undo:
                    if  len(self.grass_systems[self.grass_system_index].tiles) > 0:
                        last_object = self.grass_systems[self.grass_system_index].tiles.pop()


        """ PARTICLE SYSTEMS """
        if len(self.particle_system_presets) > 0:
            if self.place_particle_system:
                try:
                    particle_system = copy.deepcopy(self.particle_system_presets[self.particle_system_index])
                except IndexError:
                    self.current_asset_index = 0
                    particle_system = copy.deepcopy(self.particle_system_presets[self.particle_system_index])
                particle_system.position = self.place_position
                particle_system.asset_index = self.particle_system_index
                self.current_asset = particle_system

                if self.place:
                    self.particle_systems.append(self.current_asset)

                if self.next_item:
                    self.particle_system_index = cycle_list('forward', self.current_asset_index, self.particle_system_presets)

                if self.prev_item:
                    self.particle_system_index = cycle_list('backwards', self.current_asset_index, self.particle_system_presets)

                if self.undo:
                    if  len(self.particle_systems) > 0:
                        last_object = self.particle_systems.pop()


        """ LOADPOINTS """
        if len(self.loadpoint_levels) > 0:
            if self.place_loadpoint:
                try:
                    loadpoint_level = self.loadpoint_levels[self.current_asset_index]
                except IndexError:
                    self.current_asset_index = 0
                    loadpoint_level = self.loadpoint_levels[self.current_asset_index]

                if self.current_asset_index % 2 == 0:
                    loadpoint_colour = (255, 255, 0)
                else:
                    loadpoint_colour = (255, 150, 150)

                loadpoint = LoadPoint(
                    level=loadpoint_level,
                    level_index=self.current_asset_index,
                    colour=loadpoint_colour
                )
                loadpoint.position = self.place_position
                self.current_asset = loadpoint

                if self.place:
                    self.loadpoints.append(self.current_asset)

                if self.next_item:
                    self.current_asset_index = cycle_list('forward', self.current_asset_index, self.loadpoint_levels)

                if self.prev_item:
                    self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.loadpoint_levels)

                if self.undo:
                    if  len(self.loadpoints) > 0:
                        last_object = self.loadpoints.pop()


        """ SAVING AND LOADING LEVEL """
        if self.save:
            self.save_level()
        if self.load:
                self.load_level()


    def save_level(self):
        level_data = {}

        # SAVING NON-INTERACTABLE SPRITESTACK OBJECTS DATA
        objects_data = []
        for obj in self.non_interactable_sprite_stack_objects:
            object_data = obj.get_data()
            objects_data.append(object_data)
        level_data['non_interactable_spritestack_objects_data'] = objects_data

        # SAVING DYNAMIC SPRITESTACK OBJECTS DATA
        objects_data = []
        for obj in self.dynamic_sprite_stack_objects:
            object_data = obj.get_data()
            objects_data.append(object_data)
        level_data['dynamic_spritestack_objects_data'] = objects_data

        # SAVING GRASS SYSTEMS DATA
        grass_systems_data = []
        for grass_system in self.grass_systems:
            grass_system_data = grass_system.get_data()
            grass_systems_data.append(grass_system_data)
        level_data['grass_systems'] = grass_systems_data

        # SAVING PLANT SYSTEMS DATA
        plant_systems_data = []
        for plant_system in self.plant_systems:
            plant_system_data = plant_system.get_data()
            plant_systems_data.append(plant_system_data)
        level_data['plant_systems'] = plant_systems_data

        # SAVING PARTICLE SYSTEMS DATA
        particle_systems_data = []
        for particle_system in self.particle_systems:
            particle_system_data = particle_system.get_data()
            particle_systems_data.append(particle_system_data)
        level_data['particle_systems'] = particle_systems_data

        # SAVING LOADPOINTS
        loadpoints_data = []
        for loadpoint in self.loadpoints:
            loadpoint_data = {}
            loadpoint_data['position'] = loadpoint.position
            loadpoint_data['level_index'] = loadpoint.level_index
            loadpoint_data['colour'] = loadpoint.colour
            loadpoints_data.append(loadpoint_data)
        level_data['loadpoints'] = loadpoints_data


        with open(f'{self.name}_data.json', "w") as file:
            json.dump(level_data, file, indent=4)


    def load_level(self):

        try:
            with open(f'{self.name}_data.json', "r") as file:
                data = json.load(file)

                # LOADING NON-INTERACTABLE SPRITESTACK OBJECTS DATA
                self.non_interactable_sprite_stack_objects = []
                for object_data in data['non_interactable_spritestack_objects_data']:
                    object_position = object_data['position']
                    object_rotation = object_data['rotation']
                    asset_index = object_data['asset_index']
                    object_asset = self.non_interactable_sprite_stack_assets[asset_index]
                    self.non_interactable_sprite_stack_objects.append(SpritestackModel(
                        object_asset,
                        asset_index,
                        object_position,
                        object_rotation
                    ))

                # LOADING DYNAMIC SPRITESTACK OBJECTS DATA
                self.dynamic_sprite_stack_objects = []
                for object_data in data['dynamic_spritestack_objects_data']:
                    object_position = object_data['position']
                    object_rotation = object_data['rotation']
                    asset_index = object_data['asset_index']
                    object_asset = self.dynamic_sprite_stack_assets[asset_index]
                    self.dynamic_sprite_stack_objects.append(DynamicObject(
                        object_asset,
                        asset_index,
                        object_position,
                        object_rotation
                    ))

                # LOADING GRASS SYSTEM DATA
                for grass_system_index in range(len(self.grass_systems)):
                    self.grass_systems[grass_system_index].load(data['grass_systems'][grass_system_index])

                # LOADING PLANT SYSTEM DATA
                for plant_system_index in range(len(self.plant_systems)):
                    self.plant_systems[plant_system_index].load(data['plant_systems'][plant_system_index])

                # LOADING PARTICLE SYSTEM DATA
                self.particle_systems = []
                for particle_system_data in data['particle_systems']:
                    particle_system_position = particle_system_data['position']
                    particle_system_asset = self.particle_system_presets[particle_system_data['asset_index']]
                    particle_system_object = copy.deepcopy(particle_system_asset)
                    particle_system_object.position = particle_system_position
                    particle_system_object.asset_index = particle_system_data['asset_index']
                    self.particle_systems.append(particle_system_object)

                # LOADING LOADPOINT DATA
                self.loadpoints = []
                for loadpoint in data['loadpoints']:
                    loadpoint_object = LoadPoint(
                        level=self.loadpoint_levels[loadpoint['level_index']],
                        level_index=loadpoint['level_index'],
                        colour=loadpoint['colour']
                    )
                    loadpoint_object.position = loadpoint['position']
                    self.loadpoints.append(loadpoint_object)

        except FileNotFoundError:
            print(f'No file found for {self.name}')


    def update(self):

        

        """ CALCULATING OBJECT PALCEMENT POSITION """
        display_surface = pygame.display.get_surface()
        display_width, display_height = display_surface.get_size()
        scale_factor_x = self.camera.width / display_width
        scale_factor_y = self.camera.height / display_height
        
        mouse_camera_x = pygame.mouse.get_pos()[0] * scale_factor_x
        mouse_camera_y = pygame.mouse.get_pos()[1] * scale_factor_y

        mouse_camera_centre_x = mouse_camera_x - self.camera.width/2
        mouse_camera_centre_y = mouse_camera_y - self.camera.height/2

        camera_angle = -radians(self.camera.rotation)

        d = sqrt((mouse_camera_centre_x)**2 + (mouse_camera_centre_y)**2)
        gamma = atan2(mouse_camera_centre_y, mouse_camera_centre_x)

        place_position_x = d * cos(camera_angle + gamma) + self.camera.position[0]
        place_position_y = d * sin(camera_angle + gamma) + self.camera.position[1]

        self.place_position = [place_position_x, place_position_y, self.place_height]   

        """ CAMERA MOVEMENT"""
        self.camera.follow(self.player.position)
        self.camera.move()

        """ UPDATING PLAYER AND ALL PLAYER-LINKED OBJECTS """
        self.player.update(self.camera)

        """ HANDLING OBJECT MOVEMENT """
        for obj in self.dynamic_sprite_stack_objects + self.vehicles:
            obj.move()

        """ HANDLING VEHICLE DRIVING """
        if self.play:
            for vehicle in self.vehicles:
                vehicle.handle_driver(self.player)






        """ HANDLING DYNAMIC OBJECT COLLISION """
        dynamic_objects = self.dynamic_sprite_stack_objects + [self.player] + self.vehicles + self.player.projectiles + self.non_interactable_sprite_stack_objects
        for obj in dynamic_objects:
            obj.hitbox.collided = False
            obj.hitbox.update() # UPDATING HITBOX AND RENDER VERTICES

        for object_1, object_2 in combinations(dynamic_objects, 2):
                object_1.hitbox.colour = (255, 0, 0)
                object_2.hitbox.colour = (255, 0, 0)
                if not (object_1.movelocked and object_2.movelocked):

                    object_1_is_on_screen_x = abs(self.camera.position[0] - object_1.position[0]) < self.camera.width/2
                    if object_1_is_on_screen_x:
                        object_1_is_on_screen_y = abs(self.camera.position[1] - object_1.position[1]) < self.camera.height/2
                        if object_1_is_on_screen_y:

                            object_2_is_on_screen_x = abs(self.camera.position[0] - object_2.position[0]) < self.camera.width/2
                            if object_2_is_on_screen_x:
                                object_2_is_on_screen_y = abs(self.camera.position[1] - object_2.position[1]) < self.camera.height/2
                                if object_2_is_on_screen_y:

                                    check_threshold_distance_x = (object_1.hitbox.size[0] + object_2.hitbox.size[0]) * sqrt(2)
                                    dx = abs(object_1.position[0] - object_2.position[0])
                                    if dx < check_threshold_distance_x:

                                        check_threshold_distance_y = (object_1.hitbox.size[1] + object_2.hitbox.size[1]) * sqrt(2)
                                        dy = abs(object_1.position[1] - object_2.position[1])
                                        if dy < check_threshold_distance_y:

                                            # CHECKING FOR COLLISION
                                            object_1.hitbox.check_collision(object_2)

                                            # IF A COLLISION HAS HAPPENED
                                            if object_2 in object_1.hitbox.colliding_objects.keys():

                                                # GETTING COLLISION DATA
                                                mtv_axis = object_1.hitbox.colliding_objects[object_2]['mtv_axis']
                                                overlap = object_1.hitbox.colliding_objects[object_2]['overlap']

                                                # RESOLVING COLLISION
                                                if object_1.interactable and object_2.interactable:
                                                    object_1.hitbox.resolve_collision(object_2, mtv_axis, overlap)

        for obj in dynamic_objects:
            if obj.hitbox.collided:
                obj.hitbox.colour = (255, 255, 0)
            else:
                obj.hitbox.colour = (255, 0, 0)
            





        """ UPDATING PARTICLE SYSTEMS """
        for particle_system in self.particle_systems:
            particle_system.update()

        """ HANDLING LOADPOINTS """
        for loadpoint in self.loadpoints:
            loadpoint.handle_loading(player=self.player, game=self.game)

        """ HANDLING STAIRS """
        for stairs in self.stairs:
            distance = sqrt((self.player.position[0] - stairs.position[0])**2 + (self.player.position[1] - stairs.position[1])**2)
            effect_radius = sqrt(stairs.hitbox.size[0]**2 + stairs.hitbox.size[1]**2)
            if distance <= effect_radius:
                stairs.control_object_z_offset(self.player)




    def render(self):
        render_surface = pygame.Surface((self.render_width, self.render_height))
        render_surface.fill(self.fill_colour)

        # GETTING A LIST OF ALL PLANT OBJECTS ACROSS ALL PLANT SYSTEMS
        plants = []
        for i in range(len(self.plant_systems)):
            system_plants = self.plant_systems[i].plants
            for j in range(len(system_plants)):
                plants.append(system_plants[j])

        # GETTING A LIST OF ALL PLANT OBJECTS ACROSS ALL PLANT SYSTEMS
        grass_tiles = []
        for i in range(len(self.grass_systems)):
            system_tiles = self.grass_systems[i].tiles
            for j in range(len(system_tiles)):
                grass_tiles.append(system_tiles[j])

        """ RENDERING ALL LEVEL OBJECTS """
        render_objects= self.stairs + [self.player] + self.vehicles + self.non_interactable_sprite_stack_objects + self.dynamic_sprite_stack_objects + plants + grass_tiles + self.particle_systems + self.loadpoints
        if self.current_asset:
            render_objects += [self.current_asset]
        global_render(
            screen=render_surface,
            camera=self.camera,
            objects=render_objects,
            bend_objects=[self.player] + self.vehicles, #self.dynamic_sprite_stack_objects + [self.player] + self.vehicles,
        )

        """ RENDERING PLAYER PROJECTILES """
        for projectile in self.player.projectiles:
            projectile.render(screen=render_surface, camera=self.camera)

        for grass_system in self.grass_systems:
            grass_system.apply_wind()

        upscaled_surface = pygame.transform.scale(render_surface, (self.game.screen_width, self.game.screen_height))
        self.game.screen.blit(upscaled_surface, (0, 0))


        display_fps(self.game.screen, self.game.clock, font)

        display_place_info(self.game.screen, font, self.place_position, self.current_asset_rotation)
