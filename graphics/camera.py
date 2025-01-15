import pygame

from math import sqrt

from numpy import sign


class Camera:
    def __init__(self, width, height, map_width, map_height):

        self.width = width
        self.height = height

        self.position = [0, 0]
        self.rotation = 0

        self.vx = 0
        self.vy = 0
        self.omega = 0
        self.absolute_acceleration = 200
        self.linear_drag = 0.1
        self.omega_drag = 0.05
        self.linear_speed_limit = 500
        self.max_omega = 20
        self.dt = 0.1

        self.map_width = map_width
        self.map_height = map_height

        self.rotate_left = False
        self.rotate_right = False
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.Move_down = False


    def follow(self, position):
        distance_threshold = 20
        velocity_threshold = 20

        dx = position[0] - self.position[0]
        dy = position[1] - self.position[1]
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



    def align(self, rotation):
        if not (self.rotate_left or self.rotate_right):
            align_factor = 0.3
            angle_diff = (rotation - self.rotation)
            self.omega += angle_diff*align_factor




    def handle_movement(self, keys):
        self.rotate_left = keys[pygame.K_q]
        self.rotate_right = keys[pygame.K_e]
        self.move_left = keys[pygame.K_LEFT]
        self.move_right = keys[pygame.K_RIGHT]
        self.move_up = keys[pygame.K_UP]
        self.Move_down = keys[pygame.K_DOWN]

    def move(self):

        """ CAMERA ROTATION """
        turn_speed = 1
        
        self.rotation = self.rotation % 360
        if self.rotate_left:
            self.omega += turn_speed
        if self.rotate_right:
            self.omega -= turn_speed

        if abs(self.omega) > self.max_omega:
            self.omega = sign(self.omega) * self.max_omega

        self.rotation += self.omega * self.dt
        self.omega *= 1 - self.omega_drag

        self.vx *= (1 - self.linear_drag)
        self.vy *= (1 - self.linear_drag)


        """ CAMERA MOVEMENT """
        speed = sqrt(self.vx**2 + self.vy**2)
        if speed > self.linear_speed_limit:
            self.vx = (self.vx / speed) * self.speed_limit
            self.vy = (self.vy / speed) * self.speed_limit

        self.position[0] += self.vx * self.dt
        self.position[1] += self.vy * self.dt

        # Preventing camera from going out of map bounds
        if self.position[0] < self.width/2:
            self.position[0] = self.width/2
        if self.position[0] > self.map_width - self.width/2:
            self.position[0] = self.map_width - self.width/2

        if self.position[1] < self.height/2:
            self.position[1] = self.height/2
        if self.position[1] > self.map_height - self.height/2:
            self.position[1] = self.map_height - self.height/2

