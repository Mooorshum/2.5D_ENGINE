import pygame
import copy
import json

from math import radians, sin, cos, sqrt, atan2

from graphics.rendering import global_render
from general_game_mechanics.dynamic_objects import DynamicObject, Character

from graphics.grass import GrassTile
from graphics.plants import Plant
from graphics.sprite_stacks import SpritestackModel


pygame.init()

font = pygame.font.SysFont(None, 20)
def display_fps(screen, clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'fps: {fps}', True, pygame.Color("white"))
    screen_width, screen_height = screen.get_size()
    text_rect = fps_text.get_rect(topright=(screen_width - 10, 10))
    screen.blit(fps_text, text_rect)


def cycle_list(direction, current_index, lst):
    if direction == 'forward':
        return (current_index + 1) % len(lst)
    elif direction == 'backwards':
        return (current_index - 1) % len(lst)
    return current_index



class Level:
    def __init__(self, game):

        self.name = 'test_level'

        """ LEVEL EDITING """
        self.place_position = [0, 0]
        self.current_asset = None
        self.current_asset_index = 0
        self.current_asset_rotation = 0

        self.plant_system_index = 0
        self.grass_system_index = 0

        self.place_sprite_stack = True
        self.place_plant = False
        self.place_grass_tile = False

        self.rotate_clockwise = False
        self.rotate_counterclockwise = False
        self.place = False
        self.next_item = False
        self.prev_item = False
        self.undo = False
        self.save = False
        self.load = False
        self.objects = []
        self.dynamic_objects = []
        self.cache = []


        """ GAME ASSETS """
        self.game = game
        self.camera = self.game.camera

        self.sprite_stack_assets = self.game.sprite_stack_assets

        self.plant_systems = self.game.plant_systems
        self.grass_systems = self.game.grass_systems

        self.particle_systems = self.game.particle_systems

        self.npc_assets = self.game.npc_assets

        """ CONFIGURING PLAYER OBJECT """
        self.player_asset = self.game.player_asset
        player_start_position = [200, 200]
        player_start_rotation = 0
        self.player = Character(asset=self.player_asset, asset_index=0, position=player_start_position, rotation=player_start_rotation)
        self.player.movelocked = False
        

        self.fill_colour = (105, 66, 56)

        self.rotation_speed = 2
        self.scroll_speed = 0.1

        background = "background_small.png"
        self.background = pygame.image.load(background).convert_alpha()




    def handle_controls_editing(self, keys, events):

        self.player.handle_movement(keys)

        
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

        for event in events:

            """ KEY PRESSES """
            if event.type == pygame.KEYDOWN:

                # UNDO
                if ctrl_pressed and event.key == pygame.K_z:
                    self.undo = True

                # SWITCH BETWEEN DIFFERENT ASSET TYPES
                elif event.key == pygame.K_1:
                    self.place_sprite_stack = True
                    self.place_plant = False
                    self.place_grass_tile = False
                elif event.key == pygame.K_2:
                    self.place_sprite_stack = False
                    self.place_plant = True
                    self.place_grass_tile = False
                elif event.key == pygame.K_3:
                    self.place_sprite_stack = False
                    self.place_plant = False
                    self.place_grass_tile = True

                # SAVING AND LOADING LEVEL FROM FILE
                elif ctrl_pressed and event.key == pygame.K_s:
                    self.save = True
                elif ctrl_pressed and event.key == pygame.K_l:
                    self.load = True


            """ MOUSE CLICKS """
            # PLACE ASSET
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.place = True


            """ MOUSE SCROLLING + KEY PRESSES """
            # ZOOM IN, ZOOM OUT
            if keys[pygame.K_LCTRL]:
                    if event.type == pygame.MOUSEWHEEL:
                        if event.y == -1:
                            self.game.render_width *= 1 + self.scroll_speed
                            self.game.render_height *= 1 + self.scroll_speed
                            self.camera.width *= 1 + self.scroll_speed
                            self.camera.height *= 1 + self.scroll_speed
                        elif event.y == 1:
                            self.game.render_width /= 1 + self.scroll_speed
                            self.game.render_height /= 1 + self.scroll_speed
                            self.camera.width /= 1 + self.scroll_speed
                            self.camera.height /= 1 + self.scroll_speed

            # ROTATE ASSET
            if self.place_sprite_stack:
                if keys[pygame.K_LSHIFT]:
                    if event.type == pygame.MOUSEWHEEL:
                        if event.y == -1:
                            self.rotate_clockwise = True
                        elif event.y == 1:
                            self.rotate_counterclockwise = True

        

            # CYCLE CURRENT SYSTEM ASSETS 
            if event.type == pygame.MOUSEWHEEL:
                if not ( keys[pygame.K_LCTRL] or keys[pygame.K_LSHIFT]):
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

        """ SPRITE STACK ASSETS """
        if self.place_sprite_stack:
            try:
                asset = self.sprite_stack_assets[self.current_asset_index]
                self.current_asset = SpritestackModel(asset, self.current_asset_index, self.place_position, self.current_asset_rotation)
            except IndexError:
                self.current_asset_index = 0
                asset = self.sprite_stack_assets[self.current_asset_index]
                self.current_asset = SpritestackModel(asset, self.current_asset_index, self.place_position, self.current_asset_rotation)

            self.current_asset.rotation = self.current_asset_rotation
            self.current_asset.position = self.place_position

            if self.place:
                self.objects.append(self.current_asset)
                if isinstance(self.current_asset, DynamicObject) and not self.current_asset.movelocked:
                    self.dynamic_objects.append(self.current_asset)

            if self.next_item:
                self.current_asset_index = cycle_list('forward', self.current_asset_index, self.sprite_stack_assets)

            if self.prev_item:
                self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.sprite_stack_assets)

            if self.rotate_clockwise:
                if 'rotation' in vars(self.current_asset).keys():
                    self.current_asset_rotation += 360 / self.current_asset.asset.num_unique_angles * self.rotation_speed

            if self.rotate_counterclockwise:
                if 'rotation' in vars(self.current_asset).keys():
                    self.current_asset_rotation -= 360 / self.current_asset.asset.num_unique_angles * self.rotation_speed

            if self.undo:
                if len(self.objects) > 0:
                    last_object = self.objects.pop()
                    if isinstance(last_object, DynamicObject) and not self.current_asset.movelocked:
                        self.dynamic_objects.remove(last_object)

        """ PLANT ASSETS """
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

        """ SAVING AND LOADING LEVEL """
        if self.save:
            self.save_level()
        if self.load:
                self.load_level()


    def save_level(self):
        level_data = {}

        # SAVING SPRITESTACK OBJECT DATA
        objects_data = []
        for obj in self.objects:
            object_data = obj.get_data()
            objects_data.append(object_data)
        level_data['spritestack_objects_data'] = objects_data

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

        with open(f'{self.name}_data.json', "w") as file:
            json.dump(level_data, file, indent=4)


    def load_level(self):

        try:
            with open(f'{self.name}_data.json', "r") as file:
                data = json.load(file)

                # LOADING SPRITESTACK OBJECTS DATA
                self.objects = []
                for object_data in data['spritestack_objects_data']:
                    object_position = object_data['position']
                    object_rotation = object_data['rotation']
                    asset_index = object_data['asset_index']
                    object_asset = self.sprite_stack_assets[asset_index]
                    self.objects.append(SpritestackModel(
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

        self.place_position = [place_position_x, place_position_y]   

        """ PLAYER MOVEMENT"""
        self.player.move(self.game.camera)

        """ CAMERA MOVEMENT"""
        self.camera.follow(self.player.position)
        self.camera.move()




    def render(self):
        render_surface = pygame.Surface((self.game.render_width, self.game.render_height))
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

        global_render(
            screen=render_surface,
            camera=self.camera,
            objects=self.objects + [self.current_asset] + plants + grass_tiles + [self.player],
            bend_objects=self.dynamic_objects + [self.player],
            background=self.background,
        )

        for grass_system in self.grass_systems:
            grass_system.apply_wind()

        upscaled_surface = pygame.transform.scale(render_surface, (self.game.screen_width, self.game.screen_height))
        self.game.screen.blit(upscaled_surface, (0, 0))


        display_fps(self.game.screen, self.game.clock, font)
