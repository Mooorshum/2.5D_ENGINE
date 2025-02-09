from math import sin, cos, atan2, degrees, pi, sqrt, radians
from numpy import sign

import pygame

from general_game_mechanics.collisions import Hitbox

from graphics.particles import ParticleSystem, Projectile
from graphics.sprite_stacks import SpritestackModel

from presets.particle_presets import earthen_dust, flame_front

import random

import copy




class DynamicObject(SpritestackModel):
    def __init__(self, asset, asset_index, position, rotation):
        super().__init__(asset, asset_index, position, rotation)

        self.v_drag = 0.03
        self.omega_drag = 0.05
        self.dt = 0.01

        self.mass = asset.mass

        self.vx = 0
        self.vy = 0
        self.omega = 0

        self.ax = 0
        self.ay = 0
        self.a_omega = 0

        self.ground_effect_particle_system = None

        self.movelocked = self.asset.movelocked


    def move(self):
        if not self.movelocked:

            new_vx = (self.vx + self.ax * self.dt) * ( 1 - self.v_drag)
            new_vy = (self.vy + self.ay * self.dt) * ( 1 - self.v_drag)
            new_omega = (self.omega +  self.a_omega * self.dt) * ( 1 - self.omega_drag)

            new_x = self.position[0] + new_vx * self.dt
            new_y = self.position[1] - new_vy * self.dt
            new_rotation = self.rotation + new_omega * self.dt

            self.vx = new_vx
            self.vy = new_vy
            self.omega = new_omega

            self.position[0] = new_x
            self.position[1] = new_y
            self.rotation = new_rotation

    def render(self, screen, camera, offset=[0, 0]):
        super().render(screen, camera, offset)
        self.hitbox.render(screen, camera, offset)

        if self.ground_effect_particle_system:
            self.ground_effect_particle_system.position = self.position
            self.ground_effect_particle_system.render(screen, camera)
            self.ground_effect_particle_system.update()



            

            

class Vehicle(DynamicObject):
    def __init__(self, asset, asset_index, position, rotation):
        super().__init__(asset, asset_index, position, rotation)

        self.driver = None

        # Dustcloud settings
        self.dust = earthen_dust
        self.max_dustcloud_size = 20
        self.dust_particles_max_count = 50

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
                        self.driver.vehicle = self
            elif (self.driver != None):
                random_exit_angle = radians(random.randint(-180, 180))
                self.driver.position = [
                    self.position[0] + (self.hitbox.size[0]/2 + enter_exit_padding) * sin(random_exit_angle),
                    self.position[1] + (self.hitbox.size[1]/2 + enter_exit_padding) * cos(random_exit_angle)
                    ]
                self.driver.vehicle = None
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
            
        super().move()


    def render(self, screen, camera, offset=[0, 0]):
        self.dust.position = [
            self.position[0],
            self.position[1],
            self.position[2]
        ]
        factor = sqrt(self.vx**2 + self.vy**2)/self.max_speed
        self.dust.r_range = (0, round(self.max_dustcloud_size*factor))
        self.dust.max_count = self.dust_particles_max_count * factor
        self.dust.render(screen, camera)
        self.dust.update()
        super().render(screen, camera, offset)








