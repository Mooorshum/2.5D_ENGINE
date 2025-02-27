import pygame

from math import sqrt

from general_game_mechanics.collisions import Hitbox

class LoadPoint:
    def __init__(self, level, level_index=0, position=[0, 0], size=20, colour=(255, 255, 0)):
        self.level_index = level_index
        self.level = level
        self.position = position
        self.size = size
        self.colour = colour
        self.y0_offset = -1000
        self.marker_opacity = 0.5

        # PROPERTIES REQUIRED FOR TOPOLOGICAL DEPTH SORTING
        self.rotation = 0
        self.height = 20
        self.hitbox = Hitbox(
            object=self,
            size=(self.size, self.size),
            render_box_size=(self.size, self.size),
            type='circle'
        )
        self.movelocked = True
        self.interactable = False

    def handle_loading(self, player, game):
        self.marker_opacity = 0.25
        dx = player.position[0] - self.position[0]
        dy = player.position[1] - self.position[1]
        if sqrt(dx**2 + dy**2) < self.size:
            self.marker_opacity = 0.5
            if player.action:
                game.current_level.save_level()
                self.level.load_level()
                game.current_level = self.level
                

    def render(self, screen, offset=[0, 0]):
        temp_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            temp_surface,
            (*self.colour, int(255*self.marker_opacity)),
            (self.size, self.size),
            self.size
        )

        screen.blit(
            temp_surface,
            (
                self.position[0] + offset[0] - self.size,
                self.position[1] + offset[1] - self.size
            )
        )