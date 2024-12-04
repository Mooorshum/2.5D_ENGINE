import pygame

from graphics.static_objects import Building
from general_game_mechanics.dynamic_objects import Vehicle
from graphics.camera import Camera


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

        self.background = pygame.image.load("background.png").convert()
        self.map_width = self.background.get_width()
        self.map_height = self.background.get_height()
        self.screen = pygame.display.set_mode((self.map_width, self.map_height))
        

        self.camera_width = 400
        self.camera_height = 250
        self.camera = Camera(self.camera_width, self.camera_height, self.map_width, self.map_height)





        

        pygame.display.set_caption("SANDBOX")
        self.clock = pygame.time.Clock()
        self.mouse_x, self.mouse_y = None, None

        self.player = Vehicle(type='vehicle', name='hippie_van', scale=1)
        self.player_start_position = [200, 200]
        self.player.position = [200, 200]


        self.shack_1 = Building(type='building', name='shack', scale=1.5)
        self.shack_1.position = [600, 200]
        self.shack_1.rotation = -30



        self.shack_2 = Building(type='building', name='shack', scale=1.5)
        self.shack_2.position = [200, 400]
        self.shack_2.rotation = 0



        self.time = 0






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




        self.player.draw_dust(self.screen)
        self.player.draw(self.screen)
        self.player.hitbox.draw(self.screen)
        self.player.move()





        self.shack_1.draw(self.screen, offset=[0, 0], spread=0.9)
        self.shack_1.rotate(self.player.position)

        print(self.player.position)


        self.shack_2.draw(self.screen, offset=[0, 0],  spread=0.9)
        self.shack_2.rotate(self.player.position)



        self.time += 1

        pygame.display.update()
        self.clock.tick(110)


if __name__ == "__main__":
    game = Game()
    game.run()
