import pygame
from math import sin, cos, pi, radians, atan2, sqrt
from numpy import sign


class Hitbox:
    def __init__(self, object, size, type, colour=(255, 0, 0)):
        self.object = object
        self.size = size
        self.type = type

        self.colour = colour

        self.collision_position = [0, 0]

        self.collided = False

        # Defining edges and axes for SAT algorithm
        self.vertices = []
        self.axes = []


    def get_vertices(self):
        self.vertices = []

        if self.type == 'rectangle':

            # VERTEX COORDINATES IN OBJECT REFERENCE FRAME
            upper_left_0 = [-self.size[0]/2, -self.size[1]/2]
            upper_right_0 = [self.size[0]/2, -self.size[1]/2]
            lower_left_0 = [-self.size[0]/2, self.size[1]/2]
            lower_right_0 = [self.size[0]/2, self.size[1]/2]
            vertices_0 = [upper_left_0, upper_right_0, lower_right_0, lower_left_0]

        # GETTING VERTEX COORDINATES FOR ROTATED HITBOX
        object_rotation = -radians(self.object.rotation)
        for vertex in vertices_0:
            rotated_vertex_x = vertex[0] * cos(object_rotation) - vertex[1] * sin(object_rotation)
            rotated_vertex_y = vertex[1] * cos(object_rotation) + vertex[0] * sin(object_rotation)
            rotated_point = [self.object.position[0] + rotated_vertex_x, self.object.position[1] + rotated_vertex_y]
            self.vertices.append(rotated_point)


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

    
    def project_point_onto_axis(self, axis, point):
        projection = axis[0]*point[0] + axis[1]*point[1]
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
                projection = self.project_point_onto_axis(axis, vertex)
                self_projections.append(projection)

            # GETTING PROJECTIONS OF OTHER HITBOX VERTICES ONTO ALL AXES
            other_projections = []
            for vertex in other_hitbox.vertices:
                projection = self.project_point_onto_axis(axis, vertex)
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








    def calculate_contact_point(self, other_object, mtv_axis_normal):
        dist = sqrt(self.size[0]**2 + self.size[1]**2)
        contact_point = [
            self.object.position[0] + dist * mtv_axis_normal[0] / 2,
            self.object.position[1] + dist * mtv_axis_normal[1] / 2,
        ]

        return contact_point






    def resolve_collision(self, other_object, mtv_axis, overlap):
        self.collided = True
        other_object.hitbox.collided = True
        self_center_x = sum(vertex[0] for vertex in self.vertices) / len(self.vertices)
        self_center_y = sum(vertex[1] for vertex in self.vertices) / len(self.vertices)
        other_center_x = sum(vertex[0] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)
        other_center_y = sum(vertex[1] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)

        direction_x = other_center_x - self_center_x
        direction_y = other_center_y - self_center_y

        dot = direction_x * mtv_axis[0] + direction_y * mtv_axis[1]
        if dot < 0:
            mtv_axis = [-mtv_axis[0], -mtv_axis[1]]
        mtv_magnitude = sqrt(mtv_axis[0]**2 + mtv_axis[1]**2)

        mtv_axis_normal = [mtv_axis[0]/mtv_magnitude, mtv_axis[1]/mtv_magnitude]
        mtv = [mtv_axis_normal[0] * overlap, mtv_axis_normal[1] * overlap]


        self.collision_position = self.calculate_contact_point(other_object, mtv_axis_normal)
        
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


    def render(self, screen, camera, offset=[0, 0]):
        if self.type == 'rectangle':
            rect_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, self.colour, rect_surface.get_rect(), 1)
            rotated_surface = pygame.transform.rotate(rect_surface, self.object.rotation - camera.rotation)
            rotated_rect = rotated_surface.get_rect(center=(self.object.position[0] + offset[0], self.object.position[1] + offset[1]))
            screen.blit(rotated_surface, rotated_rect.topleft)

        # DRAWING HIBOX VERTICES
        camera_rotation = radians(camera.rotation)
        self.get_axes()
        for vertex in self.vertices:
            vertex_offset_x = camera.position[0] - vertex[0] + (vertex[0] - camera.position[0])*cos(camera_rotation) - (vertex[1] - camera.position[1])*sin(camera_rotation)
            vertex_offset_y = camera.position[1] - vertex[1] + (vertex[0] - camera.position[0])*sin(camera_rotation) + (vertex[1] - camera.position[1])*cos(camera_rotation)
            vertex_offset = [vertex_offset_x - camera.position[0] + camera.width/2, vertex_offset_y - camera.position[1] + camera.height/2]
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    vertex[0] + vertex_offset[0],
                    vertex[1] + vertex_offset[1]
                ),
                2,
                1
            )

        # DRAWING COLLISION POINT
        if self.collided:
            collision_point_offset_x = camera.position[0] - self.collision_position[0] + (self.collision_position[0] - camera.position[0])*cos(camera_rotation) - (self.collision_position[1] - camera.position[1])*sin(camera_rotation)
            collision_point_offset_y = camera.position[1] - self.collision_position[1] + (self.collision_position[0] - camera.position[0])*sin(camera_rotation) + (self.collision_position[1] - camera.position[1])*cos(camera_rotation)
            collision_point_offset = [collision_point_offset_x - camera.position[0] + camera.width/2, collision_point_offset_y - camera.position[1] + camera.height/2]
            pygame.draw.circle(
                screen,
                (0, 255, 255),
                (
                    self.collision_position[0] + collision_point_offset[0],
                    self.collision_position[1] + collision_point_offset[1]
                ),
                2,
                1
            )