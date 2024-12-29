import pygame

from math import sin, cos

from graphics import grass, plants
from graphics.particles import ParticleSystem
from graphics.static_objects import Building
from world.particle_presets import flame
from general_game_mechanics.dynamic_objects import Vehicle

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
        self.screen_width = 800
        self.screen_height = 500

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("background.png").convert()

        pygame.display.set_caption("SANDBOX")
        self.clock = pygame.time.Clock()
        self.mouse_x, self.mouse_y = None, None

        self.flame = flame
        self.flame.x = 300
        self.flame.y = 300

        self.player = Vehicle(type='vehicle', name='hippie_van', scale=1.5)
        self.player.position = [200, 200]


        self.cop = Vehicle(type='vehicle', name='cop_car', scale=1.5)
        self.cop.scale = 1.5
        self.cop.position = [self.screen_width//2, self.screen_height//2]


        self.grass_system = grass.GrassSystem()
        self.grass_system.blades_per_tile = 20
        for x in range (self.grass_system.tile_size, self.screen_width, self.grass_system.tile_size):
            for y in range (self.grass_system.tile_size, self.screen_height, self.grass_system.tile_size):
                self.grass_system.create_new_tile((x, y), 'assets/grass')
        self.grass_system.sort_tiles()

        self.wheat_system = grass.GrassSystem()
        self.wheat_system.blades_per_tile = 3
        for x in range (self.wheat_system.tile_size, self.screen_width, self.wheat_system.tile_size):
            for y in range (self.wheat_system.tile_size, self.screen_height, self.wheat_system.tile_size):
                self.wheat_system.create_new_tile((x, y), 'assets/wheat')
        self.wheat_system.sort_tiles()


        self.shack = Building(type='building', name='shack', scale=2.5)
        self.shack.position = [600, 200]
        self.shack.rotation = -30



        self.shrubs = plants.PlantSystem(
            folder='assets/branchy_bush',
            num_branches_range = (1,7),
            base_angle_range = (-1, 1),
            stiffness_range = (0.01, 0.2),
            gravity = 0.1,
            density = 1 
            )


        self.fern = plants.PlantSystem(
            folder='assets/fern',
            num_branches_range = (3,7),
            base_angle_range = (-2, 2),
            stiffness_range = (0.01, 0.2),
            gravity = 0.1,
            density = 1
            )





        self.time = 0





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

        

    def update_screen_game(self, time_delta : float):
        display_fps(self.screen, self.clock, font)

        grass_bend_objects= [self.player, self.cop]

        self.grass_system.render_grass_tiles(self.screen, grass_bend_objects)
        self.grass_system.apply_wind(1/20, self.time)

        self.wheat_system.render_grass_tiles(self.screen, grass_bend_objects)
        self.wheat_system.apply_wind(1/20, self.time)
        


        self.shrubs.bendpoints = [self.player.position, self.cop.position]
        self.shrubs.render(self.screen)

        self.fern.bendpoints = [self.player.position, self.cop.position]
        self.fern.render(self.screen)



        """ self.shack.draw(self.screen, spread=0.9) """


        self.cop.draw_dust(self.screen)
        self.cop.draw(self.screen)
        self.cop.hitbox.draw(self.screen)
        self.cop.move()


        self.player.draw_dust(self.screen)
        self.player.draw(self.screen)
        self.player.hitbox.draw(self.screen)
        
        self.player.move()

        self.player.hitbox.handle_collision(self.cop)


        self.flame.update_particles()
        self.flame.draw_particles(self.screen)
        self.flame.position = (self.mouse_x ,self.mouse_y)









        self.time += 1

        pygame.display.update()
        self.clock.tick(110)


if __name__ == "__main__":
    game = Game()
    game.run()