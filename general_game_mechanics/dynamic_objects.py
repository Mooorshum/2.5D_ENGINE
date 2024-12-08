from math import sin, cos, atan2, degrees, pi, sqrt, radians
from numpy import sign

import pygame

from general_game_mechanics.collisions import Hitbox

from graphics.particles import ParticleSystem
from graphics.sprite_stacks import render_stack, split_stack_image, SpritestackModel







""" class Vehicle(SpritestackModel):
    def __init__(self, type=None, name=None, scale=1):
        super().__init__(type, name, scale)

        self.mass = 1000
        self.movespeed = 40
        self.speed_limit = 100
        self.drag = 0.05
        self.dt = 0.1

        self.rotation = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

        self.hitbox = Hitbox(self)

        # Dustcloud settings
        self.dust = ParticleSystem()
        DUST_BROWN_1 = (184, 160, 133)
        DUST_BROWN_2 = (181, 153, 140)
        DUST_BROWN_3 = (181, 153, 140)
        DUST_BROWN_4 = (199, 186, 151)
        self.dust.colours = (
            DUST_BROWN_1, DUST_BROWN_2, DUST_BROWN_3, DUST_BROWN_4,
        )
        self.dust.lifetime_range = (10, 100)
        self.dust.acceleration_range = (10, 50)
        self.dust.ay_system = -30
        self.max_dustcloud_size = 20
        self.dust_particles_max_count = 50


    def handle_movement(self, keys):
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
        self.vx += ax * self.dt
        self.vy += ay * self.dt


    def move(self):
        new_x = self.position[0] + self.vx * self.dt
        new_y = self.position[1] + self.vy * self.dt
        self.vx -= self.vx*self.drag
        self.vy -= self.vy*self.drag
        self.position[0] = new_x
        self.position[1] = new_y
        self.rotation = degrees(-atan2(self.vy, self.vx))

    def draw_dust(self, screen):
        self.dust.position = self.position
        factor = sqrt(self.vx**2 + self.vy**2)/self.speed_limit
        self.dust.r_range = (0, round(self.max_dustcloud_size*factor))
        self.dust.max_count = self.dust_particles_max_count * factor
        self.dust.update_particles()
        self.dust.draw_particles(screen) """



class DynamicObject(SpritestackModel):
    def __init__(self, type=None, name=None, scale=1):
        super().__init__(type, name, scale)

        self.movelocked = False

        self.mass = 1000

        self.linear_acceleration_forward = 10
        self.linear_speed_limit_forward = 80

        self.linear_acceleration_backwards = 5
        self.linear_speed_limit_backwards = 20

        self.anglular_acceleration = 25
        self.angular_speed_limit = 25

        self.brake_acceleration = 10
        self.linear_drag = 0.1
        self.angular_drag = 0.5
        self.dt = 0.1

        self.rotation = 0
        self.angular_speed = 0
        self.linear_speed = 0

        self.hitbox = Hitbox(self)

        # Dustcloud settings
        self.dust = ParticleSystem()
        DUST_BROWN_1 = (184, 160, 133)
        DUST_BROWN_2 = (181, 153, 140)
        DUST_BROWN_3 = (181, 153, 140)
        DUST_BROWN_4 = (199, 186, 151)
        self.dust.colours = (
            DUST_BROWN_1, DUST_BROWN_2, DUST_BROWN_3, DUST_BROWN_4,
        )
        self.dust.lifetime_range = (10, 100)
        self.dust.acceleration_range = (10, 50)
        self.dust.ay_system = -30
        self.max_dustcloud_size = 20
        self.dust_particles_max_count = 50


    def handle_movement(self, keys):
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]
        move_up = keys[pygame.K_UP]
        move_down = keys[pygame.K_DOWN]
        space = keys[pygame.K_SPACE]

        if self.type=='vehicle':
            if move_left:
                self.angular_speed += self.anglular_acceleration * self.dt
            if move_right:
                self.angular_speed -= self.anglular_acceleration * self.dt
            if move_up:
                self.linear_speed += self.linear_acceleration_forward * self.dt
            if move_down:
                self.linear_speed -= self.linear_acceleration_backwards * self.dt
            if space:
                self.linear_speed -= sign(self.linear_speed) * self.brake_acceleration * self.dt


    def move(self):
        if not self.movelocked:
            # applying speed limits
            if self.linear_speed > self.linear_speed_limit_forward:
                self.linear_speed = self.linear_speed_limit_forward
            if self.linear_speed < -self.linear_speed_limit_backwards:
                self.linear_speed = -self.linear_speed_limit_backwards
            if abs(self.angular_speed) > self.angular_speed_limit:
                self.angular_speed = sign(self.angular_speed) * self.angular_speed_limit
    
            # Applying drag
            self.linear_speed -= self.linear_speed * self.linear_drag * self.dt
            self.angular_speed -= self.angular_speed * self.angular_drag * self.dt
    
            # Updating rotation
            self.rotation += self.angular_speed * self.dt * (abs(self.linear_speed)/self.linear_speed_limit_forward)**(1/4)
    
            # Updating position
            self.position[0] += self.linear_speed * cos(radians(self.rotation)) * self.dt
            self.position[1] -= self.linear_speed * sin(radians(self.rotation)) * self.dt


    def render(self, screen, offset=[0, 0]):
        self.dust.position = self.position
        factor = abs(self.linear_speed)/self.linear_speed_limit_forward
        self.dust.r_range = (0, round(self.max_dustcloud_size*factor))
        self.dust.max_count = self.dust_particles_max_count * factor
        self.dust.update()
        self.dust.render(screen, offset)
        super().render(screen, offset)