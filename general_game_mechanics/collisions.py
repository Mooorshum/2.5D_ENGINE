import pygame
from math import sin, cos, pi, radians, atan2, sqrt
from numpy import sign


class Hitbox:
    def __init__(self, object, size, type, colour=(255, 0, 0)):
        self.object = object
        self.size = size
        self.type = type

        self.colour = colour

        self.contact_point = [0, 0]

        self.collided = False

        # Defining edges and axes for SAT algorithm
        self.vertices = []
        self.axes = []

        self.mtv_axis_normalized = [0, 0]

    def get_vertices(self):
        self.vertices = []

        # VERTICES FOR RECTANGULAR HITBOX
        if self.type == 'rectangle':
            # VERTEX COORDINATES IN OBJECT REFERENCE FRAME
            upper_left_0 = [-self.size[0]/2, -self.size[1]/2]
            upper_right_0 = [self.size[0]/2, -self.size[1]/2]
            lower_left_0 = [-self.size[0]/2, self.size[1]/2]
            lower_right_0 = [self.size[0]/2, self.size[1]/2]
            vertices_0 = [
                upper_left_0,
                upper_right_0,
                lower_right_0,
                lower_left_0,
            ]

        # VERTICES FOR CIRCULAR HITBOX
        if self.type == 'circle':
            # VERTEX COORDINATES IN OBJECT REFERENCE FRAME
            vertex_count = 6
            vertices_0 = []
            for phi_degrees in range(0, 360, int(360/vertex_count)):
                phi = radians(phi_degrees)
                vertex = [self.size[0]/2 * cos(phi), self.size[1]/2 * sin(phi)]
                vertices_0.append(vertex)

        # GETTING VERTEX COORDINATES FOR ROTATED HITBOX
        object_rotation = -radians(self.object.rotation)
        for vertex in vertices_0:
            rotated_vertex_x = vertex[0] * cos(object_rotation) - vertex[1] * sin(object_rotation)
            rotated_vertex_y = vertex[1] * cos(object_rotation) + vertex[0] * sin(object_rotation)
            rotated_vertex = [self.object.position[0] + rotated_vertex_x, self.object.position[1] + rotated_vertex_y]
            self.vertices.append(rotated_vertex)


    def get_axes(self):
        self.get_vertices()
        self.axes = []

        for vertex_index in range(len(self.vertices)):

            vertex_1 = self.vertices[vertex_index]
            vertex_2 = self.vertices[(vertex_index + 1) % len(self.vertices)]

            edge_vector = [vertex_2[0] - vertex_1[0], vertex_2[1] - vertex_1[1]]
            normal_vector = [
                -edge_vector[1] / sqrt(edge_vector[0]**2 + edge_vector[1]**2),
                edge_vector[0] / sqrt(edge_vector[0]**2 + edge_vector[1]**2)
            ]

            axis = normal_vector
            self.axes.append(axis)

    
    def project_onto_axis(self, axis, vector_or_point):
        projection = axis[0]*vector_or_point[0] + axis[1]*vector_or_point[1]
        return projection


    def check_collision(self, object):
        other_hitbox = object.hitbox

        self.get_axes()
        other_hitbox.get_axes()

        all_axes = self.axes + other_hitbox.axes

        min_overlap = float('inf')
        mtv_axis = None

        for axis in all_axes:

            # GETTING PROJECTIONS OF OWN HITBOX VERTICES ONTO ALL AXES
            self_projections = []
            for vertex in self.vertices:
                projection = self.project_onto_axis(axis, vertex)
                self_projections.append(projection)

            # GETTING PROJECTIONS OF OTHER HITBOX VERTICES ONTO ALL AXES
            other_projections = []
            for vertex in other_hitbox.vertices:
                projection = self.project_onto_axis(axis, vertex)
                other_projections.append(projection)

            self_min = min(self_projections)
            self_max = max(self_projections)
            other_min = min(other_projections)
            other_max = max(other_projections)

            if self_max < other_min or other_max < self_min:
                return
            
            overlap = min(self_max - other_min, other_max - self_min)
            if overlap < min_overlap:
                min_overlap = overlap
                mtv_axis = axis

        self.resolve_collision(object, mtv_axis, min_overlap)


    def calculate_contact_point(self, other_object):
        self_center_x = self.object.position[0] #sum(vertex[0] for vertex in self.vertices) / len(self.vertices)
        self_center_y = self.object.position[1] #sum(vertex[1] for vertex in self.vertices) / len(self.vertices)

        other_center_x = other_object.position[0] #sum(vertex[0] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)
        other_center_y = other_object.position[1] #sum(vertex[1] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)

        object_connecting_line = [other_center_x - self_center_x, other_center_y - self_center_y]

        object_connecting_line_angle = atan2(object_connecting_line[1], object_connecting_line[0])

        min_angle_diff_between_connecting_line_and_vertex_ray = float('inf')

        for vertex_index in range(len(self.vertices)):
            vertex = self.vertices[vertex_index]

            vertex_ray_angle = atan2(vertex[1] - self_center_y, vertex[0] - self_center_x)
            angle_diff = object_connecting_line_angle - vertex_ray_angle

            if abs(angle_diff) < abs(min_angle_diff_between_connecting_line_and_vertex_ray):
                
                nearest_vertex_index = vertex_index
                min_angle_diff_between_connecting_line_and_vertex_ray = angle_diff

        vertex_1 = self.vertices[nearest_vertex_index]

        if min_angle_diff_between_connecting_line_and_vertex_ray < 0:
            vertex_2_index = (nearest_vertex_index - 1) % len(self.vertices)
        elif min_angle_diff_between_connecting_line_and_vertex_ray > 0:
            vertex_2_index = (nearest_vertex_index + 1) % len(self.vertices)
        else:
            return vertex_1
        
        vertex_2 = self.vertices[vertex_2_index]

        # SOLVING FOR THE INTERSECTION POINT BETWEEN EDGE AND CONNECTING LINE
        x1, y1 = vertex_1
        x2, y2 = vertex_2

        magnitude = sqrt(object_connecting_line[0]**2 + object_connecting_line[1]**2)
        connecting_dx = object_connecting_line[0] / magnitude
        connecting_dy = object_connecting_line[1] / magnitude

        edge_dx = x2 - x1
        edge_dy = y2 - y1

        # LINEAR EQUATION
        t_contact = ((x1 - self_center_x) * edge_dy - (y1 - self_center_y) * edge_dx) / (connecting_dx * edge_dy - connecting_dy * edge_dx)

        contact_x = self_center_x + t_contact * connecting_dx
        contact_y = self_center_y + t_contact * connecting_dy

        return contact_x, contact_y


    def calculate_impulse_change(self, other_object):
        self_center_x = self.object.position[0] #sum(vertex[0] for vertex in self.vertices) / len(self.vertices)
        self_center_y = self.object.position[1] #sum(vertex[1] for vertex in self.vertices) / len(self.vertices)

        other_center_x = other_object.position[0] #sum(vertex[0] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)
        other_center_y = other_object.position[1] #sum(vertex[1] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)

        distance = sqrt((other_center_x - self_center_x)**2 + (other_center_y - self_center_y)**2)
        direction_norm = [(other_center_x - self_center_x) / distance, (other_center_y - self_center_y) / distance] 

        self_speed = [self.object.vx, self.object.vy]
        other_speed = [other_object.vx, other_object.vy]

        self_speed_projection = self.project_onto_axis(direction_norm, self_speed)
        other_speed_projection = self.project_onto_axis(direction_norm, other_speed)
        relative_velocity = other_speed_projection - self_speed_projection

        impulse_magnitude = relative_velocity / (1/self.object.mass + 1/other_object.mass)
        impulse = [impulse_magnitude * direction_norm[0], impulse_magnitude * direction_norm[1]]

        self.object.vx += impulse[0] / self.object.mass
        self.object.vy += impulse[1] / self.object.mass

        if not other_object.movelocked:
            other_object.vx -= impulse[0] / other_object.mass
            other_object.vy -= impulse[1] / other_object.mass

        """ ANGULAR MOMENTUM CALCULATIONS GO HERE """


    def resolve_collision(self, other_object, mtv_axis, overlap):
        tolerance = 5 # tolerance for object minimum obejct collision distance

        self_center_x = self.object.position[0] #sum(vertex[0] for vertex in self.vertices) / len(self.vertices)
        self_center_y = self.object.position[1] #sum(vertex[1] for vertex in self.vertices) / len(self.vertices)

        other_center_x = other_object.position[0] #sum(vertex[0] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)
        other_center_y = other_object.position[1] #sum(vertex[1] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)

        if abs(self_center_x - other_center_x) < tolerance and abs(self_center_y - other_center_y) < tolerance:
                return

        self.collided = True
        other_object.hitbox.collided = True

        direction_x = other_center_x - self_center_x
        direction_y = other_center_y - self_center_y

        dot = direction_x * mtv_axis[0] + direction_y * mtv_axis[1]
        if dot < 0:
            mtv_axis = [-mtv_axis[0], -mtv_axis[1]]
        mtv_magnitude = sqrt(mtv_axis[0]**2 + mtv_axis[1]**2)

        mtv_axis_normalized = [mtv_axis[0]/mtv_magnitude, mtv_axis[1]/mtv_magnitude]

        self.mtv_axis_normalized = mtv_axis_normalized

        mtv = [mtv_axis_normalized[0] * overlap, mtv_axis_normalized[1] * overlap]

        # SEPARATING OBJECTS
        if self.object.movelocked and not other_object.movelocked:
            other_object.position[0] += mtv[0]
            other_object.position[1] += mtv[1]
        elif other_object.movelocked and not self.object.movelocked:
            self.object.position[0] -= mtv[0]
            self.object.position[1] -= mtv[1]
        else:
            self.object.position[0] -= mtv[0]/2
            self.object.position[1] -= mtv[1]/2
            other_object.position[0] += mtv[0]/2
            other_object.position[1] += mtv[1]/2

        # CALCULATING COLLISION POINT
        self.contact_point = self.calculate_contact_point(other_object)

        # CONSERVATION OF MOMENTUM
        self.calculate_impulse_change(other_object)


    def render(self, screen, camera, offset=[0, 0]):
        # DRAWING HIBOX VERTICES
        camera_rotation = radians(camera.rotation)
        self.get_axes()
        for vertex in self.vertices:
            vertex_offset_x = camera.position[0] - vertex[0] + (vertex[0] - camera.position[0])*cos(camera_rotation) - (vertex[1] - camera.position[1])*sin(camera_rotation)
            vertex_offset_y = camera.position[1] - vertex[1] + (vertex[0] - camera.position[0])*sin(camera_rotation) + (vertex[1] - camera.position[1])*cos(camera_rotation)
            vertex_offset = [vertex_offset_x - camera.position[0] + camera.width/2, vertex_offset_y - camera.position[1] + camera.height/2]
            pygame.draw.circle(
                screen,
                self.colour,
                (
                    vertex[0] + vertex_offset[0],
                    vertex[1] + vertex_offset[1]
                ),
                2,
            )

        # DRAWING HITBOX EDGES
        for vertex_index in range(len(self.vertices)):

            vertex_1 = self.vertices[vertex_index]
            vertex_1_offset_x = camera.position[0] - vertex_1[0] + (vertex_1[0] - camera.position[0])*cos(camera_rotation) - (vertex_1[1] - camera.position[1])*sin(camera_rotation)
            vertex_1_offset_y = camera.position[1] - vertex_1[1] + (vertex_1[0] - camera.position[0])*sin(camera_rotation) + (vertex_1[1] - camera.position[1])*cos(camera_rotation)
            vertex_1_offset = [vertex_1_offset_x - camera.position[0] + camera.width/2, vertex_1_offset_y - camera.position[1] + camera.height/2]

            vertex_2 = self.vertices[(vertex_index + 1) % len(self.vertices)]
            vertex_2_offset_x = camera.position[0] - vertex_2[0] + (vertex_2[0] - camera.position[0])*cos(camera_rotation) - (vertex_2[1] - camera.position[1])*sin(camera_rotation)
            vertex_2_offset_y = camera.position[1] - vertex_2[1] + (vertex_2[0] - camera.position[0])*sin(camera_rotation) + (vertex_2[1] - camera.position[1])*cos(camera_rotation)
            vertex_2_offset = [vertex_2_offset_x - camera.position[0] + camera.width/2, vertex_2_offset_y - camera.position[1] + camera.height/2]

            pygame.draw.line(
                screen,
                self.colour,
                (vertex_1[0] + vertex_1_offset[0], vertex_1[1] + vertex_1_offset[1]),
                (vertex_2[0] + vertex_2_offset[0], vertex_2[1] + vertex_2_offset[1]),
                1
            )

        # DRAWING COLLISION POINT
        if self.collided:
            collision_point_offset_x = camera.position[0] - self.contact_point[0] + (self.contact_point[0] - camera.position[0])*cos(camera_rotation) - (self.contact_point[1] - camera.position[1])*sin(camera_rotation)
            collision_point_offset_y = camera.position[1] - self.contact_point[1] + (self.contact_point[0] - camera.position[0])*sin(camera_rotation) + (self.contact_point[1] - camera.position[1])*cos(camera_rotation)
            collision_point_offset = [collision_point_offset_x - camera.position[0] + camera.width/2, collision_point_offset_y - camera.position[1] + camera.height/2]
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    self.contact_point[0] + collision_point_offset[0],
                    self.contact_point[1] + collision_point_offset[1]
                ),
                2,
            )
