import pygame

import copy

import os
import random
from math import sqrt, sin, cos, pi, radians, exp
from numpy import sign




class GrassBlade:
    def __init__(self, image, position):
        self.image = image
        self.image_path = None
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.position = position
        self.max_shade_amount = 150
        self.rotation = 0

    def render_blade(self, surf, rotation, position, offset=[0, 0]):
        rotation_rads = radians(self.rotation)
        rotated_image = pygame.transform.rotate(self.image, rotation)
        shade = pygame.Surface(rotated_image.get_size())
        shade_amount = min(int(self.max_shade_amount * (abs(rotation) / 90)), self.max_shade_amount)
        shade.set_alpha(shade_amount)
        rotated_image.blit(shade, (0, 0))
        position = (
            position[0] - rotated_image.get_width() // 2 - self.image_width*sin(rotation_rads) + offset[0],
            position[1] - rotated_image.get_height()//2 - self.image_width*cos(rotation_rads) + offset[1]
        )
        surf.blit(rotated_image, position)




class GrassTileAsset:
    def __init__(self, index, size, grass_folder, num_blades, stiffness, relax_speed, wind_magnitude, num_states, scale):
        self.index = index
        self.size = size
        self.stiffness = stiffness
        self.relax_speed = relax_speed
        self.num_blades = num_blades
        self.wind_magnitude = wind_magnitude
        self.num_states = num_states
        self.scale = scale
        self.max_angle = 70 # maximum possible inclination

        self.y0_offset = -size / 4
        
        self.grass_blades = []
        self.tile_image_rotation_value = {}

        # Getting individual grass blade images
        self.blade_asset_images, self.blade_asset_image_paths = self.get_blade_asset_images_and_paths(f'{grass_folder}/blade_images')

        # Generating blades for a newly created asset
        self.populate_tile()

        # Rendering and caching asset images for different rotation values
        self.map_tile_images_to_rotation(num_states, wind_magnitude)


    def get_blade_asset_images_and_paths(self, folder):
        blade_asset_images = []
        blade_asset_image_paths = []
        for image in sorted(os.listdir(folder)):
            blade_image = pygame.image.load(f'{folder}/{image}').convert()
            if self.scale != 1:
                scale = (blade_image.get_width()*self.scale, blade_image.get_height()*self.scale)
                blade_image = pygame.transform.scale(blade_image, scale)
            blade_image.set_colorkey((0, 0, 0))
            blade_asset_images.append(blade_image)
            blade_asset_image_paths.append(f'{folder}/{image}')
        return blade_asset_images, blade_asset_image_paths


    def populate_tile(self):
        k = 0
        # Randomly generate grass blades to fill the tile
        x_start, y_start =  -self.size * self.scale // 2, - self.size * self.scale // 2
        x_end, y_end = self.size * self.scale // 2, self.size * self.scale // 2
        while k < self.num_blades:
            i = random.randint(x_start, x_end)
            j = random.randint(y_start, y_end)
            if k == 0:
                self.generate_blade([i, j])
                k += 1
            elif all((i, j) != blade.position for blade in self.grass_blades):
                self.generate_blade([i, j])
                k += 1
        self.grass_blades.sort(key=lambda blade: blade.position[1]) # sorting blades to give an illusion of depth


    def generate_blade(self, position):
        if all(position != blade.position for blade in self.grass_blades):
            new_blade_image_id = random.randint(0, len(self.blade_asset_images)-1)
            new_blade_image = self.blade_asset_images[new_blade_image_id]
            new_blade = GrassBlade(new_blade_image, position)
            new_blade.image_path = self.blade_asset_image_paths[new_blade_image_id]
            self.grass_blades.append(new_blade)


    def map_tile_images_to_rotation(self, num_states, wind_magnitude):
        padding = int(self.size * self.scale * 2 + 30)
        image_rotation = {}
        tile_size = (self.size * self.scale + padding, self.size * self.scale + padding)
        for i in range(num_states):
            # Create a blank surface for the tile image
            tile_image = pygame.Surface(tile_size, pygame.SRCALPHA)
            # Calculate the rotation angle for this state
            rotation = int(-wind_magnitude + 2 * wind_magnitude / (num_states - 1) * i)
            for blade in self.grass_blades:
                relative_position = (
                    (self.size * self.scale + padding)//2 + blade.position[0],
                    (self.size * self.scale + padding)//2 + blade.position[1]
                )
                blade.rotation = rotation
                blade.render_blade(tile_image, rotation, relative_position)
            image_rotation[rotation] = tile_image
        self.tile_image_rotation_value = image_rotation


    def get_data(self):
        data = {}
        data['index'] = self.index 
        data['size'] = self.size
        data['stiffness'] = self.stiffness
        data['relax_speed'] = self.relax_speed
        data['num_blades'] = self.num_blades
        data['wind_magnitude'] = self.wind_magnitude
        data['num_states'] = self.num_states
        data['scale'] = self.scale

        data['blade_positions'] = []
        data['blade_image_paths'] = []

        data['blade_image_indices'] = [
            self.blade_asset_image_paths.index(blade.image_path) 
            for blade in self.grass_blades
        ]

        data['blade_positions'] = [
            blade.position
            for blade in self.grass_blades
        ]

        data['blade_image_paths'] = [
            blade.image_path
            for blade in self.grass_blades
        ]

        return data
    
    def load(self, data):
        self.grass_blades = []
        self.index = data['index']
        self.size = data['size']
        self.stiffness = data['stiffness']
        self.relax_speed = data['relax_speed']
        self.num_blades = data['num_blades']
        self.wind_magnitude = data['wind_magnitude']
        self.num_states = data['num_states']
        self.scale = data['scale']
        for blade_index in range(len(data['blade_positions'])):
            blade_position = data['blade_positions'][blade_index]
            blade_image_path = data['blade_image_paths'][blade_index]
            blade_image = pygame.image.load(blade_image_path).convert()
            if self.scale != 1:
                scale = (blade_image.get_width()*self.scale, blade_image.get_height()*self.scale)
                blade_image = pygame.transform.scale(blade_image, scale)
            blade_image.set_colorkey((0, 0, 0))
            blade = GrassBlade(blade_image, blade_position)
            blade.image_path = blade_image_path
            self.grass_blades.append(blade)
        self.map_tile_images_to_rotation(self.num_states, self.wind_magnitude)
        




