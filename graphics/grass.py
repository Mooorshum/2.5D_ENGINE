import pygame
import os
import random
from math import sqrt, sin, cos, pi, radians, exp
from numpy import sign


WHITE = (255, 255, 255)

class GrassBlade:
    def __init__(self, image, position):
        self.image = image
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


class GrassTile:
    def __init__(self, size, position, folder, blades_per_tile, stiffness, relax_speed, wind_magnitude, num_states, scale_factor):
        self.size = size
        self.position = position
        self.stiffness = stiffness
        self.blades_per_tile = blades_per_tile
        self.scale_factor = scale_factor
        self.wind_magnitude = wind_magnitude
        
        self.relax_speed = relax_speed
        self.num_states = num_states
        
        self.max_angle = 70 # maximum possible inclination

        self.phase_shift = 0

        self.relaxed = True
        self.tile_uniform_rotation = 0

        self.y0_offset = size/4

        # Loading individual grass blade images
        self.blade_asset_images = self.get_blade_asset_images(folder)
        
        # Storing the blades that belong to this particular tile
        self.grass_blades = []
        self.populate_tile() # Generating blades for a newly created tile
        self.grass_blades.sort(key=lambda blade: blade.position[1]) # sorting blades to give an illusion of depth

        # Rendering and caching tile images for different rotation values
        self.tile_image_rotation_value = self.map_tile_images_to_rotation()
        


    def populate_tile(self):
        k = 0
        # Randomly generate grass blades to fill the tile
        x_start, y_start = self.position[0] - self.size // 2, self.position[1] - self.size // 2
        x_end, y_end = self.position[0] + self.size // 2, self.position[1] + self.size // 2
        while k < self.blades_per_tile:
            i = random.randint(x_start, x_end)
            j = random.randint(y_start, y_end)
            if k == 0:
                self.generate_blade((i, j))
                k += 1
            elif all((i, j) != blade.position for blade in self.grass_blades):
                self.generate_blade((i, j))
                k += 1

    def get_blade_asset_images(self, folder):
        blade_asset_images = []
        for image in sorted(os.listdir(folder)):
            blade_image = pygame.image.load(f'{folder}/{image}').convert()
            if self.scale_factor != 1:
                scale_factor = (blade_image.get_width()*self.scale_factor, blade_image.get_height()*self.scale_factor)
                blade_image = pygame.transform.scale(blade_image, scale_factor)
            blade_image.set_colorkey((0, 0, 0))
            blade_asset_images.append(blade_image)
        return blade_asset_images

    def map_tile_images_to_rotation(self):
        padding = int(self.size * 2 * self.scale_factor + 30)
        image_rotation = {}
        tile_size = (self.size + padding, self.size + padding)
        for i in range(self.num_states):
            # Create a blank surface for the tile image
            tile_image = pygame.Surface(tile_size, pygame.SRCALPHA)
            # Calculate the rotation angle for this state
            rotation = int(-self.wind_magnitude + 2 * self.wind_magnitude / (self.num_states - 1) * i)
            for blade in self.grass_blades:
                relative_position = (
                    (self.size + padding)//2 - (self.position[0] - blade.position[0]),
                    (self.size + padding)//2 - (self.position[1] - blade.position[1])
                )
                blade.rotation = rotation
                blade.render_blade(tile_image, rotation, relative_position)
            image_rotation[rotation] = tile_image
        return image_rotation

    def render_tile_simple(self, screen, offset=[0, 0]):
        closest_mapped_angle = self.get_closest_mapped_angle()
        tile_image = self.tile_image_rotation_value[closest_mapped_angle]
        # draw the whole tile as a single image
        screen.blit(
            tile_image,
            (self.position[0] - tile_image.get_width()//2 + offset[0],
             self.position[1] - tile_image.get_height()//2 + offset[1],
            )
        )

    def render_tile_detailed(self, screen, bendpoints, offset=[0, 0]):
        threshold = 0.2
        for blade in self.grass_blades:
            for bendpoint in bendpoints:
                distance_to_blade = sqrt((blade.position[0] - bendpoint[0])**2 + (blade.position[1] - bendpoint[1])**2)
                distance_factor = exp(-distance_to_blade/self.size)
                if distance_factor > threshold:
                    direction = sign(blade.position[0] - bendpoint[0])
                    blade.rotation -= distance_factor * direction / self.stiffness

            if abs(blade.rotation) > self.max_angle:
                blade.rotation = sign(blade.rotation) * self.max_angle
            blade.render_blade(screen, blade.rotation, blade.position, offset)

    def relax(self):
        relaxed = True
        eps_angle = 10
        for blade in self.grass_blades:
                diff_angle = self.tile_uniform_rotation - blade.rotation
                if abs(diff_angle) > eps_angle:
                    blade.rotation += sign(diff_angle) * self.relax_speed
                    relaxed = False
        if relaxed:
            self.relaxed = True

    def render(self, screen, bend_objects, offset=[0, 0]):
        bendpoints = []
        for bend_object in bend_objects:
            bendpoint = (bend_object.position[0], bend_object.position[1])
            bendpoints.append(bendpoint)
        
        for bendpoint in bendpoints:
            dist = sqrt((bendpoint[0] - self.position[0])**2 + (bendpoint[1] - self.position[1])**2)
            if dist < (bend_object.hitbox_size[1]):
                self.relaxed = False

        # If the tile has been bent, and has not yet returned to a cached state
        if self.relaxed:
            self.render_tile_simple(screen, offset)
        else:
            self.render_tile_detailed(screen, bendpoints, offset)
            self.relax()

        

    def generate_blade(self, position):
        if all(position != blade.position for blade in self.grass_blades):
            new_blade_image = random.choice(self.blade_asset_images)
            new_blade = GrassBlade(new_blade_image, position)
            self.grass_blades.append(new_blade)

    def get_closest_mapped_angle(self):
        # Find the value closest to self.tile_uniform_rotation from
        # the list of mapped rotations tile_image_rotation_value.keys
        return min(
            self.tile_image_rotation_value.keys(),
            key=lambda x:abs(x-self.tile_uniform_rotation)
        )


