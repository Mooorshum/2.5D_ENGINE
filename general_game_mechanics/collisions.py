import pygame
from math import sin, cos, pi, radians, atan2, sqrt
from numpy import sign



class Hitbox:
    def __init__(self, object):
        self.object = object 

        self.colour =  (255, 0, 0)
        self.type = 'circle'

    def draw(self, screen):
        if self.type == 'box':
            hitbox_surface = pygame.Surface(self.object.hitbox_size, pygame.SRCALPHA)
            pygame.draw.rect(hitbox_surface, self.colour, 
                             pygame.Rect(0, 0, *self.object.hitbox_size), 3)
            rotated_surface = pygame.transform.rotate(hitbox_surface, self.object.rotation)
            rotated_rect = rotated_surface.get_rect(center=self.object.position)
            screen.blit(rotated_surface, rotated_rect.topleft)

        if self.type == 'circle':
            hitbox_surface = pygame.Surface(self.object.hitbox_size, pygame.SRCALPHA)
            pygame.draw.circle(
                hitbox_surface, 
                self.colour, 
                (self.object.hitbox_size[0] // 2, self.object.hitbox_size[1] // 2), 
                self.object.hitbox_size[0] // 2, 
                3
            )
            hitbox_rect = hitbox_surface.get_rect(center=self.object.position)
            screen.blit(hitbox_surface, hitbox_rect.topleft)
            



    def handle_collision(self,  colliding_object):
        displacement = 1
        if self.type == 'circle' and colliding_object.hitbox.type == 'circle':
            dx = (self.object.position[0]) - (colliding_object.position[0])
            dy = (self.object.position[1]) - (colliding_object.position[1])
            distance = sqrt(dx**2 + dy**2)
            if distance < self.object.hitbox_size[1]//2 + colliding_object.hitbox_size[1]//2 and distance > 0:
                normal_x = dx/distance
                normal_y = dy/distance
                relative_velocity_x = self.object.vx - colliding_object.vx
                relative_velocity_y = self.object.vy - colliding_object.vy
                velocity_normal = (relative_velocity_x * normal_x) + (relative_velocity_y * normal_y)
                impulse = (2 * velocity_normal) / (self.object.mass + colliding_object.mass)
                self.object.vx -= impulse * colliding_object.mass * normal_x
                self.object.vy -= impulse * colliding_object.mass * normal_y
                colliding_object.vx += impulse * self.object.mass * normal_x
                colliding_object.vy += impulse * self.object.mass * normal_y
                self.object.position[0] += displacement * normal_x
                self.object.position[1] += displacement * normal_y
                colliding_object.position[0] -= displacement * normal_x
                colliding_object.position[1] -= displacement * normal_y