class Character(DynamicObject):
    def __init__(self, asset, asset_index, position, rotation):
        super().__init__(asset=asset, asset_index=asset_index, position=position, rotation=rotation)

        self.movespeed = 1000
        self.walk_speed_limit = 50
        self.run_speed_limit = 100

        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.running = False

        self.vehicle = None

        self.projectile_asset = flame_front
        self.projectile_speed = 50
        self.aiming = False
        self.shoot = False
        self.projectiles = []

        self.action = None


    def handle_controls(self, keys, events):
        self.move_up = keys[pygame.K_s]
        self.move_down = keys[pygame.K_w]
        self.move_left = keys[pygame.K_a]
        self.move_right = keys[pygame.K_d]
        self.running = pygame.key.get_mods() & pygame.KMOD_SHIFT

        self.action = False
        self.aiming = False
        self.shoot = False

        for event in events:

            """ ACTION """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.action = True

            """ AIMING """
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.aiming = True

            """ SHOOTING """
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shoot = True

        if self.vehicle != None:
            self.vehicle.handle_movement(keys)







        
    def update(self, camera):

        """ ANIMATING OBJECT BY SWITCHING STACK INDEX """
        if sqrt(self.vx**2 + self.vy**2) > 5:

            if self.internal_time // 10 == 0:
                self.stack_index = 0
            elif self.internal_time // 10 == 1:
                self.stack_index = 1
            elif self.internal_time // 10 == 2:
                self.stack_index = 2
            elif self.internal_time // 10 == 3:
                self.stack_index = 3
            elif self.internal_time // 10 == 4:
                self.stack_index = 4
            elif self.internal_time // 10 == 5:
                self.stack_index = 5
            elif self.internal_time // 10 == 6:
                self.stack_index = 6
            elif self.internal_time // 10 == 7:
                self.stack_index = 7
            else:
                self.internal_time = 0

            if self.running:
                if self.internal_time // 8 == 0:
                    self.stack_index = 8
                elif self.internal_time // 8 == 1:
                    self.stack_index = 9
                elif self.internal_time // 8 == 2:
                    self.stack_index = 10
                elif self.internal_time // 8 == 3:
                    self.stack_index = 11
                elif self.internal_time // 8 == 4:
                    self.stack_index = 12
                elif self.internal_time // 8 == 5:
                    self.stack_index = 13
                else:
                    self.internal_time = 8

        else:
            self.internal_time = 0
            self.stack_index = 0

        self.internal_time += 1


        """ RUNNING / WALKING MOVEMENT """
        if self.vehicle != None:
            self.position = self.vehicle.position
        else:
            if self.running:
                speed_limit = self.run_speed_limit
            else:
                speed_limit = self.walk_speed_limit
            ax, ay = 0, 0

            if self.move_up:
                ay -= self.movespeed
            if self.move_down:
                ay += self.movespeed
            if self.move_left:
                ax -= self.movespeed
            if self.move_right:
                ax += self.movespeed

            transformed_ax = ax * cos(radians(camera.rotation)) - ay * sin(radians(camera.rotation))
            transformed_ay = ax * sin(radians(camera.rotation)) + ay * cos(radians(camera.rotation))

            if transformed_ax != 0 or transformed_ay != 0:
                norm_factor = sqrt(transformed_ax**2 + transformed_ay**2)
                transformed_ax /= norm_factor
                transformed_ay /= norm_factor

            if sqrt(self.vx**2 + self.vy**2) <= speed_limit:
                self.ax = transformed_ax * self.movespeed
                self.ay = transformed_ay * self.movespeed
            else:
                self.ax = 0
                self.ay = 0

            if self.ax != 0 or self.ay != 0:
                self.rotation = degrees(atan2(self.ay, self.ax))

            super().move()


        """ UPDATING PROJECTILES """
        for projectile in self.projectiles:
            projectile.update()
            if sqrt(projectile.vx**2 + projectile.vy**2) < self.projectile_speed / 5:
                self.projectiles.remove(projectile)



    def render(self, screen, camera, offset=[0, 0]):

        if not self.vehicle:
            super().render(screen, camera, offset)


    def handle_aiming_and_shooting(self, mouse_location_on_map):
        if self.shoot:
            startpoint_distance = sqrt(self.hitbox.size[0]**2 + self.hitbox.size[1]**2) / 2 + 20
            projectile_angle = atan2(
                mouse_location_on_map[0] - self.position[0],
                mouse_location_on_map[1] - self.position[1]
            )
            projectile_start_position = [
                self.position[0] + startpoint_distance * sin(projectile_angle),
                self.position[1] + startpoint_distance * cos(projectile_angle),
                0
            ]
            projectile_particle_system = copy.deepcopy(self.projectile_asset)
            projectile = Projectile(
                projectile_particle_system,
                projectile_start_position,
                projectile_angle,
                self.projectile_speed
            )
            self.projectiles.append(projectile)
            self.vx += sin(-projectile_angle) * projectile.mass / self.mass * projectile.start_speed
            self.vy += cos(-projectile_angle) * projectile.mass / self.mass * projectile.start_speed

        for projectile in self.projectiles:
            if projectile.elapsed_time > projectile.lifetime:
                self.projectiles.remove(projectile)




class Stairs(DynamicObject):
    def __init__(self, asset, asset_index, position, rotation):
        super().__init__(asset, asset_index, position, rotation)
        self.height = asset.height

        # CALCULATING START AND END POINTS OF STAIRS
        self.start = [
            self.position[0] - self.hitbox.size[0] / 2 * sin(radians(self.rotation) - pi/2),
            self.position[1] + self.hitbox.size[1] / 2 * cos(radians(self.rotation) - pi/2)
        ]
        self.end = [
            self.position[0] + self.hitbox.size[0] / 2 * sin(radians(self.rotation) - pi/2),
            self.position[1] - self.hitbox.size[1] / 2 * cos(radians(self.rotation) - pi/2)
        ]

        self.norm_axis = [
            (self.end[0] - self.start[0]) / self.hitbox.size[1],
            (self.end[1] - self.start[1]) / self.hitbox.size[1]
        ]


    def control_object_z_offset(self, obj):
        # PROJECTION OF OBJECT POSITION ONTO STAIR AXIS
        projection = (obj.position[0] - self.start[0])*self.norm_axis[0] + (obj.position[1] - self.start[1])*self.norm_axis[1]

        if projection < 0 or projection > self.hitbox.size[1]:
            return
        
        obj.position[2] = self.position[2] + projection / self.hitbox.size[1] * self.height