class GrassTile:
    def __init__(self, position, asset):
        self.asset = asset
        self.position = position

        self.y0_offset = self.asset.y0_offset

        self.phase_shift = 0

        self.relaxed = True
        self.tile_uniform_rotation = 0

        self.grass_blades = [
            GrassBlade(copy.deepcopy(blade.image), copy.deepcopy(blade.position))
            for blade in self.asset.grass_blades
        ]


    def render_tile_simple(self, screen, offset=[0, 0]):
        closest_mapped_angle = self.get_closest_mapped_angle()
        tile_image = self.asset.tile_image_rotation_value[closest_mapped_angle]
        screen.blit(
            tile_image,
            (self.position[0] - tile_image.get_width()//2 + offset[0],
             self.position[1] - tile_image.get_height()//2 + offset[1],
            )
        )


    def get_closest_mapped_angle(self):
        # Find the value closest to self.tile_uniform_rotation from
        # the list of mapped rotations tile_image_rotation_value.keys
        return min(
            self.asset.tile_image_rotation_value.keys(),
            key=lambda x:abs(x-self.tile_uniform_rotation)
        )


    def render_tile_detailed(self, screen, bend_objects, bend_effect_radius, offset=[0, 0]):   
        for blade in self.grass_blades:
            blade_position_on_tile = (blade.position[0] + self.position[0], blade.position[1] + self.position[1])
            for bend_object in bend_objects:
                if not bend_object.movelocked:
                    object_distance_to_blade = sqrt((blade_position_on_tile[0] - bend_object.position[0])**2 + (blade_position_on_tile[1] - bend_object.position[1])**2)
                    
                    if object_distance_to_blade < bend_effect_radius:
                        object_distance_factor = abs(object_distance_to_blade / bend_effect_radius)
                        direction = sign(blade_position_on_tile[0] - bend_object.position[0])
                        blade.rotation -= object_distance_factor * direction / self.asset.stiffness


            if abs(blade.rotation) > self.asset.max_angle:
                blade.rotation = sign(blade.rotation) * self.asset.max_angle
            blade.render_blade(
                screen,
                blade.rotation,
                (blade_position_on_tile[0], blade_position_on_tile[1]),
                offset)


    def relax(self):
        relaxed = True
        eps_angle = 10
        for blade in self.grass_blades:
                diff_angle = self.tile_uniform_rotation - blade.rotation
                if abs(diff_angle) > eps_angle:
                    blade.rotation += sign(diff_angle) * self.asset.relax_speed
                    relaxed = False
        if relaxed:
            self.relaxed = True


    def render(self, screen, bend_objects, offset=[0, 0]):
        bend_effect_padding = 0
        for bend_object in bend_objects:
            if not bend_object.movelocked:
                dist = sqrt((bend_object.position[0] - self.position[0])**2 + (bend_object.position[1] - self.position[1])**2)
                bend_effect_radius = sqrt(bend_object.hitbox.size[0]**2 + bend_object.hitbox.size[1]**2) / 2 + bend_effect_padding
                if dist < bend_effect_radius:
                    self.relaxed = False

        # If the tile has been bent, and has not yet returned to a cached state
        if self.relaxed:
            self.render_tile_simple(screen, offset)
        else:
            self.render_tile_detailed(screen, bend_objects, bend_effect_radius, offset)
            self.relax()


    def get_data(self):
        data = {}
        data['position'] = self.position
        data['asset_index'] = self.asset.index
        return data
    
    def load(self, data, asset):
        self.position = data['position']
        self.asset = asset




