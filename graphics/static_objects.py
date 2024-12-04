from math import atan2, pi, degrees, radians

from graphics.sprite_stacks import SpritestackModel

class Building(SpritestackModel):
    def __init__(self, type=None, name=None, scale=1):
        super().__init__(type, name, scale)

        self.rotation = 0
        self.prev_camera_angle = 0

    def rotate(self, camera_position):
        angle_eps = 0.01
        dx = camera_position[0] - self.position[0]
        dy = camera_position[1] - self.position[1]

        angle_to_camera = degrees(abs(atan2(dy, dx))/2 )
        self.rotation -= self.prev_camera_angle - angle_to_camera
        self.prev_camera_angle = angle_to_camera



