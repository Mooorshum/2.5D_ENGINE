from math import atan2, pi, degrees, radians, copysign

from graphics.sprite_stacks import SpritestackModel

class Building(SpritestackModel):
    def __init__(self, type=None, name=None, scale=1):
        super().__init__(type, name, scale)

        self.rotation = 0
        self.prev_camera_angle = 0
        self.max_camera_added_rotation = 5

    def rotate(self, camera_position):
        dx = camera_position[0] - self.position[0]
        dy = camera_position[1] - self.position[1]

        x_factor = dx / 100
        if abs(x_factor) > 1:
            x_factor = 1 * copysign(1, x_factor)
        y_factor = dy / 100
        if abs(y_factor) > 1:
            y_factor = 1 * copysign(1, y_factor)
        angle_to_camera = self.max_camera_added_rotation * x_factor * y_factor

        self.rotation += self.prev_camera_angle - angle_to_camera
        self.prev_camera_angle = angle_to_camera