class GrassSystem:
    def __init__(
            self,
            folder,
            min_tile_size=10, max_tile_size=100,
            min_num_blades=5, max_num_blades=10,
            stiffness=0.01, relax_speed=1, 
            num_assets=10,
            wind_omega=1/20,
            scale=1
        ):

        self.folder = folder
        
        self.min_tile_size = min_tile_size
        self.max_tile_size = max_tile_size
        self.min_num_blades = min_num_blades
        self.max_num_blades = max_num_blades
        self.stiffness = stiffness

        self.relax_speed = relax_speed
        self.tiles_num_states = 11
        self.wind_magnitude = 8
        self.wind_direction = 0.05

        self.wind_omega = wind_omega
        self.internal_time = 0

        self.asset_scale = scale
        
        self.assets = self.generate_assets(self.folder, num_assets)

        self.tiles = []
        self.bendpoints = []

        self.sort_tiles()


    def generate_assets(self, grass_folder, num_assets):
        assets = []
        for asset_index in range(num_assets):
            tile_size = random.randint(self.min_tile_size, self.max_tile_size)
            num_blades = random.randint(self.min_num_blades, self.max_num_blades)
            asset = GrassTileAsset(
                asset_index,
                tile_size,
                grass_folder,
                num_blades,
                self.stiffness,
                self.relax_speed,
                self.wind_magnitude,
                self.tiles_num_states,
                self.asset_scale
            )
            assets.append(asset)
        """ assets = sorted(assets, key=lambda asset: asset.num_blades) """
        return assets


    def create_tile(self, asset_index, position):
        asset = self.assets[asset_index]
        grass_tile = GrassTile(position, asset)
        self.tiles.append(grass_tile)


    def sort_tiles(self):
        self.tiles.sort(key=lambda tile: tile.position[1])


    def apply_wind(self):
        wind_direction = radians(self.wind_direction)
        for tile in self.tiles:
            wind_offset = (tile.position[0] * cos(wind_direction) +
                      tile.position[1] * sin(wind_direction))
            phase_shift = self.wind_magnitude * wind_offset
            tile.phase_shift = phase_shift
            tilted_angle = self.wind_magnitude * sin(self.wind_omega * self.internal_time + phase_shift)
            tile.tile_uniform_rotation = tilted_angle
        self.internal_time += 1


    def get_data(self):
        system_data = {}

        # GETTING ASSET DATA
        system_asset_data = []
        for asset in self.assets:
            system_asset_data.append(asset.get_data())
        system_data['assets'] = system_asset_data

        # GETTING GRASS TILES DATA
        system_tiles_data = []
        for tile in self.tiles:
            system_tiles_data.append(tile.get_data())
        system_data['tiles'] = system_tiles_data

        # GENERAL SYSTEM INFO
        system_data['grass_folder'] = self.folder

        return system_data
    
    def load(self, system_data):

        # LOADING ASSETS
        self.assets = []
        for asset_data in system_data['assets']:
            asset = GrassTileAsset(
                asset_data['index'],
                asset_data['size'],
                system_data['grass_folder'],
                asset_data['num_blades'],
                asset_data['stiffness'],
                asset_data['relax_speed'],
                asset_data['wind_magnitude'],
                asset_data['num_states'],
                asset_data['scale']
            )
            asset.load(asset_data)
            """ asset.map_tile_images_to_rotation(asset_data['num_states'], asset_data['wind_magnitude']) """
            self.assets.append(asset)

        # LOADING TILES
        self.tiles = []
        for tile_data in system_data['tiles']:
            self.create_tile(tile_data['asset_index'], tile_data['position'])

            