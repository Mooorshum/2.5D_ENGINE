import pygame

import random
from math import sin, cos, pi


WHITE = (255, 255, 255)


class Particle:
    def __init__(self, x_start, y_start, colour, radius, lifetime):
        self.x = x_start
        self.y = y_start
        self.colour = colour
        self.lifetime = lifetime
        self.r = radius
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.mass = 1
        self.drag_x = 2
        self.drag_y = 0.8
        self.damping = 0.5
        self.dt = 0.1
        self.displacement_boundary_collisions = 2

    def move(self, background_hitbox):
        self.vx += self.ax * self.dt - self.vx*self.drag_x
        self.vy += self.ay * self.dt - self.vy*self.drag_y
        new_x = self.x + self.vx * self.dt
        new_y = self.y + self.vy * self.dt
        if background_hitbox:
            try:
                hit_boundary_top = background_hitbox.get_at((int(new_x + self.r), int(new_y))) != WHITE
                hit_boundary_bottom = background_hitbox.get_at((int(new_x + self.r), int(new_y + 2*self.r))) != WHITE
                hit_boundary_left = background_hitbox.get_at((int(new_x), int(new_y + self.r))) != WHITE
                hit_boundary_right = background_hitbox.get_at((int(new_x + 2*self.r), int(new_y + self.r))) != WHITE
                if hit_boundary_top:
                    self.vy = -self.vy * (1 - self.damping)
                if hit_boundary_bottom:
                    self.vy = -self.vy * (1 - self.damping)
                if hit_boundary_left:
                    self.vx = -self.vx * (1 - self.damping)
                if hit_boundary_right:
                    self.vx = -self.vx * (1 - self.damping)
                if hit_boundary_top:
                    new_y += self.displacement_boundary_collisions
                if hit_boundary_bottom:
                    new_y -= self.displacement_boundary_collisions
                if hit_boundary_left:
                    new_x += self.displacement_boundary_collisions
                if hit_boundary_right:  
                    new_x -= self.displacement_boundary_collisions
            except IndexError:
                self.vx, self.vy = 0, 0
        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r, 0)


class ParticleSystem:
    def __init__(
        self,
    ):
        self.x = 0
        self.y = 0
        self.max_count = 0
        self.r_range = ()
        self.opacity_range = None
        self.lifetime_range = ()
        self.acceleration_range = ()
        self.particles = []
        self.background_hitbox = None
        self.ax_system = 0
        self.ay_system = 0

    def create_particle(self):
        if len(self.particles) < self.max_count:
            colour = random.choice(self.colours)
            radius = random.randint(self.r_range[0], self.r_range[1])
            lifetime = random.randint(self.lifetime_range[0], self.lifetime_range[1])
            particle = Particle(self.x, self.y, colour, radius, lifetime)
            angle = random.uniform(0, 2 * pi)
            acceleration = random.randint(self.acceleration_range[0], self.acceleration_range[1])
            particle.ax = self.ax_system + acceleration * cos(angle)
            particle.ay = self.ay_system + acceleration * sin(angle)
            self.particles.append(particle)

    def update_particles(self):
        self.create_particle()
        for particle in self.particles[:]:
            particle.move(self.background_hitbox)
            particle.lifetime -= 1
            particle.r -= particle.r/(particle.lifetime + 1)
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw_particles(self, screen):
        for particle in self.particles:
            particle.draw(screen)
