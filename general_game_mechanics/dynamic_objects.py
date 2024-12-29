from math import sin, cos, atan2, degrees, pi, sqrt, radians
from numpy import sign

import pygame

from general_game_mechanics.collisions import Hitbox

from graphics.particles import ParticleSystem
from graphics.sprite_stacks import SpritestackModel

from world.particle_presets import earthen_dust





class DynamicObject(SpritestackModel):
    def __init__(self, type=None, name=None, scale=1, mass=1000, movelocked=False):
        super().__init__(type, name, scale)

        self.mass = mass

        self.v_drag = 0.03
        self.omega_drag = 0.05
        self.dt = 0.01

        self.position = [0, 0]
        self.rotation = 0

        self.vx = 0
        self.vy = 0
        self.omega = 0

        self.ax = 0
        self.ay = 0
        self.a_omega = 0

        self.movelocked = movelocked

        self.hitbox = Hitbox(self)


    def move(self):
        if not self.movelocked:

            new_vx = (self.vx + self.ax * self.dt) * ( 1 - self.v_drag)
            new_vy = (self.vy + self.ay * self.dt) * ( 1 - self.v_drag)
            new_omega = (self.omega +  self.a_omega * self.dt) * ( 1 - self.omega_drag)

            new_x = self.position[0] + new_vx * self.dt
            new_y = self.position[1] - new_vy * self.dt
            new_rotation = self.rotation + new_omega * self.dt

            self.rotation = new_rotation

            self.vx = new_vx
            self.vy = new_vy
            self.omega = new_omega

            self.position[0] = new_x
            self.position[1] = new_y


            





            

class Vehicle(DynamicObject):
    def __init__(self, type=None, name=None, scale=1):
        super().__init__(type, name, scale)

        # Dustcloud settings
        self.dust = earthen_dust
        self.max_dustcloud_size = 20
        self.dust_particles_max_count = 50

        # SPEED_LIMIT
        self.max_speed = 400

        # ACCELERATION
        self.driving_acceleration = 2000
        self.steering_acceleration = 1500

        # DRAG
        self.braking_drag = 0.05
        self.omega_drag = 0.02

        self.turn_left = False
        self.turn_right = False
        self.accelerate = False
        self.reverse = False
        self.brake = False

        self.hitbox = Hitbox(self)


    def handle_movement(self, keys):
        self.turn_left = keys[pygame.K_a]
        self.turn_right = keys[pygame.K_d]
        self.accelerate = keys[pygame.K_w]
        self.reverse = keys[pygame.K_s]
        self.brake = keys[pygame.K_SPACE]


    def move(self):

        current_driving_acceleration = 0
        current_steering_acceleration = 0
        current_speed = sqrt(self.vx**2 + self.vy**2)

        steering_speed_factor = current_speed / self.max_speed
        if steering_speed_factor < 0.75:
            steering_speed_factor = 0.75
        if current_speed < 200:
            steering_speed_factor = 0.4
        if current_speed < 100:
            steering_speed_factor = 0.3
        if current_speed < 30:
            steering_speed_factor = 0

        if self.turn_left:
            current_steering_acceleration = self.steering_acceleration * steering_speed_factor
        if self.turn_right:
            current_steering_acceleration = -self.steering_acceleration * steering_speed_factor

        if self.accelerate:
            current_driving_acceleration = self.driving_acceleration

        if self.reverse:
            current_driving_acceleration = -self.driving_acceleration

        if self.brake:
            self.vx *= 1 - self.braking_drag
            self.vy *= 1 - self.braking_drag
            self.omega *= (1 - self.braking_drag/10)

        # Applying speed limits
        if current_speed > self.max_speed:
            current_driving_acceleration = 0

        self.ax = current_driving_acceleration * cos(radians(self.rotation))
        self.ay = current_driving_acceleration * sin(radians(self.rotation))
        self.a_omega = current_steering_acceleration

        # Gradually align velocity direction with the rotation angle when accelerating or braking
        if self.accelerate or self.brake:
            current_angle = atan2(self.vy, self.vx)
            forward_angle = radians(self.rotation)
            reverse_angle = radians(self.rotation) - pi
            forward_diff = (forward_angle - current_angle + pi) % (2 * pi) - pi
            reverse_diff = (reverse_angle - current_angle + pi) % (2 * pi) - pi
            if abs(forward_diff) < abs(reverse_diff):
                angle_diff = forward_diff
            else:
                angle_diff = reverse_diff
            align_factor = 1.1 - sqrt(self.vx**2 + self.vy**2) / self.max_speed # LOWER VALUE PROVIDES MORE DRIFT
            align_factor = max(0, min(align_factor, 1))
            adjusted_angle = current_angle + angle_diff * align_factor
            speed = sqrt(self.vx**2 + self.vy**2)
            self.vx = speed * cos(adjusted_angle)
            self.vy = speed * sin(adjusted_angle)
  
        super().move()

    def render(self, screen, camera, offset=[0, 0]):
        """ self.dust.position = [
            self.position[0] - self.hitbox_size[0]/2*cos(self.rotation),
            self.position[1] - self.hitbox_size[1]/2*sin(self.rotation),
            0
        ]
        factor = sqrt(self.vx**2 + self.vy**2)/self.max_speed
        self.dust.r_range = (0, round(self.max_dustcloud_size*factor))
        self.dust.max_count = self.dust_particles_max_count * factor
        self.dust.render(screen, camera)
        self.dust.update() """
        super().render(screen, camera, offset)
