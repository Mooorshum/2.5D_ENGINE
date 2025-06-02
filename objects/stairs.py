from math import sin, cos, radians, pi

from objects.generic import DynamicObject

class Stairs(DynamicObject):
    def __init__(self, asset, asset_index, position, rotation):
        super().__init__(asset, asset_index, position, rotation)
        self.height = asset.height

        # CALCULATING START AND END POINTS OF STAIRS
        self.start = [
            self.position[0] - self.hitbox.size[0] / 2 * sin(radians(self.rotation) - pi/2),
            self.position[1] + self.hitbox.size[1] / 2 * cos(radians(self.rotation) - pi/2)
        ]
        self.end = [
            self.position[0] + self.hitbox.size[0] / 2 * sin(radians(self.rotation) - pi/2),
            self.position[1] - self.hitbox.size[1] / 2 * cos(radians(self.rotation) - pi/2)
        ]

        self.norm_axis = [
            (self.end[0] - self.start[0]) / self.hitbox.size[1],
            (self.end[1] - self.start[1]) / self.hitbox.size[1]
        ]


    def control_object_z_offset(self, obj):
        # PROJECTION OF OBJECT POSITION ONTO STAIR AXIS
        projection = (obj.position[0] - self.start[0])*self.norm_axis[0] + (obj.position[1] - self.start[1])*self.norm_axis[1]

        if projection < 0 or projection > self.hitbox.size[1]:
            return
        
        obj.position[2] = self.position[2] + projection / self.hitbox.size[1] * self.height