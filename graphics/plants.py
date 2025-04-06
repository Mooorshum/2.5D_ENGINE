import pygame

import copy
import random
import os

from math import sqrt, sin, cos, atan2, degrees, hypot, ceil, asin, pi, copysign, exp, radians
from numpy import sign

from general_game_mechanics.collisions import Hitbox


def draw_rotated_image(image, rotation_point_x, rotation_point_y, screen, angle=0, offset=[0, 0]):
    image_height = image.get_height()
    rotated_image = pygame.transform.rotate(image, -degrees(angle))
    rotated_image_rect = rotated_image.get_rect()
    rotated_image_rect.centerx = rotation_point_x
    rotated_image_rect.centery = rotation_point_y
    rotated_image_rect.centerx = rotation_point_x + image_height / 2 * sin(angle)
    rotated_image_rect.centery = rotation_point_y - image_height / 2 * cos(angle)
    screen.blit(
        rotated_image,
        (
            rotated_image_rect.topleft[0] + offset[0],
            rotated_image_rect.topleft[1] + offset[1]
        )
    )



class Branch:
    def __init__(self, base_position, base_angle, stiffness, folder, scale=1):

        self.branch_folder = folder

        self.base_position = base_position
        self.base_angle = base_angle
        self.stiffness = stiffness

        self.scale = scale

        self.num_segments = 0
        self.segment_images = []
        self.segment_image_paths = []

        self.segment_lengths = []
        self.segment_angles = []

        self.total_angle_change = 0

        self.initialize_branch(self.branch_folder, self.scale)
        
        self.segment_startpoints = [
            [None, None] for _ in range(len(self.segment_images))
        ]


    def initialize_branch(self, branch_folder, scale):
        self.num_segments = len(os.listdir(branch_folder))
        for i in range(self.num_segments):
            segment_image_path = f'{branch_folder}/segment_{i}.png'
            segment_image = pygame.image.load(segment_image_path).convert()
            if scale != 1:
                segment_image = pygame.transform.scale(
                    segment_image,
                    (
                        int(segment_image.get_width() * scale),
                        int(segment_image.get_height() * scale)
                    )
                )
            segment_image.set_colorkey((0, 0, 0))
            self.segment_lengths.append(segment_image.get_height())
            self.segment_images.append(segment_image)
            self.segment_image_paths.append(segment_image_path)
            self.segment_angles.append(self.base_angle)


    def apply_forces(self, external_force):
        total_angle_change = 0
        max_relative_bend = pi/2
        max_root_bend = pi/3
        
        for i in range(self.num_segments):
            angle = self.segment_angles[i]

            # Elastic force
            if i > 0:
                delta_angle = angle - self.segment_angles[i-1]
                if abs(delta_angle) > max_relative_bend:
                    angle = self.segment_angles[i-1] + max_relative_bend*copysign(1, delta_angle)
                elastic_force = -self.stiffness * delta_angle
            else:
                delta_angle = angle - self.base_angle
                elastic_force = -self.stiffness * delta_angle

            new_angle = angle + (elastic_force + external_force )

            if i == 0:
                if new_angle < -max_root_bend:
                    new_angle = -max_root_bend
                elif new_angle > max_root_bend:
                    new_angle = max_root_bend

            total_angle_change += abs(angle - new_angle)
            self.segment_angles[i] = new_angle
        self.total_angle_change = total_angle_change
            

    def render_on_surface(self, surface, offset=[0, 0]):
        x_start, y_start = self.base_position[0] - offset[0], self.base_position[1] - offset[1]

        for i in range(self.num_segments):
            angle = self.segment_angles[i]
            length = self.segment_lengths[i]

            # Calculate the position of the next segment start point
            x_next = x_start + length * sin(angle)
            y_next = y_start - length * cos(angle)
            self.segment_startpoints[i] = [x_start + offset[0], y_start + offset[1]]
            x_start, y_start = x_next, y_next

            # Render the segment on the surface with adjusted offsets
            segment_startpoint_x = self.segment_startpoints[i][0] - offset[0]
            segment_startpoint_y = self.segment_startpoints[i][1] - offset[1]
            segment_image = self.segment_images[i]
            draw_rotated_image(segment_image, segment_startpoint_x, segment_startpoint_y, surface, angle=angle)


    def render(self, screen, offset=[0, 0]):
        # branch root startpoint
        x_start, y_start = self.base_position[0], self.base_position[1]

        for i in range(self.num_segments):

            # update segment startpoint
            angle = self.segment_angles[i]
            length = self.segment_lengths[i]
            x_next = x_start + length * sin(angle)
            y_next = y_start - length * cos(angle)
            self.segment_startpoints[i] = [x_start, y_start]
            x_start, y_start = x_next, y_next

            # render segments
            segment_startpoint_x = self.segment_startpoints[i][0]
            segment_startpoint_y = self.segment_startpoints[i][1]
            segment_image = self.segment_images[i]
            angle = self.segment_angles[i]
            draw_rotated_image(segment_image, segment_startpoint_x, segment_startpoint_y, screen, angle=angle, offset=offset)

    def get_data(self):
        data = {}
        data['scale'] = self.scale
        data['branch_folder'] = self.branch_folder
        data['base_position'] = self.base_position
        data['base_angle'] = self.base_angle
        return data




