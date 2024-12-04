import pygame

from math import sqrt


class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.map_width = map_width
        self.map_height = map_height

        self.vx = 0
        self.vy = 0
        self.absolute_acceleration = 1
        self.drag = 0.1
        self.speed_limit = 10
        self.dt = 0.1

    def follow(self, position):
        dx = self.rect.x - position[0]
        dy = self.rect.y - position[1]
        distance = sqrt(dx**2 + dy**2)
        normal_direction_x = dx/distance
        normal_direction_y = dy/distance
    
        vx_new = self.vx + self.absolute_acceleration * normal_direction_x - self.drag
        vy_new = self.vy + self.absolute_acceleration * normal_direction_y - self.drag
        
        if sqrt(vx_new**2 + vy_new**2) > self.speed_limit:
            vx_new = self.speed_limit * normal_direction_x
            vy_new = self.speed_limit * normal_direction_y

        x_new = self.rect.x + self.vx * self.dt
        y_new = self.rect.y + self.vy * self.dt

        self.rect.x = max(0, min(x_new, self.map_width - self.rect.width))
        self.rect.y = max(0, min(y_new, self.map_height - self.rect.height))
