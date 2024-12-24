import os

import pygame

import random
from math import sin, cos, pi, radians, sqrt, atan2


WHITE = (255, 255, 255)


class Particle:
    def __init__(self, start_position, colour, radius, lifetime):
        self.position = start_position
        self.colour = colour
        self.lifetime = lifetime
        self.r = radius
        self.opacity = 1

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
        offset_x = camera.position[0] - self.position[0] + (self.position[0] - camera.position[0]) * cos(camera_rotation) - (self.position[1] - camera.position[1]) * sin(camera_rotation)
        offset_y = camera.position[1] - self.position[1] + (self.position[0] - camera.position[0]) * sin(camera_rotation) + (self.position[1] - camera.position[1]) * cos(camera_rotation)
        offset = [offset_x - camera.position[0] + camera.width / 2, offset_y - camera.position[1] + camera.height / 2]

        particle_surface = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        particle_color = (*self.colour[:3], int(self.opacity * 255))
        pygame.draw.circle(particle_surface, particle_color, (self.r, self.r), self.r)
        screen.blit(
            particle_surface,
            (
                self.position[0] + offset[0] - self.r,
                self.position[1] + offset[1] + self.position[2] - self.r,
            ),
        )


class ParticleSystem:
    def __init__(self):
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










class ImageParticle(Particle):
    def __init__(self, start_position, image, lifetime):
        super().__init__(start_position, WHITE, 0, lifetime)
        self.image = image
        self.opacity = 0
        self.scale_factor = 0
        self.total_lifetime = lifetime

    def draw(self, screen, camera):
        camera_rotation = radians(camera.rotation)
        offset_x = camera.position[0] - self.position[0] + (self.position[0] - camera.position[0]) * cos(camera_rotation) - (self.position[1] - camera.position[1]) * sin(camera_rotation)
        offset_y = camera.position[1] - self.position[1] + (self.position[0] - camera.position[0]) * sin(camera_rotation) + (self.position[1] - camera.position[1]) * cos(camera_rotation)
        offset = [offset_x - camera.position[0] + camera.width / 2, offset_y - camera.position[1] + camera.height / 2]

        if self.image:
            """ CHANGE THIS TO BE A FOGSYSTEM PARAMETER !!!!!!!!!!!!!!!!! """
            scale = 0.25 

            image = self.image
            pygame.transform.scale(image, (image.get_width()* scale, image.get_height() * scale))
            image.set_alpha(int(self.opacity))
            screen.blit(
                image,
                (
                    self.position[0] + offset[0],
                    self.position[1] + offset[1] + self.position[2],
                )
            )


class FogCloud(ParticleSystem):
    def __init__(self, cloud_size=(100, 50, 30), max_particle_radius=50, max_cloud_opacity=1, images=None):
        super().__init__()
        self.cloud_size = cloud_size
        self.max_particle_radius = max_particle_radius
        self.max_cloud_opacity = max_cloud_opacity
        self.images = images if images else []

        self.y0_offset = cloud_size[1]/2

    def create_particle(self):
        if len(self.particles) < self.max_count and self.images:
            lifetime = random.randint(self.lifetime_range[0], self.lifetime_range[1])
            particle_x = self.position[0] + random.randint(-self.cloud_size[0] // 2, self.cloud_size[0] // 2)
            particle_y = self.position[1] + random.randint(-self.cloud_size[1] // 2, self.cloud_size[1] // 2)
            particle_z = self.position[2] + random.randint(-self.cloud_size[2] // 2, self.cloud_size[2] // 2)
            image = random.choice(self.images)
            particle = ImageParticle([particle_x, particle_y, particle_z], image, lifetime)
            self.particles.append(particle)

    def update(self, camera, ):
        self.create_particle()
        for particle in self.particles[:]:
            if particle.lifetime <= 0:
                self.particles.remove(particle)
                continue


            particle.move()
            particle.lifetime -= 1

            total_lifetime = particle.total_lifetime
            elapsed_time = total_lifetime - particle.lifetime

            # Scaling opacity with particle lifetime
            opacity_factor = 1 - ((2 * elapsed_time - total_lifetime) / total_lifetime) ** 4

            # Adjusting opacity based on camera distance
            max_camera_distance = 300
            distance = sqrt((camera.position[0] - particle.position[0]) ** 2 + (camera.position[1] - particle.position[1]) ** 2)
            distance_factor = min(1, (distance / max_camera_distance)**2)
            particle.opacity = distance_factor * self.max_cloud_opacity * opacity_factor * 255

            dx = particle.position[0] - camera.position[0]
            dy = particle.position[1] - camera.position[1]
            angle = atan2(dy, dx)
            distance_speed_factor = (100 / sqrt(dx**2 + dy**2))
            
            particle.ax = self.ax_system * cos(angle) * distance_speed_factor
            particle.ay = self.ay_system * sin(angle) * distance_speed_factor
            particle.vx *= 0.01
            particle.vy *= 0.01

    def render(self, screen, camera):
        for particle in self.particles:
            particle.draw(screen, camera)


class FogSystem:
    def __init__(self, cloud_size, map_size, max_particle_count, max_cloud_opacity):
        self.cloud_size = cloud_size
        self.max_particle_count = max_particle_count
        self.max_cloud_opacity = max_cloud_opacity
        
        """ LOADING CLOUD IMAGES FROM FOLDER """
        self.images = []
        self.max_cloud_size = (0, 0)
        self.images_folder = f'assets/fog/images/'
        self.num_images = len(os.listdir(self.images_folder))
        for i in range(self.num_images):
            image = (
                pygame.image.load(
                    f'{self.images_folder}image_{i}.png'
                ).convert_alpha()
            )
            self.images.append(image)

        """ GENERATING CLOUDS ON MAP """
        self.clouds = []
        points_x = map_size[0] // self.cloud_size[0]
        points_y = map_size[1] // self.cloud_size[1]
        step_x = map_size[0] / points_x
        step_y = map_size[1] / points_y
        for i in range(points_x):
            for j in range(points_y):
                x = i * step_x
                y = j * step_y
                cloud = FogCloud(
                    cloud_size=(100, 50, 30),
                    max_particle_radius=20,
                    max_cloud_opacity=self.max_cloud_opacity,
                    images=self.images
                )
                cloud.position = [x, y, 0]
                cloud.max_count = self.max_particle_count
                cloud.r_range = (5, 10)
                cloud.lifetime_range = (100, 500)
                cloud.ax_system = 10
                cloud.ay_system = 10
                cloud.az_system = -0.01
                self.clouds.append(cloud)

    def update(self, camera):
        for cloud in self.clouds:
            cloud.update(camera)


