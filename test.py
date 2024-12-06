import pygame

from graphics import grass, shrubs
from graphics.rendering import global_render
from graphics.static_objects import Building
from general_game_mechanics.dynamic_objects import Vehicle
from graphics.camera import Camera

from world.particle_presets import flame


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

        self.map_width = 1600
        self.map_height = 1000
        self.camera_width = 600
        self.camera_height = 400

        self.camera = Camera(self.camera_width, self.camera_height, self.map_width, self.map_height)

        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        
        self.background = pygame.image.load("background_x2.png").convert()





        pygame.display.set_caption("SANDBOX")
        self.clock = pygame.time.Clock()
        self.mouse_x, self.mouse_y = None, None

        self.player = Vehicle(type='vehicle', name='hippie_van', scale=1.3)
        self.player_start_position = [200, 200]
        self.player.position = [200, 200]


        self.cop = Vehicle(type='vehicle', name='cop_car', scale=1.5)
        self.cop.scale = 1.5
        self.cop.position = [400, 400]


        self.shack_1 = Building(type='building', name='shack', scale=2)
        self.shack_1.position = [600, 200]
        self.shack_1.rotation = -30


        self.shack_2 = Building(type='building', name='shack', scale=2)
        self.shack_2.position = [200, 400]
        self.shack_2.rotation = 10


        self.flame = flame
        self.flame.position = [600, 500]

        self.grass_system = grass.GrassSystem()
        self.grass_system.blades_per_tile = 30
        for x in range (self.grass_system.tile_size, self.map_width, self.grass_system.tile_size):
            for y in range (self.grass_system.tile_size, self.map_height, self.grass_system.tile_size):
                self.grass_system.create_new_tile((x, y), 'assets/grass')
        self.grass_system.sort_tiles()


        self.wheat_system = grass.GrassSystem()
        self.wheat_system.blades_per_tile = 1
        for x in range (self.wheat_system.tile_size, self.map_width, self.wheat_system.tile_size):
            for y in range (self.wheat_system.tile_size, self.map_height, self.wheat_system.tile_size):
                self.wheat_system.create_new_tile((x, y), 'assets/wheat')
        self.wheat_system.sort_tiles()


        self.shrubs = shrubs.PlantSystem(
            folder='assets/branchy_bush',
            num_branches_range = (1,7),
            base_angle_range = (-1, 1),
            stiffness_range = (0.01, 0.2),
            gravity = 0.1,
            density = 1 
            )


        self.fern = shrubs.PlantSystem(
            folder='assets/fern',
            num_branches_range = (3,7),
            base_angle_range = (-2, 2),
            stiffness_range = (0.01, 0.2),
            gravity = 0.1,
            density = 1
            )


        self.time = 0




    def run(self):
        clock = pygame.time.Clock()
        
        while self.game_state != GameStates.AT_EXIT:
            time_delta = clock.tick(60) / 1000.0
            self.handle_events()
            if self.game_state == GameStates.PLAYING:
                self.update_screen_game(time_delta)
            elif self.game_state == GameStates.PAUSED:
                pygame.display.update()

        pygame.quit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameStates.AT_EXIT
            else:
                self.game_state = GameStates.PLAYING

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.game_state = GameStates.PAUSED

        self.player.handle_movement(keys)


    def update_screen_game(self, time_delta : float):
        display_fps(self.screen, self.clock, font)


        self.camera.follow(self.player.position)

        self.screen.blit(
            self.background,
            (0, 0),
            self.camera.rect
        )

        offset = [-self.camera.rect.x, -self.camera.rect.y]
        camera_positon = self.camera.rect.center

        foliage_bend_objects= [self.player, self.cop]

        self.grass_system.bend_objects = foliage_bend_objects
        self.grass_system.apply_wind(1/20, self.time)
        self.wheat_system.apply_wind(1/20, self.time)


        self.shrubs.bend_objects = foliage_bend_objects
        self.fern.bend_objects = foliage_bend_objects
        

        self.player.move()
        self.cop.move()
        self.player.hitbox.handle_collision(self.cop)

        self.shack_1.rotate(camera_positon)
        self.shack_2.rotate(camera_positon)

        self.flame.update()
        

        game_objects = [
            self.player, self.cop,
            self.shack_1, self.shack_2,
            self.flame
            ]
        """ game_objects += self.grass_system.tiles
        game_objects += self.wheat_system.tiles """
        game_objects += self.shrubs.plants
        game_objects += self.fern.plants
        global_render(self.screen, game_objects, bend_objects=foliage_bend_objects, offset=offset)
        self.player.hitbox.draw(self.screen, offset=offset)
        self.cop.hitbox.draw(self.screen, offset=offset)


        display_fps(self.screen, self.clock, font)


        self.time += 1

        pygame.display.update()
        self.clock.tick(110)


if __name__ == "__main__":
    game = Game()
    game.run()
