import pygame
import time
import os
from math import sqrt, sin, cos, atan2, degrees, hypot, ceil, asin, pi, copysign
from numpy import sign
from statistics import mean
import random

from graphics.foliage import PlantSystem
from graphics.particles import ParticleSystem

from map_effects.weather import Wind

from characters.players import BasicCharacter

from ui.menu import MainMenu
from ui import START_GAME_EVENT
pygame.init()

from enum import Enum

class GameStates(Enum):
    PLAYING = 1
    PAUSED = 2
    AT_EXIT = 3




font = pygame.font.SysFont(None, 20)

def display_fps(screen, clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f'fps: {fps}', True, pygame.Color("white"))
    screen_width, screen_height = screen.get_size()
    text_rect = fps_text.get_rect(topright=(screen_width - 10, 10))
    screen.blit(fps_text, text_rect)







class Game:
    def __init__(self):
        self.game_state = GameStates.PAUSED
        self.screen_width = 960
        self.screen_height = 541

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("background.png").convert()
        self.background
        self.background_hitbox = pygame.image.load("background_hitbox.png").convert()

        pygame.display.set_caption("SANDBOX")
        self.clock = pygame.time.Clock()
        self.mouse_x, self.mouse_y = None, None

        self.wind = Wind()
        self.wind.amplitudes = [0.005, 0.03, 0.02, 0.05]
        self.wind.frequencies = [0.1, 0.05, 0.02, 0.005]

    
        self.flame = ParticleSystem()
        YELLOW = (255, 255, 0)
        FLAME_ORANGE_1 = (255, 240, 0)
        FLAME_ORANGE_2 = (255, 230, 0)
        FLAME_ORANGE_3 = (255, 220, 0)
        FLAME_ORANGE_4 = (255, 200, 0)
        FLAME_ORANGE_5 = (255, 180, 0)
        FLAME_ORANGE_6 = (255, 160, 0)
        FLAME_ORANGE_7 = (255, 140, 0)
        FLAME_ORANGE_8 = (255, 120, 0)
        FLAME_ORANGE_9 = (255, 100, 0)
        RED = (255, 0, 0)
        self.flame.colours = (
            YELLOW, 
            FLAME_ORANGE_1, FLAME_ORANGE_2, FLAME_ORANGE_3,
            FLAME_ORANGE_4, FLAME_ORANGE_5, FLAME_ORANGE_6,
            FLAME_ORANGE_7, FLAME_ORANGE_8, FLAME_ORANGE_9
        )
        self.flame.background_hitbox = self.background_hitbox
        self.flame.max_count = 100
        self.flame.r_range = (1, 15)
        self.flame.lifetime_range = (10, 80)
        self.flame.acceleration_range = (20, 100)
        self.flame.ay_system = -150

        self.shrubs = PlantSystem(plant_folder='assets/images/plants/branchy_bush')
        self.shrubs.mask_name = 'test_mask'
        self.shrubs.num_leaves_range = (1,10)
        self.shrubs.stiffness_range = (0.005, 0.05)
        self.shrubs.root_stiffness_range = (0.01, 0.1)
        self.shrubs.density = 0.5
        self.shrubs.generate_plants()

        self.grass = PlantSystem(plant_folder='assets/images/plants/grass')
        self.grass.mask_name = 'test_mask'
        self.grass.num_leaves_range = (1,3)
        self.grass.stiffness_range = (0.01, 0.1)
        self.grass.root_stiffness_range = (0.01, 0.1)
        self.grass.density = 1
        self.grass.generate_plants()

        self.flower = PlantSystem(plant_folder='assets/images/plants/flower')
        self.flower.mask_name = 'test_mask'
        self.flower.num_leaves_range = (1,1)
        self.flower.stiffness_range = (0.02, 0.04)
        self.flower.root_stiffness_range = (0.1, 0.2)
        self.flower.density = 0.5
        self.flower.generate_plants()

        self.fern = PlantSystem(plant_folder='assets/images/plants/fern')
        self.fern.mask_name = 'test_mask'
        self.fern.num_leaves_range = (3,7)
        self.fern.stiffness_range = (0.01, 0.1)
        self.fern.root_stiffness_range = (0.01, 0.1)
        self.fern.density = 0.2
        self.fern.generate_plants()

        self.player = BasicCharacter(character_folder='assets/images/characters/cop_car')

        self.main_menu = MainMenu(pygame.display.get_surface().size)



    def run(self):
        clock = pygame.time.Clock()
        while self.game_state != GameStates.AT_EXIT:
            time_delta = clock.tick(60) / 1000.0
            self.handle_events()
            if self.game_state == GameStates.PLAYING:
                self.screen.blit(self.background, (0, 0))
                self.update_screen_game(time_delta)
            elif self.game_state == GameStates.PAUSED:
                self.screen.blit(self.background, (0, 0))
                self.main_menu.draw(self.screen, time_delta)
                pygame.display.update()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameStates.AT_EXIT

            else:
                if event.type == START_GAME_EVENT:
                    self.main_menu.hide()
                    self.game_state = GameStates.PLAYING
                else:
                    self.main_menu.process_events(event)

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.game_state = GameStates.PAUSED
            self.main_menu.show()

        self.player.handle_movement(keys)
            
        # Generating flame at cursor location
        self.flame.x = self.mouse_x
        self.flame.y = self.mouse_y

        # Making grass bend at mouse location
        self.grass.x_player = self.player.x
        self.grass.y_player = self.player.y
        
        # Making shrubs bend at mouse location
        self.shrubs.x_player = self.player.x
        self.shrubs.y_player = self.player.y

        # Making flower bend at mouse location
        self.flower.x_player = self.player.x
        self.flower.y_player = self.player.y

        # Making fern bend at mouse location
        self.fern.x_player = self.player.x
        self.fern.y_player = self.player.y

        

    def update_screen_game(self, time_delta : float):
        #self.screen.blit(self.background, (0, 0))
        display_fps(self.screen, self.clock, font)

        self.flame.create_particle()
        self.flame.update_particles()
        self.flame.draw_particles(self.screen)

        self.fern.update_plants()
        self.fern.draw_plants(self.screen)

        self.shrubs.update_plants()
        self.shrubs.draw_plants(self.screen)

        """ self.grass.update_plants()
        self.grass.draw_plants(self.screen)

        self.flower.update_plants()
        self.flower.draw_plants(self.screen) """

        """ self.player.draw(self.screen) """
        self.player.render_stack(self.screen, spread=3, scale=0.5)

        pygame.display.update()
        self.clock.tick(110)


if __name__ == "__main__":
    game = Game()
    game.run()