import random
import pygame

from math import sin, cos, atan2, sqrt, radians, pi

from assets.particle_systems import vehicle_exhaust

from objects.generic import CompositeObject


class Vehicle(CompositeObject):
    
    def __init__(self, parts_positions_rotations, type=None, position=[0,0,0], rotation=0, hitbox_size=[64,64], hitbox_offset=(0,0), hitbox_type='rectangle'):
        super().__init__(parts_positions_rotations, type, position, rotation, hitbox_size, hitbox_offset, hitbox_type)

        self.driver = None

        # Dustcloud settings
        self.exhaust = vehicle_exhaust
        self.max_dustcloud_size = 20
        self.exhaust_particles_max_count = 50

        # SPEED_LIMIT
        self.max_speed = 700

        # ACCELERATION
        self.driving_acceleration = 1500
        self.steering_acceleration = 1000

        # DRAG
        self.braking_drag = 0.05
        self.omega_drag = 0.02

        self.turn_left = False
        self.turn_right = False
        self.accelerate = False
        self.reverse = False
        self.brake = False


    def handle_driver(self, character):
        enter_exit_padding = 20
        if character.action:
            if not self.driver and not character.vehicle:
                distance_to_character = sqrt((self.position[0] - character.position[0])**2 + (self.position[1] - character.position[1])**2)
                if distance_to_character < sqrt(self.hitbox.size[0]**2 + self.hitbox.size[1]**2) / 2 + enter_exit_padding:
                    if character.action:
                        self.driver = character
                        self.driver.collidable = False
                        self.driver.vehicle = self
            elif (self.driver != None):
                random_exit_angle = radians(random.randint(-180, 180))
                self.driver.position = [
                    self.position[0] + (self.hitbox.size[0]/2 + enter_exit_padding) * sin(random_exit_angle),
                    self.position[1] + (self.hitbox.size[1]/2 + enter_exit_padding) * cos(random_exit_angle),
                    self.position[2]
                    ]
                self.driver.vehicle = None
                self.driver.collidable = True
                self.driver = None


    def handle_movement(self, keys):
        self.turn_left = keys[pygame.K_a]
        self.turn_right = keys[pygame.K_d]
        self.accelerate = keys[pygame.K_w]
        self.reverse = keys[pygame.K_s]
        self.brake = keys[pygame.K_b]


    def move(self):

        if self.driver:
            
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
            if self.driver:
                self.driver.vx = self.vx
                self.driver.vy = self.vy
            
        super().move()


    def render(self, screen, camera, offset=[0, 0]):
        self.exhaust.position = [
            self.position[0],
            self.position[1],
            self.position[2]
        ]
        factor = sqrt(self.vx**2 + self.vy**2)/self.max_speed
        self.exhaust.r_range = (0, round(self.max_dustcloud_size*factor))
        self.exhaust.max_count = self.exhaust_particles_max_count * factor
        self.exhaust.render(screen, camera)
        self.exhaust.update()
        super().render(screen, camera, offset)