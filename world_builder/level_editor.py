import pygame
import copy
import json

from math import radians, sin, cos, sqrt, atan2
from itertools import combinations

from graphics.rendering import global_render, get_visible_objects, depth_sort
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

def display_place_info(screen, font, place_position, rotation, mode, play):
    info = f'x: {int(place_position[0])},  y: {int(place_position[1])},  z: {int(place_position[2])},  rot: {rotation}, mode: {mode}, PLAY: {play}'
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




def control_editing(level):
    if level.play:
        return
    
    if level.current_asset_group == 'texture':
        asset = level.texture_assets[level.current_asset_index]
        level.current_asset = DynamicObject(asset, level.current_asset_index, level.place_position, level.current_asset_rotation)
        level.current_asset.rotation = level.current_asset_rotation
        level.current_asset.position = level.place_position
            
    if level.current_asset_group == 'object':
        asset = level.object_assets[level.current_asset_index]
        level.current_asset = DynamicObject(asset, level.current_asset_index, level.place_position, level.current_asset_rotation)
        level.current_asset.rotation = level.current_asset_rotation
        level.current_asset.position = level.place_position

    if level.current_asset_group == 'vehicle':
        asset = level.vehicle_assets[level.current_asset_index]
        level.current_asset = Vehicle(asset, level.current_asset_index, level.place_position, level.current_asset_rotation)
        level.current_asset.rotation = level.current_asset_rotation
        level.current_asset.position = level.place_position

    if level.current_asset_group == 'plant':
        plant_asset = level.plant_systems[level.plant_system_index].assets[level.current_asset_index]
        plant = Plant(plant_asset, level.place_position)
        level.current_asset = plant
        level.current_asset.position = level.place_position
        for branch in level.current_asset.branches:
            branch.base_position = level.current_asset.position

    if level.current_asset_group == 'grass':
        grass_tile_asset = level.grass_systems[level.grass_system_index].assets[level.current_asset_index]
        grass_tile = GrassTile(level.place_position, grass_tile_asset)
        level.current_asset = grass_tile
        level.current_asset.position = level.place_position
        current_asset = level.grass_systems[level.grass_system_index].assets[level.current_asset_index]

    if level.current_asset_group == 'particle_system':
        particle_system = copy.deepcopy(level.particle_system_assets[level.particle_system_index])
        particle_system.position = level.place_position
        particle_system.asset_index = level.particle_system_index
        level.current_asset = particle_system

    if level.current_asset_group == 'loadpoint':
        loadpoint_level = level.loadpoint_levels[level.current_asset_index]
        loadpoint = LoadPoint(
            level=loadpoint_level,
            level_index=level.current_asset_index,
            colour=(255, 255, 0)
        )
        loadpoint.position = level.place_position
        level.current_asset = loadpoint


    if level.current_asset:
        if level.current_action == 'place':
            if level.current_asset_group == 'texture':
                level.textures.append(level.current_asset)
            if level.current_asset_group == 'object':
                level.objects.append(level.current_asset)
            if level.current_asset_group =='vehicle':
                level.current_asset.hitbox.collidable = True
                level.vehicles.append(level.current_asset)
            if level.current_asset_group == 'plant':
                level.plant_systems[level.plant_system_index].create_plant(level.current_asset_index, level.place_position)
                for branch in level.current_asset.branches:
                        branch.base_position = level.place_position
            if level.current_asset_group == 'grass':
                level.grass_systems[level.grass_system_index].create_tile(level.current_asset_index, level.place_position)
            if level.current_asset_group == 'particle_system':
                level.particle_systems.append(level.current_asset)
            



        if level.current_action == 'next_item':
            if level.current_asset_group == 'texture':
                level.current_asset_index = cycle_list('forward', level.current_asset_index, level.texture_assets)
            if level.current_asset_group == 'object':
                level.current_asset_index = cycle_list('forward', level.current_asset_index, level.object_assets)
            if level.current_asset_group =='vehicle':
                level.current_asset_index = cycle_list('forward', level.current_asset_index, level.vehicle_assets)
            if level.current_asset_group == 'plant':
                level.current_asset_index = cycle_list('forward', level.current_asset_index, level.plant_systems[level.plant_system_index].assets)
            if level.current_asset_group == 'grass':
                level.current_asset_index = cycle_list('forward', level.current_asset_index, level.grass_systems[level.grass_system_index].assets)
            if level.current_asset_group == 'particle_system':
                level.current_asset_index = cycle_list('forward', level.current_asset_index, level.particle_system_assets)


        if level.current_action == 'prev_item':
            if level.current_asset_group == 'texture':
                level.current_asset_index = cycle_list('backwards', level.current_asset_index, level.texture_assets)
            if level.current_asset_group == 'object':
                level.current_asset_index = cycle_list('backwards', level.current_asset_index, level.object_assets)
            if level.current_asset_group =='vehicle':
                level.current_asset_index = cycle_list('backwards', level.current_asset_index, level.vehicle_assets)
            if level.current_asset_group == 'plant':
                level.current_asset_index = cycle_list('backwards', level.current_asset_index, level.plant_systems[level.plant_system_index].assets)
            if level.current_asset_group == 'grass':
                level.current_asset_index = cycle_list('backwards', level.current_asset_index, level.grass_systems[level.grass_system_index].assets)
            if level.current_asset_group == 'particle_system':
                level.current_asset_index = cycle_list('backwards', level.current_asset_index, level.particle_system_assets)


        if level.current_action == 'rotate_clockwise_or_next_system':
            if level.current_asset_group in ['texture', 'object', 'vehicle']:
                level.current_asset_rotation += 360 / level.current_asset.asset.num_unique_angles * level.rotation_speed
            if level.current_asset_group == 'plant':
                level.plant_system_index = cycle_list('forward', level.plant_system_index, level.plant_systems)
            if level.current_asset_group == 'grass':
                level.grass_system_index = cycle_list('forward', level.grass_system_index, level.grass_systems)

        if level.current_action == 'rotate_counterclockwise_or_prev_system':
            if level.current_asset_group in ['texture', 'object', 'vehicle']:
                level.current_asset_rotation -= 360 / level.current_asset.asset.num_unique_angles * level.rotation_speed
            if level.current_asset_group == 'plant':
                level.plant_system_index = cycle_list('backwards', level.plant_system_index, level.plant_systems)
            if level.current_asset_group == 'grass':
                level.grass_system_index = cycle_list('backwards', level.grass_system_index, level.grass_systems)


    if level.current_action == 'undo':
        if level.current_asset_group == 'texture':
            if  len(level.textures) > 0:
                last_object = level.textures.pop()
        if level.current_asset_group == 'object':
            if  len(level.objects) > 0:
                last_object = level.objects.pop()
        if level.current_asset_group =='vehicle':
            if  len(level.vehicles) > 0:
                last_object = level.vehicles.pop()
        if level.current_asset_group == 'plant':
            if  len(level.plant_systems[level.plant_system_index].plants) > 0:
                last_object = level.plant_systems[level.plant_system_index].plants.pop()
        if level.current_asset_group == 'grass':
            if  len(level.grass_systems[level.grass_system_index].tiles) > 0:
                last_object = level.grass_systems[level.grass_system_index].tiles.pop()
        if level.current_asset_group == 'particle_system':
            if len(level.particle_systems) > 0:
                last_object = level.particle_systems[level.particle_system_index].pop()


    if level.current_asset_group == 'colliding_objects':
        level.current_asset = None
        if level.current_action == 'place':
            nearest_object = min(level.objects + level.vehicles, key=lambda obj: (level.place_position[0] - obj.position[0])**2 + (level.place_position[1] - obj.position[1])**2 + (level.place_position[2] - obj.position[2])**2)
            if nearest_object.collidable:
                nearest_object.collidable = False
                nearest_object.hitbox.show_hitbox = False
            else:
                nearest_object.collidable = True
                nearest_object.hitbox.show_hitbox = True


    if level.current_asset_group == 'moving_objects':
        level.current_asset = None
        if level.current_action == 'place':
            nearest_object = min(level.objects + level.vehicles, key=lambda obj: (level.place_position[0] - obj.position[0])**2 + (level.place_position[1] - obj.position[1])**2 + (level.place_position[2] - obj.position[2])**2)
            if nearest_object.movelocked:
                nearest_object.movelocked = False
            else:
                nearest_object.movelocked = True









