import pygame

from math import sqrt


class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.map_width = map_width
        self.map_height = map_height

        self.vx = 0
        self.vy = 0
        self.absolute_acceleration = 100
        self.drag = 0.1
        self.speed_limit = 400
        self.dt = 0.1

    def follow(self, position):
        distance_threshold = 20
        velocity_threshold = 20

        dx = position[0] - self.rect.centerx
        dy = position[1] - self.rect.centery
        distance = sqrt(dx**2 + dy**2)

        if distance != 0:
            normal_direction_x = dx / distance
            normal_direction_y = dy / distance
        else:
            normal_direction_x, normal_direction_y = 0, 0


        a_smooth = self.absolute_acceleration * (distance / 200)**2
        if a_smooth > self.absolute_acceleration:
            a_smooth = self.absolute_acceleration

        self.vx += a_smooth * normal_direction_x * self.dt
        self.vy += a_smooth * normal_direction_y * self.dt

        if (distance < distance_threshold) and (sqrt(self.vx**2 + self.vy**2) < velocity_threshold):
            self.vx = 0
            self.vy = 0

        self.vx *= (1 - self.drag)
        self.vy *= (1 - self.drag)

        speed = sqrt(self.vx**2 + self.vy**2)
        if speed > self.speed_limit:
            self.vx = (self.vx / speed) * self.speed_limit
            self.vy = (self.vy / speed) * self.speed_limit

        self.rect.x += self.vx * self.dt
        self.rect.y += self.vy * self.dt

        self.rect.x = max(0, min(self.rect.x, self.map_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.map_height - self.rect.height))
