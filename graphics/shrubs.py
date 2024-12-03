import pygame

import random
import os

from math import sqrt, sin, cos, atan2, degrees, hypot, ceil, asin, pi, copysign, exp
from numpy import sign


WHITE = (255, 255, 255)

def draw_rotated_image(image, rotation_point_x, rotation_point_y, screen, angle=0):
    image_height = image.get_height()
    rotated_image = pygame.transform.rotate(image, -degrees(angle))
    rotated_image_rect = rotated_image.get_rect()
    rotated_image_rect.centerx = rotation_point_x
    rotated_image_rect.centery = rotation_point_y
    rotated_image_rect.centerx = rotation_point_x + image_height / 2 * sin(angle)
    rotated_image_rect.centery = rotation_point_y - image_height / 2 * cos(angle)
    screen.blit(rotated_image, rotated_image_rect.topleft)



class Branch:
    def __init__(self, base_position, base_angle, stiffness, folder):

        self.base_position = base_position
        self.base_angle = base_angle
        self.stiffness = stiffness
        self.elastic_force_mulitplier = 10

        self.num_segments = 0
        self.segment_images = []
        self.segment_lengths = []
        self.segment_angles = []

        self.total_angle_change = 0

        self.initialize_branch(folder)

        
        self.segment_startpoints = [
            [None, None] for _ in range(len(self.segment_images))
        ]


    def initialize_branch(self, branch_folder):
        self.num_segments = len(os.listdir(branch_folder))
        for i in range(self.num_segments):
            segment_image = pygame.image.load(f'{branch_folder}/segment_{i}.png').convert_alpha()
            self.segment_lengths.append(segment_image.get_height())
            self.segment_images.append(segment_image)
            self.segment_angles.append(self.base_angle)


    def apply_forces(self, external_force):
        total_angle_change = 0
        max_relative_bend = pi/2
        max_root_bend = 0.75*pi
        
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
            

    def render_on_surface(self, surface, offset_x=0, offset_y=0):
        x_start, y_start = self.base_position[0] - offset_x, self.base_position[1] - offset_y

        for i in range(self.num_segments):
            angle = self.segment_angles[i]
            length = self.segment_lengths[i]

            # Calculate the position of the next segment start point
            x_next = x_start + length * sin(angle)
            y_next = y_start - length * cos(angle)
            self.segment_startpoints[i] = [x_start + offset_x, y_start + offset_y]
            x_start, y_start = x_next, y_next

            # Render the segment on the surface with adjusted offsets
            segment_startpoint_x = self.segment_startpoints[i][0] - offset_x
            segment_startpoint_y = self.segment_startpoints[i][1] - offset_y
            segment_image = self.segment_images[i]
            draw_rotated_image(segment_image, segment_startpoint_x, segment_startpoint_y, surface, angle=angle)


    def render(self, screen):
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
            draw_rotated_image(segment_image, segment_startpoint_x, segment_startpoint_y, screen, angle=angle)




class Plant:
    def __init__(self, folder, num_branches, position, base_angle_range, stiffness):

        self.position = position
        self.image = None
        self.num_branches = num_branches
        
        self.hitbox_radius = 50

        self.branches = []

        self.total_angle_change = 0
        self.is_bent = False
        
        self.initialize_plant(folder, base_angle_range, stiffness)


    def initialize_plant(self, plant_folder, base_angle_range, stiffness):
        number_of_branch_variants = len(os.listdir(plant_folder))
        for k in range(0, self.num_branches):
            branch_base_angle = random.uniform(base_angle_range[0], base_angle_range[1])
            branch_variant_number = random.randint(0, number_of_branch_variants-1)
            branch_folder = f'{plant_folder}/branches/branch_{branch_variant_number}'
            branch = Branch(self.position, branch_base_angle, stiffness, branch_folder)
            self.branches.append(branch)

        # Creating single prerendered image for whole plant
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
            branch.render_on_surface(plant_surface, offset_x=self.position[0] - surface_width // 2,
                                     offset_y=self.position[1] - surface_height // 2)
        self.image = plant_surface


    def render_simple(self, screen):
        if self.image:
            screen.blit(self.image, (self.position[0] - self.image.get_width() // 2, 
                                     self.position[1] - self.image.get_height() // 2))


    def render_detailed(self, screen, bendpoints):
        # calculating total force from all bendpoints
        max_bend_factor = 0.3
        bend_factor = 0
        bend_sign = 0
        total_bend_force = 0
        total_angle_change = 0
        for bendpoint in bendpoints:
            if abs(self.position[0] - bendpoint[0]) <= self.hitbox_radius:
                if abs(self.position[1] - bendpoint[1]) <= self.hitbox_radius:
                    abs_distance_to_plant = sqrt((self.position[0] - bendpoint[0])**2 + (self.position[1] - bendpoint[1])**2)
                    bend_sign = copysign(1, self.position[0] - bendpoint[0])
                    bend_factor = min(max_bend_factor, (abs_distance_to_plant / self.hitbox_radius))
                    total_bend_force += bend_sign * bend_factor

        # updating and rendering all branches
        for branch in self.branches:
            branch.apply_forces(total_bend_force)
            total_angle_change += branch.total_angle_change
            branch.render(screen)
        self.total_angle_change = total_angle_change


    def render_plant(self, screen, bendpoints):
        min_angle_change_for_detailed_render = 0.01

        # monitoring if the plant is currently being bent
        is_bent = False
        for bendpoint in bendpoints:
            if sqrt((self.position[0] - bendpoint[0])**2 + (self.position[1] - bendpoint[1])**2) <= self.hitbox_radius:
                is_bent = True
        self.is_bent = is_bent

        if (self.total_angle_change > min_angle_change_for_detailed_render) or (self.is_bent):
            self.render_detailed(screen, bendpoints)
        else:
            self.render_simple(screen)




class PlantSystem:
    def __init__(self, folder, num_branches_range, base_angle_range, stiffness_range, gravity, density):

        self.num_branches_range = num_branches_range
        self.base_angle_range = base_angle_range
        self.stiffness_range = stiffness_range
        self.gravity = gravity
        self.density = density

        self.mask_name = 'test_mask'
        self.plants = []
        self.bendpoints = []
        self.create_plants(folder)


    def create_plants(self, plant_folder):
        mask = pygame.image.load(f'{plant_folder}/masks/{self.mask_name}.png').convert()
        mask_width = mask.get_width()
        mask_height = mask.get_height()
        for x in range(mask_width):
            for y in range(mask_height):
                colour = mask.get_at((x, y))
                if colour != WHITE:
                    rand_num = random.uniform(0, 1)
                    if rand_num < self.density:
                        position = (x, y)
                        num_branches = random.randint(self.num_branches_range[0], self.num_branches_range[1])
                        stiffness = random.uniform(self.stiffness_range[0], self.stiffness_range[1])
                        plant = Plant(plant_folder, num_branches, position, self.base_angle_range, stiffness)
                        self.plants.append(plant)


    def render(self, screen):
        for plant in self.plants:
            plant.render_plant(screen, self.bendpoints)