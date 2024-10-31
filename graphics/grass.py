import pygame
import os
import random
from math import sqrt, sin, pi
from numpy import sign

class GrassBlade:
    def __init__(self, image, position):
        self.image = image
        self.position = position
        self.max_shade_amount = 100
        self.rotation = 0

    def render_blade(self, surf, rotation, offset=(0,0)):
        rotated_image = pygame.transform.rotate(self.image, rotation)
        shade = pygame.Surface(rotated_image.get_size())
        shade_amount = min(int(self.max_shade_amount * (abs(rotation) / 90)), self.max_shade_amount)
        shade.set_alpha(shade_amount)
        rotated_image.blit(shade, (0, 0))
        surf.blit(
            rotated_image,
            (
                self.position[0] - rotated_image.get_width() // 2 - offset[0],
                self.position[1] - rotated_image.get_height() // 2 - offset[1]
            )
        )




class GrassTile:
    def __init__(self, size, position, folder, density, stiffness, cutoff_distance, relax_speed, num_states, scale_factor):
        self.size = size
        self.position = position
        self.stiffness = stiffness
        self.bend_cutoff_distance = cutoff_distance
        self.density = density
        self.scale_factor = scale_factor
        
        self.relax_speed = relax_speed
        self.num_states = num_states
        
        self.max_angle = 89 # maximum possible inclination

        self.phase_shift = sin((self.position[0]) * 3)

        self.relaxed = True
        self.tile_uniform_rotation = 0

        # Loading individual grass blade images
        self.blade_asset_images = self.get_blade_asset_images(folder)
        
        # Storing the blades that belong to this particular tile
        self.grass_blades = []
        self.populate_tile() # Generating blades for a newly created tile
        self.grass_blades.sort(key=lambda blade: blade.position[1]) # sorting blades to give an illusion of depth

        # Rendering and caching tile images for different rotation values
        self.tile_image_rotation_value = self.map_tile_images_to_rotation()
        

    def populate_tile(self):
        # Randomly generate grass blades to fill the tile
        x_start, y_start = self.position[0] - self.size // 2, self.position[1] - self.size // 2
        x_end, y_end = self.position[0] + self.size // 2, self.position[1] + self.size // 2
        for i in range(x_start, x_end):
            for j in range(y_start, y_end):
                # Determine whether to place a blade based on the density
                if random.uniform(0, 1) < self.density:
                    self.generate_blade((i, j))

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
        padding = self.size*2*self.scale_factor
        offset = (self.position[0] - self.size//2 - padding//2, self.position[1] - self.size//2 - padding//2)
        image_rotation = {}
        tile_size = (self.size + padding, self.size + padding)
        for i in range(self.num_states):
            # Create a blank surface for the tile image
            tile_image = pygame.Surface(tile_size, pygame.SRCALPHA)
            rotation = int(-self.max_angle + 2*self.max_angle / (self.num_states - 1) * i)  # Compute rotation value
            # Blit each blade onto the tile image at the specified rotation
            for blade in self.grass_blades:
                blade.render_blade(tile_image, rotation, offset)
            # Add the tile image to the dictionary with the rotation as the key
            image_rotation[rotation] = tile_image
        return image_rotation

    def render_tile_simple(self, screen):
        closest_mapped_angle = self.get_closest_mapped_angle()
        tile_image = self.tile_image_rotation_value[closest_mapped_angle]
        # draw the whole tile as a single image
        screen.blit(
            tile_image,
            (self.position[0] - tile_image.get_width()//2,
             self.position[1] - tile_image.get_height()//2,
            )
        )

    def render_tile_detailed(self, screen, bend_force_position):
        for blade in self.grass_blades:
            distance_to_blade = sqrt((blade.position[0] - bend_force_position[0])**2 + (blade.position[1] - bend_force_position[1])**2)
            distance_factor = max(0, (1 - distance_to_blade/self.bend_cutoff_distance))
            direction = sign(blade.position[0] - bend_force_position[0])
            blade.rotation -= distance_factor * direction / self.stiffness
            if abs(blade.rotation) > self.max_angle:
                blade.rotation = sign(blade.rotation) * self.max_angle
            blade.render_blade(screen, blade.rotation)

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

    def handle_tile_rendering_and_state(self, screen, bend_force_position):
        # If the tile has been bent, and has not yet returned to a cached state
        if self.relaxed:
            self.render_tile_simple(screen)
        else:
            self.render_tile_detailed(screen, bend_force_position)
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
    def __init__(self):
        self.stiffness = 0.01
        self.cutoff_distance = 80
        self.tile_size = 100
        self.density = 0.007
        self.relax_speed = 5
        self.tiles_num_states = 200
        self.scale_factor = 1.5

        self.tiles = []
        self.bendpoints = []

    def create_new_tile(self, position, folder):
        # If a tile does not already exist at the position
        if all(position != tile.position for tile in self.tiles):
            # Initialize a new GrassTile instance at the given position
            tile = GrassTile(
                self.tile_size, position, folder,
               self.density, self.stiffness, self.cutoff_distance, self.relax_speed,
               self.tiles_num_states, self.scale_factor
            )
            # Add the populated tile to the list of tiles in the system
            self.tiles.append(tile)

    def sort_tiles(self):
        self.tiles.sort(key=lambda tile: tile.position[1])

    def render_grass_tiles(self, screen, bendpoints):
        for tile in self.tiles:
            for bendpoint in bendpoints:
                dist = sqrt((bendpoint[0] - tile.position[0])**2 + (bendpoint[1] - tile.position[1])**2)
                if dist < self.cutoff_distance:
                    tile.relaxed = False
                tile.handle_tile_rendering_and_state(screen, bendpoint)

    def apply_wind(self, omega, t, wind_speed=20):
        for tile in self.tiles:
            tilted_angle = wind_speed * (sin(omega * t + tile.phase_shift)) 
            tile.tile_uniform_rotation = tilted_angle
        















pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()




font = pygame.font.SysFont(None, 20)

def display_fps(screen, clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'fps: {fps}', True, pygame.Color("white"))
    screen_width, screen_height = screen.get_size()
    text_rect = fps_text.get_rect(topright=(screen_width - 10, 10))
    screen.blit(fps_text, text_rect)



