import pygame
import copy

from math import radians, sin, cos, sqrt, atan2

from graphics.rendering import global_render
from general_game_mechanics.dynamic_objects import DynamicObject


pygame.init()

font = pygame.font.SysFont(None, 20)
def display_fps(screen, clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'fps: {fps}', True, pygame.Color("white"))
    screen_width, screen_height = screen.get_size()
    text_rect = fps_text.get_rect(topright=(screen_width - 10, 10))
    screen.blit(fps_text, text_rect)


def cycle_list(direction, current_index, list):
    if direction == 'forwards':
        new_index = current_index + 1
    if direction == 'backwards':
        new_index = current_index - 1
    if new_index > len(list) - 1:
        new_index = 1
    if new_index < 0:
        new_index = len(list) + 1
    return new_index



class Level:
    def __init__(self, game):

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
        self.objects = []
        self.dynamic_objects = []
        self.cache = []

        """ GAME SETTINGS """
        self.game = game
        self.camera = self.game.camera
        self.sprite_stack_assets = self.game.sprite_stack_assets
        self.plant_systems = self.game.plant_systems
        self.grass_systems = self.game.grass_systems
        self.particle_systems = self.game.particle_systems
        

        self.fill_colour = (105, 66, 56)

        self.rotation_speed = 3
        self.scroll_speed = 0.1

        background = "background_test_grid.png"
        self.background = pygame.image.load(background).convert_alpha()




    def handle_controls_editing(self, keys, events):
        ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL
        shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT


        self.place = False
        self.next_item = False
        self.prev_item = False
        self.undo = False
        self.save = False

        self.rotate_clockwise = False
        self.rotate_counterclockwise = False

        for event in events:

            """ KEY PRESSES """
            if event.type == pygame.KEYDOWN:

                # UNDO, REDO
                if ctrl_pressed and event.key == pygame.K_z:
                    self.undo = True
                elif ctrl_pressed and event.key == pygame.K_s:
                    self.save = True

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

            # CYCLE ASSETS
            if event.type == pygame.MOUSEWHEEL:
                if not ( keys[pygame.K_LCTRL] or keys[pygame.K_LSHIFT]):
                    if event.y == 1:
                        self.next_item = True
                    elif event.y == -1:
                        self.prev_item = True

            # CYCLE ASSET SYSTEMS
            if self.place_plant:
                if keys[pygame.K_LSHIFT]:
                    if event.type == pygame.MOUSEWHEEL:
                        if event.y == -1:
                            self.rotate_clockwise = True
                        elif event.y == 1:
                            self.rotate_counterclockwise = True





    def edit_level(self):

        """ SPRITE STACK ASSETS """
        if self.place_sprite_stack:
            try:
                self.current_asset = copy.deepcopy(self.sprite_stack_assets[self.current_asset_index])
            except IndexError:
                self.current_asset = copy.deepcopy(self.sprite_stack_assets[0])
            self.current_asset.rotation = self.current_asset_rotation
            self.current_asset.position = self.place_position

            if self.place:
                self.objects.append(self.current_asset)
                if isinstance(self.current_asset, DynamicObject) and not self.current_asset.movelocked:
                    self.dynamic_objects.append(self.current_asset)

            if self.undo:
                if len(self.objects) > 0:
                    last_object = self.objects.pop()
                    if isinstance(last_object, DynamicObject):
                        self.dynamic_objects.remove(last_object)

            if self.next_item:
                if self.place_sprite_stack:
                    self.current_asset_index = cycle_list('forwards', self.current_asset_index, self.sprite_stack_assets)
                if self.place_plant:
                    self.current_asset_index = cycle_list('forwards', self.current_asset_index, self.plant_systems[self.plant_system_index].assets)
                if self.place_grass_tile:
                    self.current_asset_index = cycle_list('forwards', self.current_asset_index, self.grass_systems[self.grass_system_index].assets)

            if self.prev_item:
                if self.place_sprite_stack:
                    self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.sprite_stack_assets)
                if self.place_plant:
                    self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.plant_systems[self.plant_system_index].assets)
                if self.place_grass_tile:
                    self.current_asset_index = cycle_list('backwards', self.current_asset_index, self.grass_systems[self.grass_system_index].assets)


            if self.rotate_clockwise:
                if 'rotation' in vars(self.current_asset).keys():
                    self.current_asset_rotation += self.rotation_speed

            if self.rotate_counterclockwise:
                if 'rotation' in vars(self.current_asset).keys():
                    self.current_asset_rotation -= self.rotation_speed
        

        

        """ PLANT ASSETS """
        if self.place_plant:
            try:
                self.current_asset = copy.deepcopy(self.plant_systems[self.plant_system_index].assets[self.current_asset_index])
            except IndexError:
                self.current_asset = copy.deepcopy(self.plant_systems[self.plant_system_index].assets[0])
            self.current_asset.position = self.place_position
            for branch in self.current_asset.branches:
                branch.base_position = self.current_asset.position

            if self.place:
                self.plant_systems[self.plant_system_index].create_plant(self.current_asset_index, self.current_asset.position)
                for branch in self.plant_systems[self.plant_system_index].plants[-1].branches:
                    branch.base_position = self.current_asset.position

            if self.next_item:
                self.current_asset_index += 1
                if self.current_asset_index > len(self.plant_systems[self.plant_system_index].assets) - 1:
                    self.current_asset_index = 1

            if self.prev_item:
                self.current_asset_index -= 1
                if self.current_asset_index < 0:
                    self.current_asset_index = len(self.plant_systems[self.plant_system_index].assets) - 1

            if self.undo:
                if  len(self.plant_systems[self.plant_system_index].plants) > 0:
                    last_object = self.plant_systems[self.plant_system_index].plants.pop()




        """ GRASS ASSETS """
        if self.place_grass_tile:
            try:
                self.current_asset = copy.deepcopy(self.grass_systems[self.grass_system_index].assets[self.current_asset_index])
            except IndexError:
                self.current_asset = copy.deepcopy(self.grass_systems[self.grass_system_index].assets[0])
            self.current_asset.position = self.place_position

            if self.place:
                self.grass_systems[self.grass_system_index].create_tile(self.current_asset_index, self.current_asset.position)
                for blade in self.grass_systems[self.grass_system_index].tiles[-1].grass_blades:
                    blade.position[0] += self.grass_systems[self.grass_system_index].tiles[-1].position[0]
                    blade.position[1] += self.grass_systems[self.grass_system_index].tiles[-1].position[1]

            if self.next_item:
                self.current_asset_index += 1
                if self.current_asset_index > len(self.grass_systems[self.grass_system_index].assets) - 1:
                    self.current_asset_index = 1

            if self.prev_item:
                self.current_asset_index -= 1
                if self.current_asset_index < 0:
                    self.current_asset_index = len(self.grass_systems[self.grass_system_index].assets) - 1

            if self.undo:
                if  len(self.grass_systems[self.grass_system_index].tiles) > 0:
                    last_object = self.grass_systems[self.grass_system_index].tiles.pop()




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


        """ CAMERA MOVEMENT"""
        self.camera.follow(self.place_position)
        self.camera.move()




    def render(self):
        render_surface = pygame.Surface((self.game.render_width, self.game.render_height))

        render_surface.fill(self.fill_colour)
        global_render(
            screen=render_surface,
            camera=self.camera,
            objects=self.objects + [self.current_asset] + self.plant_systems[self.plant_system_index].plants + self.grass_systems[self.grass_system_index].tiles,
            bend_objects=self.dynamic_objects,
            background=self.background,
        )

        for grass_system in self.grass_systems:
            grass_system.apply_wind(1/20, self.game.time)

        upscaled_surface = pygame.transform.scale(render_surface, (self.game.screen_width, self.game.screen_height))
        self.game.screen.blit(upscaled_surface, (0, 0))

        display_fps(self.game.screen, self.game.clock, font)
