import os

from math import atan2, degrees, pi, sqrt
from numpy import sign

import pygame


from graphics.particles import ParticleSystem
from graphics.sprite_stacks import render_stack, split_stack_image

from world.particle_presets import earthen_dust


class SpritestackModel:
    def __init__(self, type=None, name=None, scale=1):
        self.type = type
        self.name = name
        self.x = 100
        self.y = 100

        self.scale = scale

        # Load stack images
        self.stack_index = 0
        self.stack_image_multiple = []
        self.slice_images_folder = f'assets/{self.type}/{self.name}/sprite_stacks/'
        self.num_stacks = len(os.listdir(f'assets/{self.type}/{self.name}/sprite_stacks/'))
        for i in range(self.num_stacks):
            stack_image = (
                pygame.image.load(
                    f'{self.slice_images_folder}stack_{i}.png'
                ).convert_alpha()
            )
            self.stack_image_multiple.append(split_stack_image(stack_image))

        # setting hitbox to the same size as the width of a spritestack image
        self.hitbox_r = self.stack_image_multiple[0][0].get_width()//2 * self.scale

    def draw(self, screen):
        if self.stack_index >= self.num_stacks:
            self.stack_index = 0
        stack_images = self.stack_image_multiple[self.stack_index]
        render_stack(
            stack_images,
            self.x, self.y,
            self.rotation,
            screen,
            spread=0.8,
            scale=self.scale
        )



class Vehicle(SpritestackModel):
    def __init__(self, type=None, name=None):
        super().__init__(type, name)

        self.mass = 100
        self.movespeed = 40
        self.speed_limit = 100
        self.drag = 0.05
        self.dt = 0.1

        self.rotation = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

        # Dustcloud settings
        self.dust = earthen_dust
        self.max_dustcloud_size = 20
        self.dust_particles_max_count = 50

    def move(self, keys):
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]
        move_up = keys[pygame.K_UP]
        move_down = keys[pygame.K_DOWN]
        ax, ay = 0, 0
        if move_left:
            ax = -self.movespeed
        if move_right:
            ax = self.movespeed
        if move_up:
            ay = -self.movespeed
        if move_down:
            ay = self.movespeed
        # limiting the object's speed
        if sqrt(self.vx**2 + self.vy**2) > self.speed_limit:
            ax = 0
            ay = 0
        vx_new = self.vx + ax * self.dt - self.vx*self.drag
        vy_new = self.vy + ay * self.dt - self.vy*self.drag
        self.vx, self.vy = vx_new, vy_new
        new_x = self.x + self.vx * self.dt
        new_y = self.y + self.vy * self.dt
        self.x = new_x
        self.y = new_y
        self.rotation = degrees(-atan2(self.vy, self.vx))

    def draw_dust(self, screen):
        self.dust.x = self.x
        self.dust.y = self.y
        factor = sqrt(self.vx**2 + self.vy**2)/self.speed_limit
        self.dust.r_range = (0, round(self.max_dustcloud_size*factor))
        self.dust.max_count = self.dust_particles_max_count * factor
        self.dust.update_particles()
        self.dust.draw_particles(screen)




class SinglePlant(SpritestackModel):
    def __init__(self, type=None, name=None):
        super().__init__(type, name)

        self.dt = 0.1
        self.stiffness = 5
        self.springness = 0.5
        self.max_bend_angle = 90

        self.rotation = 0
        self.bend_angle = 0
        self.bending_objects = []

    def bend(self):
        for object in self.bending_objects:
            dx = self.x - object.x
            dy = self.y - object.y
            dist = sqrt(dx**2 + dy**2)
            if dist <= self.hitbox_r + object.hitbox_r:

                bending_force = (object.mass + sqrt(object.vx**2 + object.vy**2)) / self.stiffness
                rotating_force = degrees(atan2(object.vy, -object.vx)) - self.rotation
                self.bend_angle += bending_force / self.stiffness
                self.rotation += rotating_force / self.stiffness
                
                print(f'force: {bending_force}')

                if abs(self.bend_angle) >= self.max_bend_angle:
                    self.bend_angle = self.max_bend_angle

        self.stack_index = round((self.num_stacks-1) * (self.bend_angle/self.max_bend_angle))
        
        print(f'angle: {self.bend_angle}')
        print(f'rotation: {self.rotation}')
        print(f'stack: {self.stack_index}')

        """ self.rotation = self.rotation // 360 """
        self.rotation -= sign(self.rotation)* self.springness
        self.bend_angle -= sign(self.bend_angle) * self.springness