class Level:
    def __init__(self, game, name, map_size, background=None, fill_colour=(0, 0, 0)):

        self.game = game

        self.name = name

        if background:
            self.background = pygame.image.load(background).convert_alpha()
        else:
            self.background = None

        """ LEVEL EDITING PARAMETERS """
        self.place_position = [0, 0, 0]

        self.current_asset = None
        self.current_asset_index = 0
        self.current_asset_rotation = 0
        self.plant_system_index = 0
        self.grass_system_index = 0
        self.particle_system_index = 0

        self.current_asset_group = 'object'
        self.current_action = None

        self.undo = False
        self.save = False
        self.load = False

        self.play = False

        self.stairs = [
            # Stairs(asset=self.game.stair_asset, asset_index=1, position=[map_size[0]//2, map_size[1]//2, 0], rotation=0),
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
        self.texture_assets = []
        self.object_assets = []
        self.vehicle_assets = []
        self.particle_system_assets = []
        self.npc_assets = []

        self.loadpoint_levels = []

        """ GAME OBJECTS """
        self.textures = []
        self.objects = []
        self.vehicles = []
        self.plant_systems = []
        self.grass_systems = []
        self.particle_systems = []

        self.loadpoints = []

        self.colliding_objects_moving = []
        self.colliding_objects_movelocked = []

        """ CONFIGURING PLAYER OBJECT """
        self.player_asset = self.game.player_asset
        player_start_position = [self.map_size[0]//2, self.map_size[1]//2, 0]
        player_start_rotation = 0
        self.player = Character(asset=self.player_asset, asset_index=0, position=player_start_position, rotation=player_start_rotation)
        self.player.mass = 70
        self.player.movelocked = False
        self.player.collidable = True


        self.fill_colour = fill_colour

        self.rotation_speed = 1
        self.scroll_speed = 0.1

        """ TOPOLOGICAL DEPTH SORTING SETTINGS """
        self.depth_sort_period = 5
        self.depth_sort_timer = 0
        self.depth_sorted_objects = []


    def handle_controls_editing(self, keys):

        self.current_action = None

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

        for event in self.game.events:

            """ KEY PRESSES """
            if event.type == pygame.KEYDOWN:

                # UNDO
                if ctrl_pressed and event.key == pygame.K_z:
                    self.current_action = 'undo'

                # SWITCH BETWEEN DIFFERENT ASSET TYPES
                elif event.key == pygame.K_1:
                    self.current_asset_group = 'texture'
                    self.current_asset_index = 0

                elif event.key == pygame.K_2:
                    self.current_asset_group = 'object'
                    self.current_asset_index = 0

                elif event.key == pygame.K_3:
                    self.current_asset_group = 'vehicle'
                    self.current_asset_index = 0

                elif event.key == pygame.K_4:
                    self.current_asset_group = 'plant'
                    self.current_asset_index = 0

                elif event.key == pygame.K_5:
                    self.current_asset_group = 'grass'
                    self.current_asset_index = 0

                elif event.key == pygame.K_6:
                    self.current_asset_group = 'particle_system'
                    self.current_asset_index = 0

                elif event.key == pygame.K_7:
                    self.current_asset_group = 'loadpoint'
                    self.current_asset_index = 0

                elif event.key == pygame.K_c :
                    self.current_asset_group = 'colliding_objects'

                elif event.key == pygame.K_m :
                    self.current_asset_group = 'moving_objects'

                elif event.key == pygame.K_RETURN :
                    if not self.play:
                        self.play = True
                    else:
                        self.play = False

                # SAVING AND LOADING LEVEL FROM FILE
                elif ctrl_pressed and event.key == pygame.K_s:
                    self.save = True
                elif ctrl_pressed and event.key == pygame.K_l:
                    self.load = True

            """ MOUSE CLICKS """
            # PLACE OBJECT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.current_action = 'place'

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
                            self.place_position[2] += 16
                        elif event.y == 1:
                            self.place_position[2] -= 16

            # ROTATE ASSET / CYCLE SYSTEM
            if keys[pygame.K_LSHIFT]:
                if event.type == pygame.MOUSEWHEEL:
                    if event.y == -1:
                        self.current_action = 'rotate_clockwise_or_next_system'
                    elif event.y == 1:
                        self.current_action = 'rotate_counterclockwise_or_prev_system'

            # CYCLE CURRENT SYSTEM ASSETS 
            if not ( keys[pygame.K_LCTRL] or keys[pygame.K_LSHIFT] or keys[pygame.K_z]):
                if event.type == pygame.MOUSEWHEEL:
                    if event.y == 1:
                        self.current_action = 'next_item'
                    elif event.y == -1:
                        self.current_action = 'prev_item'

        control_editing(self)


    def edit_level(self):

        """ SAVING AND LOADING LEVEL """
        if self.save:
            self.save_level()
        if self.load:
                self.load_level()


    def save_level(self):
        level_data = {}

        # SAVING TEXTURES
        objects_data = []
        for obj in self.textures:
            object_data = obj.get_data()
            objects_data.append(object_data)
        level_data['textures_data'] = objects_data

        # SAVING OBJECTS
        objects_data = []
        for obj in self.objects:
            object_data = obj.get_data()
            objects_data.append(object_data)
        level_data['objects_data'] = objects_data

        # SAVING GRASS SYSTEMS DATA
        grass_systems_data = []
        for grass_system in self.grass_systems:
            grass_system_data = grass_system.get_data()
            grass_systems_data.append(grass_system_data)
        level_data['grass_systems_data'] = grass_systems_data

        # SAVING PLANT SYSTEMS DATA
        plant_systems_data = []
        for plant_system in self.plant_systems:
            plant_system_data = plant_system.get_data()
            plant_systems_data.append(plant_system_data)
        level_data['plant_systems_data'] = plant_systems_data

        # SAVING PARTICLE SYSTEMS DATA
        particle_systems_data = []
        for particle_system in self.particle_systems:
            particle_system_data = particle_system.get_data()
            particle_systems_data.append(particle_system_data)
        level_data['particle_systems_data'] = particle_systems_data

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
                for object_data in data['textures_data']:
                    object_position = object_data['position']
                    object_rotation = object_data['rotation']
                    asset_index = object_data['asset_index']
                    object_asset = self.texture_assets[asset_index]
                    self.textures.append(SpritestackModel(
                        object_asset,
                        asset_index,
                        object_position,
                        object_rotation
                    ))

                # LOADING OBJECTS DATA
                self.objects = []
                for object_data in data['objects_data']:
                    object_position = object_data['position']
                    object_rotation = object_data['rotation']
                    asset_index = object_data['asset_index']
                    object_asset = self.object_assets[asset_index]
                    self.objects.append(DynamicObject(
                        object_asset,
                        asset_index,
                        object_position,
                        object_rotation
                    ))

                # LOADING GRASS SYSTEM DATA
                for grass_system_index in range(len(self.grass_systems)):
                    self.grass_systems[grass_system_index].load(data['grass_systems_data'][grass_system_index])

                # LOADING PLANT SYSTEM DATA
                for plant_system_index in range(len(self.plant_systems)):
                    self.plant_systems[plant_system_index].load(data['plant_systems_data'][plant_system_index])

                # LOADING PARTICLE SYSTEM DATA
                self.particle_systems = []
                for particle_system_data in data['particle_systems_data']:
                    particle_system_position = particle_system_data['position']
                    particle_system_asset = self.particle_system_assets[particle_system_data['asset_index']]
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
        place_position_z = self.place_position[2]

        """ SNAPPING TO NON-ROTATING GRID """
        place_position_x = 16 * round(place_position_x/16)
        place_position_y = 16 * round(place_position_y/16)
        place_position_z = 16 * round(place_position_z/16)
        self.place_position = [place_position_x, place_position_y, place_position_z]   

        """ CAMERA MOVEMENT"""
        if self.player.vehicle:
            move_vector = [self.player.vehicle.vx / (self.player.vehicle.max_speed/3), self.player.vehicle.vy / (self.player.vehicle.max_speed/3)]
        else:
            move_vector = [self.player.vx / self.player.run_speed_limit, self.player.vy / self.player.run_speed_limit]
        camera_follow_position_movement_offset = (
            self.player.position[0] + self.render_width / 4 * move_vector[0],
            self.player.position[1] - self.render_height / 4 * move_vector[1]
            )
        self.camera.follow(camera_follow_position_movement_offset)
        self.camera.move()

        """ UPDATING PLAYER AND ALL PLAYER-LINKED OBJECTS """
        self.player.update(self.camera)

        """ HANDLING VEHICLE DRIVING """
        if self.play:
            for vehicle in self.vehicles:
                vehicle.handle_driver(self.player)




        """ HANDLING DYNAMIC OBJECT COLLISION """
        collidable_objects_moving = []
        collidable_objects_movelocked = []
        for obj in self.objects + self.vehicles + self.player.projectiles + [self.player]:
            if obj.collidable and obj.movelocked:
                collidable_objects_movelocked.append(obj)
            elif obj.collidable and not obj.movelocked:
                collidable_objects_moving.append(obj)

        EPS = 5
        for moving_object in collidable_objects_moving:
            if sqrt(moving_object.vx**2 + moving_object.vy**2) > EPS:
                moving_object.hitbox.update()

        all_collidable_objects = collidable_objects_moving + collidable_objects_movelocked
        
        for collidable_object in all_collidable_objects:
            collidable_object.hitbox.collided = False

        for object_1, object_2 in combinations(all_collidable_objects, 2):
                
                if object_1.movelocked:
                    object_1.hitbox.colour = (255, 0, 0)
                else:
                    object_1.hitbox.colour = (0, 255, 0)

                if object_2.movelocked:
                    object_2.hitbox.colour = (255, 0, 0)
                else:
                    object_2.hitbox.colour = (0, 255, 0)

                if not (object_1.movelocked and object_2.movelocked) and (object_1.collidable and object_2.collidable):

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
                                                object_1.hitbox.resolve_collision(object_2, mtv_axis, overlap)

        for obj in collidable_objects_movelocked:
            if obj.hitbox.collided:
                obj.hitbox.colour = (255, 255, 0)
            else:
                if obj.movelocked == True:
                    obj.hitbox.colour = (255, 0, 0)

        for obj in collidable_objects_moving:
            if obj.hitbox.collided:
                obj.hitbox.colour = (255, 255, 0)
            else:
                if obj.movelocked == True:
                    obj.hitbox.colour = (0, 255, 0)


        """ HANDLING OBJECT MOVEMENT """
        for moving_object in collidable_objects_moving:
            moving_object.move()


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
        # GETTING A LIST OF PARTICLE SYSTEMS BELONGING TO PROJECTILES
        projectiles = []
        for projectile in self.player.projectiles:
            projectiles.append(projectile.particle_system)

        render_objects = self.stairs + [self.player] + projectiles + self.textures + self.vehicles + self.objects + plants + grass_tiles + self.particle_systems + self.loadpoints

        # CONTROLLING TOPOLOGICAL DEPTH SORTING
        if self.depth_sort_timer > self.depth_sort_period:
            self.depth_sort_timer = 0
        if self.depth_sort_timer == 0:
            # GETTING VISIBLE OBJECTS
            visible_objects = get_visible_objects(render_surface, self.camera, render_objects)
            # SORTING VISIBLE OBJECTS BY THEIR Z COORDINATE
            visible_objects.sort(key=lambda obj: obj.position[2])
            # PERFORMING TOPOLOGICAL DEPTH SORTING OF OBJECTS
            self.depth_sorted_objects = depth_sort(visible_objects, self.camera)
        self.depth_sort_timer += 1

        # RENDERING DEPTH SORTED OBJECTS
        if self.current_asset and not self.play:
            sorted_objects = self.depth_sorted_objects + [self.current_asset]
        else:
            sorted_objects = self.depth_sorted_objects

        global_render(
            screen=render_surface,
            camera=self.camera,
            sorted_objects=sorted_objects,
            bend_objects=[self.player] + self.vehicles, #self.dynamic_sprite_stack_objects + [self.player] + self.vehicles,
            map_size=self.map_size,
            background=self.background
        )

        for grass_system in self.grass_systems:
            grass_system.apply_wind()

        upscaled_surface = pygame.transform.scale(render_surface, (self.game.screen_width, self.game.screen_height))
        self.game.screen.blit(upscaled_surface, (0, 0))


        display_fps(self.game.screen, self.game.clock, font)

        display_place_info(self.game.screen, font, self.place_position, self.current_asset_rotation, self.current_asset_group, self.play)