class PlantAsset:
    def __init__(self, index, plant_folder, num_branches, base_angle_range, stiffness, relax_speed=0.5, scale=1):

        self.index = index

        self.image = None
        self.num_branches = num_branches

        self.branches = []

        # Used for reconstructing asset from data
        self.branch_paths = []
        self.branch_base_angles = []

        self.stiffness = stiffness
        self.total_angle_change = 0
        self.relax_speed = relax_speed
        self.scale = scale

        self.initialize_asset(plant_folder, base_angle_range)
        self.prerender_plant()

    def initialize_asset(self, plant_folder, base_angle_range):
        number_of_branch_variants = len(os.listdir(f'{plant_folder}/branches/'))
        base_angle_span = radians(random.randint(base_angle_range[0], base_angle_range[1]))
        base_angle_step = 2*base_angle_span / self.num_branches
        for k in range(0, self.num_branches):
            branch_base_angle = -base_angle_span + k*base_angle_step
            self.branch_base_angles.append(branch_base_angle)
            if self.num_branches == 1:
                branch_base_angle = radians(random.randint(-30, 30))
                self.branch_base_angles.append(branch_base_angle)
            branch_variant_number = random.randint(0, number_of_branch_variants-1)
            branch_folder = f'{plant_folder}/branches/branch_{branch_variant_number}'
            self.branch_paths.append(branch_folder)
            branch = Branch(base_position=[0, 0], base_angle=branch_base_angle, stiffness=self.stiffness, folder=branch_folder, scale=self.scale)
            self.branches.append(branch)


    def prerender_plant(self):
        # Creating single prerendered image for the whole plant
        max_branch_size = 0
        for branch in self.branches:
            branch_size = 0
            for i in range(branch.num_segments):
                branch_size += branch.segment_lengths[i]
            if branch_size > max_branch_size:
                max_branch_size = branch_size
        surface_width = max_branch_size * 2
        surface_height = max_branch_size * 2
        plant_surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        for branch in self.branches:
            branch.render_on_surface(
                plant_surface,
                offset=[ -surface_width // 2, -surface_height // 2]
            )
        self.image = plant_surface


    def get_data(self):
        data = {}
        data['index'] = self.index
        data['stiffness'] = self.stiffness
        data['scale'] = self.scale
        data['num_branches'] = self.num_branches
        data['branch_paths'] = self.branch_paths
        data['branch_base_angles'] = self.branch_base_angles
        return data


    def load(self, data):
        self.index = data['index']
        self.stiffness = data['stiffness']
        self.branches = []
        self.scale = data['scale']
        self.branch_paths = data['branch_paths']
        self.branch_base_angles = data['branch_base_angles']
        for i in range(len(self.branch_paths)):
            branch = Branch(
                base_position=[0, 0],
                base_angle=self.branch_base_angles[i],
                stiffness=self.stiffness,
                folder=self.branch_paths[i],
                scale=self.scale
            )
            self.branches.append(branch)
        self.prerender_plant()





class Plant:
    def __init__(self, asset, position):

        self.asset = asset

        self.position = position

        self.branches = copy.deepcopy(self.asset.branches)

        self.total_angle_change = 0
        self.is_bent = False
        self.relax_speed = self.asset.relax_speed

        # PROPERTIES REQUIRED FOR TOPOLOGICAL DEPTH SORTING
        self.rotation = 0
        max_branch_length = 0
        for branch in self.asset.branches:
            branch_length = 0
            for segment_length in branch.segment_lengths:
                branch_length += segment_length
            if branch_length > max_branch_length:
                max_branch_length = branch_length
        self.height = max_branch_length
        self.hitbox = Hitbox(
            object=self,
            size=(max_branch_length, max_branch_length),
            type='rectangle'
        )


    def render_simple(self, screen, offset=[0, 0]):
        if self.asset.image:
            screen.blit(
                self.asset.image,
                (
                    self.position[0] - self.asset.image.get_width() // 2 + offset[0], 
                    self.position[1] - self.asset.image.get_height() // 2 + offset[1] - self.position[2]
                )
            )


    def render_detailed(self, screen, bend_objects, offset=[0, 0]):
        # calculating total force from all bendpoints
        max_bend_factor = 0.2
        bend_factor = 0
        bend_sign = 0
        total_bend_force = 0
        total_angle_change = 0
        for bend_object in bend_objects:
            hitbox_radius = sqrt(bend_object.hitbox.size[0]**2 + bend_object.hitbox.size[0]**2) / 2
            if sqrt((self.position[0] - bend_object.position[0])**2 + (self.position[1] - bend_object.position[1])**2) <= hitbox_radius:
                    abs_distance_to_plant = sqrt((self.position[0] - bend_object.position[0])**2 + (self.position[1] - bend_object.position[1])**2)
                    bend_sign = copysign(1, self.position[0] - bend_object.position[0])
                    bend_factor = min(max_bend_factor, (abs_distance_to_plant / hitbox_radius))
                    total_bend_force += bend_sign * bend_factor

        # updating and rendering all branches
        for branch in self.branches:
            branch.apply_forces(total_bend_force * self.relax_speed)
            total_angle_change += branch.total_angle_change
            branch.render(screen, offset)
        self.total_angle_change = total_angle_change


    def render(self, screen, bend_objects, offset=[0, 0]):
        min_angle_change_for_detailed_render = 0.005

        # monitoring if the plant is currently being bent
        is_bent = False
        for bend_object in bend_objects:
            if sqrt((self.position[0] - bend_object.position[0])**2 + (self.position[1] - bend_object.position[1])**2) <= sqrt(bend_object.hitbox.size[0]**2 + bend_object.hitbox.size[1]**2) / 2:
                is_bent = True
        self.is_bent = is_bent

        if (self.total_angle_change > min_angle_change_for_detailed_render) or (self.is_bent):
            self.render_detailed(screen, bend_objects, offset)
        else:
            self.render_simple(screen, offset)

    def get_data(self):
        data = {}
        data['position'] = self.position
        data['asset_index'] = self.asset.index
        return data

    def load(self, data, asset):
        self.position = data['position']
        self.asset = asset




class PlantSystem:
    def __init__(self, folder, num_branches_range, base_angle_range, stiffness_range, relax_speed=1, scale=1, num_assets=10):

        self.plant_folder = folder

        self.num_branches_range = num_branches_range
        self.base_angle_range = base_angle_range
        self.stiffness_range = stiffness_range
        self.relax_speed = relax_speed

        self.scale = scale

        self.num_assets = num_assets
        self.assets = self.generate_assets(self.plant_folder, self.scale , self.num_assets)
        self.plants = []
        self.bend_objects = []


    def generate_assets(self, plant_folder, scale, num_assets):
        assets = []
        for asset_index in range(num_assets):
            num_branches = random.randint(self.num_branches_range[0], self.num_branches_range[1])
            stiffness = random.uniform(self.stiffness_range[0], self.stiffness_range[1])
            asset = PlantAsset(asset_index, plant_folder, num_branches, self.base_angle_range, stiffness, self.relax_speed, scale=scale)
            assets.append(asset)
        return assets


    def create_plant(self, asset_index, position):
        asset = self.assets[asset_index]
        plant = Plant(asset, position)
        for branch in plant.branches:
            branch.base_position[0] += position[0]
            branch.base_position[1] += position[1]
            branch.base_position[1] -= position[2]
        self.plants.append(plant)


    def render(self, screen, offset=[0, 0]):
        for plant in self.plants:
            plant.render(screen, self.bend_objects, offset)


    def get_data(self):
        system_data = {}

        # GETTING ASSET DATA
        system_asset_data = []
        for asset in self.assets:
            system_asset_data.append(asset.get_data())
        system_data['assets'] = system_asset_data

        # GETTING PLANT DATA
        system_plant_data = []
        for plant in self.plants:
            system_plant_data.append(plant.get_data())
        system_data['plants'] = system_plant_data

        # GENERAL SYSTEM INFO
        system_data['scale'] = self.scale
        system_data['plant_folder'] = self.plant_folder

        return system_data


    def load(self, system_data):
        
        # LOADING ASSETS
        self.assets = []
        for asset_data in system_data['assets']:
            asset = PlantAsset(
                asset_data['index'],
                system_data['plant_folder'],
                asset_data['num_branches'],
                self.base_angle_range,
                asset_data['stiffness'],
                self.relax_speed,
                system_data['scale']
            )
            asset.load(asset_data)
            self.assets.append(asset)

        # LOADING PLANTS
        self.plants = []
        for plant_data in system_data['plants']:
            self.create_plant(plant_data['asset_index'], plant_data['position'])