class GrassSystem:
    def __init__(self, folder, tile_size=100, blades_per_tile=20, scale=1, density=1, stiffness=0.01):
        self.tile_size = tile_size
        self.blades_per_tile = blades_per_tile
        self.scale_factor = scale
        self.stiffness = stiffness

        self.relax_speed = 0.5
        self.tiles_num_states = 11
        self.wind_magnitude = 8
        self.wind_direction = 0.05

        self.tiles = []
        self.bendpoints = []

        self.mask = 'test_mask.png'

        self.create_grass(folder, density)
        self.sort_tiles()


    def create_grass(self, folder, density):
        mask = pygame.image.load(f'{folder}/masks/{self.mask}').convert()
        mask_width = mask.get_width()
        mask_height = mask.get_height()
        for x in range(0, mask_width, self.tile_size):
            for y in range(0, mask_height, self.tile_size):
                colour = mask.get_at((x, y))
                if colour != WHITE:
                    rand_num = random.uniform(0, 1)
                    if rand_num < density:
                        position = (x, y)
                        self.create_new_tile(position, f'{folder}/images')


    def create_new_tile(self, position, images_folder):
        if all(position != tile.position for tile in self.tiles):
            tile = GrassTile(
                self.tile_size, position, images_folder,
                self.blades_per_tile, self.stiffness, self.relax_speed,
                self.wind_magnitude,
                self.tiles_num_states, self.scale_factor
            )
            self.tiles.append(tile)

    def sort_tiles(self):
        self.tiles.sort(key=lambda tile: tile.position[1])


    def apply_wind(self, omega, t):
        wind_direction = radians(self.wind_direction)
        for tile in self.tiles:
            wind_offset = (tile.position[0] * cos(wind_direction) +
                      tile.position[1] * sin(wind_direction))
            phase_shift = self.wind_magnitude * wind_offset
            tile.phase_shift = phase_shift
            tilted_angle = self.wind_magnitude * sin(omega * t + phase_shift)
            tile.tile_uniform_rotation = tilted_angle
