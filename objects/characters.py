import pygame

import copy

from math import sin, cos, atan2, degrees, sqrt, radians

from general_game_mechanics.inventory import GridInventory
from objects.projectiles import Projectile
from objects.generic import DynamicObject
from objects.items import Item
from assets.particle_systems import fireball



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

        self.projectile_asset = fireball
        self.projectile_speed = 50
        self.aiming = False
        self.shoot = False
        self.projectiles = []

        self.action = None

        
        self.items = []
        for i in range(5):
            item = Item()
            self.items.append(item)
        self.inventory = GridInventory(grid_size=(3, 2), items=self.items)



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


        """ UPDATING PROJECTILES """
        for projectile in self.projectiles:
            projectile.update()
            if sqrt(projectile.vx**2 + projectile.vy**2) < self.projectile_speed / 5:
                self.projectiles.remove(projectile)


    def render(self, screen, camera, offset=[0, 0]):

        if not self.vehicle:
            super().render(screen, camera, offset)
            #self.inventory.render(screen, [screen.get_width()/2, screen.get_height()/2])


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
