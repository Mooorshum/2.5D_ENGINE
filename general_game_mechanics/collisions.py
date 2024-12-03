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
                object_vx = self.object.linear_speed*cos(radians(self.object.rotation))
                object_vy = self.object.linear_speed*sin(radians(self.object.rotation))
                colliding_object_vx = colliding_object.linear_speed*cos(radians(colliding_object.rotation))
                colliding_object_vy = colliding_object.linear_speed*sin(radians(colliding_object.rotation))

                normal_x = dx/distance
                normal_y = dy/distance

                relative_velocity_x = object_vx - colliding_object_vx
                relative_velocity_y = object_vy - colliding_object_vy

                velocity_normal = (relative_velocity_x * normal_x) + (relative_velocity_y * normal_y)

                impulse = (2 * velocity_normal) / (self.object.mass + colliding_object.mass)

                object_vx -= impulse * colliding_object.mass * normal_x
                object_vy -= impulse * colliding_object.mass * normal_y
                object_rotation_new = abs(atan2(object_vx, object_vy))
                self.object.linear_speed = sqrt(object_vx**2 + object_vy**2)
                self.object.angular_speed = (object_rotation_new - self.object.rotation) * self.object.anglular_acceleration

                colliding_object_vx += impulse * self.object.mass * normal_x
                colliding_object_vy += impulse * self.object.mass * normal_y
                colliding_object_rotation_new = -abs(atan2(colliding_object_vx, colliding_object_vy))
                colliding_object.linear_speed = sqrt(colliding_object_vx**2 + colliding_object_vy**2)
                colliding_object.angular_speed = (colliding_object_rotation_new - colliding_object.rotation) * colliding_object.anglular_acceleration


                """ object_rotation_diff = self.object.rotation - atan2(object_vx, object_vy)
                colliding_object_rotation_diff = colliding_object.rotation - atan2(colliding_object_vx, colliding_object_vy) """
                rotation_diff = self.object.rotation - colliding_object.rotation

                """ self.object.angular_speed = -rotation_diff
                colliding_object.angular_speed = rotation_diff """

                self.object.position[0] += displacement * normal_x
                self.object.position[1] += displacement * normal_y
                colliding_object.position[0] -= displacement * normal_x
                colliding_object.position[1] -= displacement * normal_y
