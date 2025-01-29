from math import sin, cos, radians, pi, sqrt
import random
import pygame

from copy import deepcopy

from graphics.sprite_stacks import SpritestackModel
from presets.particle_presets import water_splash


class WaterBody(SpritestackModel):
    def __init__(self, asset, asset_index, position, rotation):
        super().__init__(asset, asset_index, position, rotation)

        self.splash_effect_trigger_radius = sqrt(self.asset.hitbox_size[0]**2 + self.asset.hitbox_size[1]**2)/2
        self.max_depth = -self.asset.z_offset
        self.splash_particle_systems = []

    def track_splashes_and_object_depth(self, object):
        dx = object.position[0] - self.position[0]
        dy = object.position[1] - (self.position[1] - self.z_offset_additional)
        distance = sqrt(dx**2 + dy**2)

        # CREATING A SPLASH EFFECT PARTICLE SYSTEM IF THE OBJECT IS IN THE TRIGGER RADIUS
        if distance < self.splash_effect_trigger_radius:
            if not object.ground_effect_particle_system:
                object.ground_effect_particle_system = deepcopy(water_splash)
            else:
                max_count = 5
                if sqrt(object.vx**2 + object.vy**2) < 10:
                    object.ground_effect_particle_system.max_count = 0
                else:
                    object.ground_effect_particle_system.max_count = max_count

        else:
            object.ground_effect_particle_system = None

        # CALCULATING ADDITIONAL OBJECT OFFSET (TO SIMULATE DEPTH)
        if distance < self.splash_effect_trigger_radius:
            object.z_offset_additional = -self.max_depth
        else:
            object.z_offset_additional = 0
