import pygame
from math import sin, cos, pi, radians, atan2, sqrt
from numpy import sign



class Hitbox:
    def __init__(self, object):
        self.object = object

        self.colour =  (255, 0, 0)
        self.type = 'circle'

    def draw(self, screen, offset=[0, 0]):
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
            hitbox_rect = hitbox_surface.get_rect(
                center=(
                    self.object.position[0] + offset[0],
                    self.object.position[1] + offset[1],
                )
            )
            screen.blit(hitbox_surface, hitbox_rect.topleft)




    def handle_collision(self,  colliding_object):
        displacement = 2
        damping = 0.6
        if self.type == 'circle' and colliding_object.hitbox.type == 'circle':
            dx = (self.object.position[0]) - (colliding_object.position[0])
            dy = (self.object.position[1]) - (colliding_object.position[1])
            distance = sqrt(dx**2 + dy**2)
            if distance < self.object.hitbox_size[1]//2 + colliding_object.hitbox_size[1]//2 and distance > 0:

                object_vx = self.object.vx
                object_vy = self.object.vy

                colliding_object_vx = colliding_object.vx
                colliding_object_vy = colliding_object.vy

                normal_x = dx/distance
                normal_y = dy/distance

                relative_velocity_x = object_vx - colliding_object_vx
                relative_velocity_y = object_vy - colliding_object_vy

                velocity_normal = (relative_velocity_x * normal_x) + (relative_velocity_y * normal_y)

                impulse = (2 * velocity_normal) / (self.object.mass + colliding_object.mass)

                object_vx -= impulse * colliding_object.mass * normal_x * damping
                object_vy -= impulse * colliding_object.mass * normal_y * damping

                colliding_object_vx += impulse * self.object.mass * normal_x
                colliding_object_vy += impulse * self.object.mass * normal_y

                self.object.vx = object_vx
                self.object.vy = object_vy

                colliding_object.vx = colliding_object_vx
                colliding_object.vy = colliding_object_vy

                if not self.object.movelocked:
                    self.object.position[0] += displacement * normal_x
                    self.object.position[1] += displacement * normal_y
                if not colliding_object.movelocked:
                    colliding_object.position[0] -= displacement * normal_x
                    colliding_object.position[1] -= displacement * normal_y


                """ APPLY A COLLISION-DIRECTION DEPENDENT SPIN """
                SPIN_SENSITIVITY = 1

                dx = colliding_object.position[0] - self.object.position[0]
                dy = colliding_object.position[1] - self.object.position[1]

                distance = sqrt(dx**2 + dy**2)

                global_coordinates_relative_v_angle = atan2(dy, dx) # ALPHA
                object_coordinates_relative_v_angle = global_coordinates_relative_v_angle + radians(colliding_object.rotation) # BETA

                global_coordinates_relative_vx = colliding_object.vx - self.object.vx
                global_coordinates_relative_vy = colliding_object.vy - self.object.vy

                cos_object_rotation = cos(radians(colliding_object.rotation))
                sin_object_rotation = sin(radians(colliding_object.rotation))

                object_coordinates_relative_vy = -global_coordinates_relative_vx * sin_object_rotation + global_coordinates_relative_vy * cos_object_rotation
                
                spin_v_factor = object_coordinates_relative_vy
                spin_collision_offset_factor =  cos(global_coordinates_relative_v_angle + object_coordinates_relative_v_angle)
                
                if object_coordinates_relative_v_angle % 2*pi > -pi/2 and object_coordinates_relative_v_angle % 2*pi < pi/2:
                    spin_direction_factor = 1
                else:
                    spin_direction_factor = -1

                colliding_object.omega += spin_v_factor * spin_direction_factor * spin_collision_offset_factor * SPIN_SENSITIVITY * self.object.mass / (self.object.mass + colliding_object.mass)
                self.object.omega -= spin_v_factor * spin_direction_factor * spin_collision_offset_factor * SPIN_SENSITIVITY * colliding_object.mass / (colliding_object.mass + colliding_object.mass)
