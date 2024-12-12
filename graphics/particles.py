import pygame

import random
from math import sin, cos, pi, radians


WHITE = (255, 255, 255)


class Particle:
    def __init__(self, start_position, colour, radius, lifetime):
        self.position = start_position
        self.colour = colour
        self.lifetime = lifetime
        self.r = radius

        self.vx = 0
        self.vy = 0
        self.vz = 0

        self.ax = 0
        self.ay = 0
        self.az = 0

        self.drag_x = 2
        self.drag_y = 0.8
        self.drag_z = 0

        self.damping = 0.5
        self.dt = 0.1
        self.displacement_boundary_collisions = 2

    def move(self):
        self.vx += self.ax * self.dt - self.vx*self.drag_x
        self.vy += self.ay * self.dt - self.vy*self.drag_y
        self.vz += self.az * self.dt - self.vz*self.drag_z
        new_x = self.position[0] + self.vx * self.dt
        new_y = self.position[1] + self.vy * self.dt
        new_z = self.position[2] + self.vz * self.dt
        self.position = (new_x, new_y, new_z)

    def draw(self, screen, camera):
        camera_rotation = radians(camera.rotation)
        offset_x = camera.position[0] - self.position[0] + (self.position[0] - camera.position[0])*cos(camera_rotation) - (self.position[1] - camera.position[1])*sin(camera_rotation)
        offset_y = camera.position[1] - self.position[1] + (self.position[0] - camera.position[0])*sin(camera_rotation) + (self.position[1] - camera.position[1])*cos(camera_rotation)
        offset = [offset_x - camera.position[0] + camera.width/2, offset_y - camera.position[1] + camera.height/2]
        pygame.draw.circle(
            screen,
            self.colour,
            [
                self.position[0] + offset[0],
                self.position[1] + offset[1] + self.position[2]
            ],
            self.r,
            0)


class ParticleSystem:
    def __init__(
        self,
    ):
        self.position = [0, 0, 0]
        self.max_count = 0
        self.r_range = ()
        self.lifetime_range = ()
        self.acceleration_range_x = (0, 0)
        self.acceleration_range_y = (0, 0)
        self.acceleration_range_z = (0, 0)
        self.particles = []
        self.ax_system = 0
        self.ay_system = 0
        self.az_system = 0

        self.y0_offset = 0

        
    def create_particle(self):
        if len(self.particles) < self.max_count:
            colour = random.choice(self.colours)
            radius = random.randint(self.r_range[0], self.r_range[1])
            lifetime = random.randint(self.lifetime_range[0], self.lifetime_range[1])
            particle = Particle(self.position, colour, radius, lifetime)
            angle = random.uniform(0, 2 * pi)
            acceleration_x = random.randint(self.acceleration_range_x[0], self.acceleration_range_x[1])
            acceleration_y = random.randint(self.acceleration_range_y[0], self.acceleration_range_y[1])
            acceleration_z = random.randint(self.acceleration_range_z[0], self.acceleration_range_z[1])
            particle.ax = self.ax_system + acceleration_x * cos(angle)
            particle.ay = self.ay_system + acceleration_y * sin(angle)
            particle.az = self.az_system - acceleration_z
            self.particles.append(particle)

    def update(self):
        self.create_particle()
        for particle in self.particles[:]:
            particle.move()
            particle.lifetime -= 1
            particle.r -= particle.r/(particle.lifetime + 1)
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def render(self, screen, camera):
        for particle in self.particles:
            particle.draw(screen, camera)
