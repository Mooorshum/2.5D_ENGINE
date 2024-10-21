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

    """ line_end_x = rotation_point_x + image_height * sin(angle)
    line_end_y = rotation_point_y - image_height * cos(angle)
    pygame.draw.line(screen, (255, 0, 0), (rotation_point_x, rotation_point_y), (line_end_x, line_end_y), 2) """
    screen.blit(rotated_image, rotated_image_rect.topleft)


class FlexibleLeaf:
    def __init__(
        self,
        x_base, y_base,
        segment_images=None,
        base_angle=pi/4,
        stiffness=0.2,
        gravity=0.01,
        dt = 2,
        root_stiffness = 0.2,
    ):
        self.x_base = x_base
        self.y_base = y_base
        self.base_angle = base_angle
        self.stiffness = stiffness
        self.gravity = gravity
        self.dt = dt
        # segment properties
        self.segments = segment_images # segment images
        self.num_segments = len(segment_images) # number of segments
        self.segment_angles = [base_angle] * len(segment_images) # segment inclination angles
        self.segment_lengths = [segment.get_height() for segment in segment_images] # segment lengths
        self.segment_startpoints = [[self.x_base, self.y_base] for _ in range(len(segment_images))] # segment startpoints
        # External forces for each segment
        self.external_force = 0
        self.root_stiffness = root_stiffness

    def update_segment_startpoints(self):
        x_start, y_start = self.x_base, self.y_base
        for i in range(self.num_segments):
            angle = self.segment_angles[i]
            length = self.segment_lengths[i]
            x_next = x_start + length * sin(angle)
            y_next = y_start - length * cos(angle)
            self.segment_startpoints[i] = [x_start, y_start]
            x_start, y_start = x_next, y_next

    def apply_forces(self):
        for i in range(self.num_segments):
            angle = self.segment_angles[i]
            segment_length = self.segment_lengths[i]

            # Elastic force
            if i > 0:
                delta_angle = angle - self.segment_angles[i-1]
                elastic_force = -self.stiffness * delta_angle 
            else:
                delta_angle = angle - self.base_angle
                elastic_force = -self.root_stiffness * delta_angle 

            # External force
            external_force = self.external_force * cos(angle/4)

            # Gravitational force
            gravitational_force = sign(angle) * (self.gravity)

            new_angle = angle + (elastic_force + gravitational_force + external_force) * self.dt

            if i == 0:
                if new_angle < -pi/2:
                    new_angle = -pi/2
                elif new_angle > pi/2:
                    new_angle = pi/2

            self.segment_angles[i] = new_angle

    def update(self):
        self.apply_forces()
        self.update_segment_startpoints()

    def draw(self, screen):
        for i in range(self.num_segments):
            segment_startpoint_x = self.segment_startpoints[i][0]
            segment_startpoint_y = self.segment_startpoints[i][1]
            segment_image = self.segments[i]
            angle = self.segment_angles[i]

            # Draw each segment, connecting at its start point
            draw_rotated_image(segment_image, segment_startpoint_x, segment_startpoint_y, screen, angle=angle)


class PlantSystem:
    def __init__(self, plant_folder):
        self.base_angle_range = (-pi/4, pi/4)
        self.stiffness_range = (0.005, 0.05)
        self.root_stiffness_range = (0.01, 0.1)
        self.density = 0.0005

        self.hitbox_lx = 60
        self.hitbox_ly = 30
        self.step_effect_radius = self.hitbox_ly # sqrt(self.hitbox_lx**2 + self.hitbox_ly**2)

        self.step_bend_force = 0.05

        self.gravity = 0.01

        self.num_leaves_range = (1,1)

        self.plant_folder = plant_folder
        
        self.mask_name = None
        self.plants = []

        self.x_player = None
        self.y_player = None

    def get_leaf_images(self, folder):
        number_of_segments = len(os.listdir(folder))
        segment_images = []
        for i in range(number_of_segments):
            segment_images.append(pygame.image.load(f'{folder}/segment_{i}.png').convert_alpha())
        return segment_images

    def generate_plants(self):
        mask = pygame.image.load(f'{self.plant_folder}/masks/{self.mask_name}.png').convert()
        mask_width = mask.get_width()
        mask_height = mask.get_height()
        for x in range(mask_width):
            for y in range(mask_height):
                colour = mask.get_at((x, y))
                if colour != WHITE:
                    rand_num = random.uniform(0, 1)
                    if rand_num < self.density:
                        self.plants.append(self.create_plant(x, y))

    def create_plant(self, x, y):
        plant_graphics_folder = f'{self.plant_folder}/graphics/'
        number_of_leaf_variants = len(os.listdir(plant_graphics_folder))
        plant_leaves = []
        num_leaves = random.randint(self.num_leaves_range[0], self.num_leaves_range[1])
        base_angle_span = (self.base_angle_range[1] - self.base_angle_range[0])
        if num_leaves > 1:
            base_angles = [self.base_angle_range[0] + (i-1)*base_angle_span/num_leaves for i in range(1, num_leaves+1)]
        else:
            base_angles = [random.uniform(-pi/10, pi/10)]
        for k in range(0, num_leaves):
            leaf_number = random.randint(0, number_of_leaf_variants-1)
            leaf_folder = f'{plant_graphics_folder}leaf_{leaf_number}/'
            leaf_segment_images = self.get_leaf_images(leaf_folder)
            leaf = FlexibleLeaf(
                x_base=x, y_base=y,
                segment_images=leaf_segment_images,
                base_angle=base_angles[k],
                stiffness=random.uniform(self.stiffness_range[0], self.stiffness_range[1]),
                gravity = self.gravity,
                root_stiffness = random.uniform(self.root_stiffness_range[0], self.root_stiffness_range[1]), 
            )
            plant_leaves.append(leaf)
            plant_leaves[-1].update_segment_startpoints()
        return plant_leaves

    def update_plants(self):
        for plant in self.plants:
            num_leaves = len(plant)
            plant_x_base, plant_y_base = plant[0].x_base, plant[0].y_base
            distance_to_base = sqrt((plant_x_base - self.x_player) ** 2 + (plant_y_base - self.y_player) ** 2)
            in_hitbox_x = (self.x_player < plant_x_base + self.hitbox_lx/2) and (self.x_player > plant_x_base - self.hitbox_lx/2)
            in_hitbox_y = (self.y_player > plant_y_base - self.hitbox_ly/2) and (self.y_player < plant_y_base + self.hitbox_ly/2)
            if in_hitbox_x and in_hitbox_y:
                for i in range(num_leaves):
                    plant[i].external_force = self.step_bend_force * (1 - distance_to_base / self.step_effect_radius) * copysign(1, plant_x_base - self.x_player)
            else:
                for i in range(num_leaves):
                    plant[i].external_force = 0
            for i in range(num_leaves):
                plant[i].update()


    def draw_plants(self, screen):
        for plant in self.plants:
            num_leaves = len(plant)
            for i in range(num_leaves):
                plant[i].draw(screen)
