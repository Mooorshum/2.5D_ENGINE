import pygame
import time
import os
from math import sqrt, sin, cos, atan2, degrees, hypot, ceil, asin, pi, copysign
from numpy import sign
from statistics import mean
import random

from foliage import PlantSystem
from particles import ParticleSystem


pygame.init()




class Wind:
    def __init__(self):
        self.t = 0
        self.dt = 0.1
        self.amplitudes = [0]
        self.frequencies = [0]

    def update(self):
        self.t += self.dt

    def get_wind_force(self):
        wind_force = 0
        for amplitude, frequency in zip(self.amplitudes, self.frequencies):
            wind_force += amplitude * sin(2 * pi * frequency * self.t)
        return wind_force



class HandlePlayerMovement:
    def __init__(self, player):
        self.player = player

    def handle_keys(self, keys):
        vx_left = 0
        vx_right = 0
        vy_up = 0
        vy_down = 0

        if keys[pygame.K_LEFT]:
            if keys[pygame.K_UP] or keys[pygame.K_UP]:
                vx_left = -sqrt(2)/2*self.player.movement_acceleration
            else:
                vx_left = -self.player.movement_acceleration

        if keys[pygame.K_RIGHT]:
            if keys[pygame.K_UP] or keys[pygame.K_UP]:
                vx_right = -sqrt(2)/2*self.player.movement_acceleration
            else:
                vx_right = self.player.movement_acceleration

        if keys[pygame.K_UP]:
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                vy_up = -sqrt(2)/2*self.player.movement_acceleration
            else:
                vy_up = -self.player.movement_acceleration

        if keys[pygame.K_DOWN]:
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                vy_down = sqrt(2)/2*self.player.movement_acceleration
            else:
                vy_down = self.player.movement_acceleration

        if keys[pygame.K_SPACE]:
           self.player.jump()

        self.player.vx = vx_left + vx_right
        self.player.vy = vy_up + vy_down



class Game:
    def __init__(self):
        self.screen_width = 962
        self.screen_height = 542
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.SCALED)
        self.background = pygame.image.load("background.png").convert()
        self.background_hitbox = pygame.image.load("background_hitbox.png").convert()

        pygame.display.set_caption("SANDBOX")
        self.clock = pygame.time.Clock()
        self.running = True
        self.mouse_x, self.mouse_y = None, None

        self.wind = Wind()
        self.wind.amplitudes = [0.005, 0.03, 0.02, 0.05]
        self.wind.frequencies = [0.1, 0.05, 0.02, 0.005]

        self.flame = ParticleSystem()
        self.flame.background_hitbox = self.background_hitbox
        self.flame.max_count = 100
        self.flame.r_range = (1, 15)
        self.flame.lifetime_range = (10, 80)
        self.flame.acceleration_range = (20, 100)

        self.shrubs = PlantSystem(plant_folder='plants/branchy_bush')
        self.shrubs.mask_name = 'test_mask'
        self.shrubs.num_leaves_range = (1,20)
        self.shrubs.stiffness_range = (0.005, 0.05)
        self.shrubs.root_stiffness_range = (0.01, 0.1)
        self.shrubs.density = 1
        self.shrubs.generate_plants()

        self.grass = PlantSystem(plant_folder='plants/grass')
        self.grass.mask_name = 'test_mask'
        self.grass.num_leaves_range = (1,3)
        self.grass.stiffness_range = (0.01, 0.1)
        self.grass.root_stiffness_range = (0.01, 0.1)
        self.grass.density = 1
        self.grass.generate_plants()

        self.flower = PlantSystem(plant_folder='plants/flower')
        self.flower.mask_name = 'test_mask'
        self.flower.num_leaves_range = (1,1)
        self.flower.stiffness_range = (0.02, 0.04)
        self.flower.root_stiffness_range = (0.1, 0.2)
        self.flower.density = 1
        self.flower.generate_plants()

    def run(self):
        while self.running:
            self.handle_events()
            self.update_screen_game()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
            
        # Generating flame at cursor location
        self.flame.x = self.mouse_x
        self.flame.y = self.mouse_y

        # Making grass bend at mouse location
        self.grass.x_player = self.mouse_x
        self.grass.y_player = self.mouse_y
        
        # Making shrubs bend at mouse location
        self.shrubs.x_player = self.mouse_x
        self.shrubs.y_player = self.mouse_y

        # Making flower bend at mouse location
        self.flower.x_player = self.mouse_x
        self.flower.y_player = self.mouse_y

    def update_screen_game(self):
        self.screen.blit(self.background, (0, 0))
        
        """ self.grass.update_grass()
        self.grass.draw_grass(self.screen) """

        self.flame.create_particle()
        self.flame.update_particles()
        self.flame.draw_particles(self.screen)

        self.shrubs.update_plants()
        self.shrubs.draw_plants(self.screen)

        self.grass.update_plants()
        self.grass.draw_plants(self.screen)

        self.flower.update_plants()
        self.flower.draw_plants(self.screen)

        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()