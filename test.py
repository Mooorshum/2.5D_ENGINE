import pygame

from graphics import grass, shrubs
from graphics.rendering import global_render
from graphics.static_objects import StaticObject
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

        self.map_width = 2000
        self.map_height = 1000

        self.camera_width = 600
        self.camera_height = 400

        self.camera = Camera(self.camera_width, self.camera_height, self.map_width, self.map_height)

        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        
        self.background = pygame.image.load("background.png").convert()





        pygame.display.set_caption("SANDBOX")
        self.clock = pygame.time.Clock()
        self.mouse_x, self.mouse_y = None, None

        self.player = Vehicle(type='vehicle', name='hippie_van', scale=1.3)
        self.player_start_position = [200, 200]
        self.player.position = [200, 200]


        self.cop = Vehicle(type='vehicle', name='cop_car', scale=1.5)
        self.cop.scale = 1.5
        self.cop.position = [400, 400]
        self.cop.rotation = 25


        self.hillbilly = Vehicle(type='vehicle', name='pickup_truck', scale=1.5)
        self.hillbilly.scale = 1.5
        self.hillbilly.position = [600, 600]
        self.hillbilly.rotation = -15


        self.shack_1 = StaticObject(type='building', name='shack', scale=2)
        self.shack_1.position = [530, 180]
        self.shack_1.rotation = -30


        self.shack_2 = StaticObject(type='building', name='shack', scale=2)
        self.shack_2.position = [200, 450]
        self.shack_2.rotation = 10



        self.barn = StaticObject(type='building', name='barn', scale=2.5)
        self.barn.position = [750, 520]
        self.barn.rotation = 50


        self.campfire = StaticObject(type='filler_object', name='campfire', scale=1.4)
        self.campfire.position = [600, 500]
        self.campfire.rotation = 30
        self.flame = flame
        self.flame.position = (self.campfire.position[0], self.campfire.position[1] - 10)

        self.grass_system = grass.GrassSystem(
            folder = 'assets/grass',
            tile_size=30,
            blades_per_tile=5,
            stiffness=0.03
        )




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


        self.game_objects = [
            self.player, self.cop, self.hillbilly,
            self.shack_1, self.shack_2, self.barn,
            self.campfire, self.flame
            ]
        self.game_objects += self.grass_system.tiles
        self.game_objects += self.shrubs.plants
        self.game_objects += self.fern.plants



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

        camera_position = self.camera.rect.center
        camera_size = (self.camera_width, self.camera_height)

        foliage_bend_objects= [self.player, self.cop]

        self.grass_system.bend_objects = foliage_bend_objects
        self.grass_system.apply_wind(1/20, self.time)


        self.shrubs.bend_objects = foliage_bend_objects
        self.fern.bend_objects = foliage_bend_objects
        

        self.player.move()
        self.cop.move()
        self.hillbilly.move()

        self.player.hitbox.handle_collision(self.cop)
        self.player.hitbox.handle_collision(self.hillbilly)
        self.cop.hitbox.handle_collision(self.hillbilly)


        self.shack_1.rotate(camera_position)
        self.shack_2.rotate(camera_position)
        self.barn.rotate(camera_position)

    
        self.flame.update()
        


        global_render(
            self.screen,
            self.game_objects,
            camera_size,
            camera_position,
            bend_objects=foliage_bend_objects,
            offset=offset
        )
        self.player.hitbox.draw(self.screen, offset=offset)
        self.cop.hitbox.draw(self.screen, offset=offset)
        self.hillbilly.hitbox.draw(self.screen, offset=offset)


        display_fps(self.screen, self.clock, font)


        self.time += 1

        pygame.display.update()
        self.clock.tick(110)


if __name__ == "__main__":
    game = Game()
    game.run()
