from math import sqrt, atan2, cos, sin

class Axis:
    def __init__(self, startpoint, rotation):
        self.startpoint = startpoint
        self.rotation = rotation

    def project(self, point):
        # THIS FUNCTION CALCULATES THE LENGTH BETWEEN THE AXIS STARTING POINT
        # AND THE PROJECTION OF A POINT ONTO THE AXIS
        x_point = point[0]
        y_point = point[1]
        x_axis = self.startpoint[0]
        y_axis = self.startpoint[1]

        dist = sqrt( (x_point - x_axis)^2 + (y_point - y_axis)^2 )
        angle = atan2(y_point - y_axis, x_point - x_axis) - self.rotation
        
        projection_length = dist * cos(angle)

        return projection_length


class Hitbox:
    def __init__(self, object, size, type, colour=(255, 0, 0)):
        self.object = object
        self.size = size
        self.type = type

        # Defining edges and axes for SAT algorithm
        self.edges = []
        self.axes = []


    def get_edges(self):
        if self.type == 'rectange':

            # EDGE COORDINATES FOR NON-ROTATED HITBOX
            upper_left_0 = [self.object.position[0] - self.size[0], self.object.position[0] - self.size[1]]
            upper_right_0 = [self.object.position[0] + self.size[0], self.object.position[0] - self.size[1]]
            lower_left_0 = [self.object.position[0] - self.size[0], self.object.position[0] + self.size[1]]
            lower_right_0 = [self.object.position[0] + self.size[0], self.object.position[0] + self.size[1]]
            points_0 = [upper_left_0, upper_right_0, lower_left_0, lower_right_0]

            # GETTING EDGE COORDINATES FOR ROTATED HITBOX
            for point in points_0:
                rotated_x = (point[0] - self.object.position[0])*cos(self.object.rotation) - (point[1] - self.object.position[1])*sin(self.object.rotation)
                rotated_y = (point[0] - self.object.position[0])*sin(self.object.rotation) + (point[1] - self.object.position[1])*cos(self.object.rotation)
                rotated_point = [rotated_x, rotated_y]
                self.edges.append(rotated_point)


    def get_axes(self):
        self.get_edges()

        for edge_index in range(len(self.edges)-1):

            edge_1 = self.edges[edge_index]
            edge_2 = self.edges[edge_index + 1]

            dx = edge_1[0] - edge_2[0]
            dy = edge_1[1] - edge_2[1]

            axis_startpoint = [ (edge_1[0] + edge_2[0])/2, (edge_1[1] + edge_2[1])/2]
            axis_rotation = atan2(dx, dy)

            axis = Axis(axis_startpoint, axis_rotation)
            self.axes.append(axis)


    def check_collision(self, other_hitbox):
        self.get_axes()
        other_hitbox.get_axes()

        all_axes = self.axes + other_hitbox.axes

        for axis in all_axes:
            self_projections = [axis.project(edge) for edge in self.edges]
            other_projections = [axis.project(edge) for edge in other_hitbox.edges]

            self_min = min(self_projections)
            self_max = max(self_projections)
            other_min = min(other_projections)
            other_max = max(other_projections)

            if self_max < other_min or other_max < self_min:
                return False
        return True
            
