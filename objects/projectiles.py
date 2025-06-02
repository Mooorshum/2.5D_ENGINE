from general_game_mechanics.collisions import Hitbox

from math import sin, cos


class Projectile():
    def __init__(self, particle_system, start_position, angle, speed):
        self.lifetime = 200
        self.mass = 50
        self.hitbox_size = (10, 10)
        self.hitbox_type = 'circle'
        self.movelocked = False

        self.collidable = True

        self.rotation = 0
        self.omega = 0

        self.particle_system = particle_system
        self.particle_system.position = start_position

        self.position = self.particle_system.position

        self.start_speed = speed
        self.start_angle = angle

        self.vx = self.start_speed * sin(self.start_angle)
        self.vy = self.start_speed * cos(self.start_angle)

        self.elapsed_time = 0

        self.dt = 0.1

        # PROPERTIES REQUIRED FOR TOPOLOGICAL DEPTH SORTING
        self.rotation = 0
        self.hitbox_size = (20, 20)
        self.hitbox_type = 'circle'
        self.hitbox = Hitbox(
            object=self,
            size=self.hitbox_size,
            type=self.hitbox_type
        )
        self.movelocked = False
        self.interactable = True


    def update(self):
        self.elapsed_time += 1

    def move(self):
        self.particle_system.position[0] += self.vx * self.dt
        self.particle_system.position[1] += self.vy * self.dt
        self.particle_system.update()
        self.position = self.particle_system.position
        self.hitbox.update()
        if self.hitbox.collided:
            self.vx *= 0.99
            self.vy *= 0.99

    def render(self, screen, camera):
        self.particle_system.render(screen, camera)
