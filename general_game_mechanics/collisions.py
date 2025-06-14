import pygame
from math import sin, cos, pi, radians, atan2, acos, sqrt
from numpy import sign, dot, cross

class Hitbox:
    def __init__(self, object, size, type, hitbox_offset=(0,0), colour=(255, 0, 0), ):
        self.show_hitbox = False

        self.object = object
        self.size = size
        self.hitbox_offset = hitbox_offset
        self.type = type

        self.colour = colour

        self.restitution = 0 # COLLISION RESTITUTION
        self.max_spin_amp = 10 # MAGIC NUMBER TO AMPLIFY ANGULAR MOMENTUM EXCHANGE
        
        self.moment_of_inertia = self.calculate_moment_of_inertia()

        self.contact_point = [0, 0]
        self.collision_normal = [0, 0]
        self.spin_vector = [0, 0]

        self.collided = False

        self.colliding_objects = {}

        # Vertices for SAT algorithm
        self.vertices = []

        # Calculating vertices, axes for SAT algorithm and topological depth sorting
        self.update() # Getting hitbox vertices
        self.axes = self.get_axes()
        
        self.mtv_axis = [0, 0]
        self.min_overlap = 0
        self.mtv_axis_normalized = [0, 0]


    def get_vertices(self, size, offset):
        vertices = []

        # VERTICES FOR RECTANGULAR HITBOX
        if self.type == 'rectangle':
            # VERTEX COORDINATES IN OBJECT REFERENCE FRAME
            upper_left_0 = [-size[0]/2 + offset[0], -size[1]/2 + offset[1]]
            upper_right_0 = [size[0]/2 + offset[0], -size[1]/2 + offset[1]]
            lower_left_0 = [-size[0]/2 + offset[0], size[1]/2 + offset[1]]
            lower_right_0 = [size[0]/2 + offset[0], size[1]/2 + offset[1]]
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
                vertex = [size[0]/2 * cos(phi) + offset[1], size[1]/2 * sin(phi) + offset[1]]
                vertices_0.append(vertex)

        # GETTING VERTEX COORDINATES FOR ROTATED HITBOX
        object_rotation = -radians(self.object.rotation)
        for vertex in vertices_0:
            rotated_vertex_x = vertex[0] * cos(object_rotation) - vertex[1] * sin(object_rotation)
            rotated_vertex_y = vertex[1] * cos(object_rotation) + vertex[0] * sin(object_rotation)
            rotated_vertex = [self.object.position[0] + rotated_vertex_x, self.object.position[1] + rotated_vertex_y]
            vertices.append(rotated_vertex)

        return vertices


    def update(self):
        self.vertices = self.get_vertices(self.size, self.hitbox_offset)


    def get_axes(self):
        self.update()
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


    def get_center_of_mass(self):
        return self.object.position


    def check_collision(self, object):
        other_hitbox = object.hitbox

        self.get_axes()
        other_hitbox.get_axes()

        all_axes = self.axes + other_hitbox.axes

        min_overlap = float('inf')
        mtv_axis = [0, 0]

        for axis in all_axes:

            # GETTING PROJECTIONS OF OWN HITBOX VERTICES ONTO ALL AXES
            self_projections = []
            for vertex in self.vertices:
                projection = dot(axis, vertex)
                self_projections.append(projection)

            # GETTING PROJECTIONS OF OTHER HITBOX VERTICES ONTO ALL AXES
            other_projections = []
            for vertex in other_hitbox.vertices:
                projection = dot(axis, vertex)
                other_projections.append(projection)

            self_min = min(self_projections)
            self_max = max(self_projections)
            other_min = min(other_projections)
            other_max = max(other_projections)

            if self_max < other_min or other_max < self_min:
                # REMOVING OBJECT AND COLLISION DATA FROM COLLIDING_OBJECTS DICT
                if object in self.colliding_objects.keys():
                    del self.colliding_objects[object]
                return

            overlap = min(self_max - other_min, other_max - self_min)
            if overlap < min_overlap:
                min_overlap = overlap
                mtv_axis = axis

        # ADDING OBJECT AND COLLISION DATA TO COLLIDING_OBJECTS DICT
        self.colliding_objects[object] = {
            'mtv_axis': mtv_axis,
            'overlap': min_overlap
        }


    def calculate_moment_of_inertia(self):
        return 1


    def vectors_angle(self, v1, v2):
        angle_v1 = atan2(v1[1], v1[0])
        angle_v2 = atan2(v2[1], v2[0])
        angle = angle_v1 - angle_v2
        return angle


    def calculate_contact_point_and_collision_normal(self, other_object): 

        def find_collision_point_and_normal(vertices_1, center_1, vertices_2, center_2):
            eps = 0.1
            for vertex_index in range(len(vertices_1)):
                vertex = vertices_1[vertex_index]
                for edge_index in range(len(vertices_2)):
                    edge_vertex_1 = vertices_2[edge_index]
                    edge_vertex_2 = vertices_2[(edge_index + 1) % len(vertices_2)]
    
                    vector_1 = [
                        edge_vertex_1[0] - vertex[0],
                        edge_vertex_1[1] - vertex[1]
                    ]
                    vector_2 = [
                        edge_vertex_2[0] - vertex[0],
                        edge_vertex_2[1] - vertex[1]
                    ]
    
                    angle = abs(self.vectors_angle(vector_1, vector_2))
    
                    if abs(angle - pi) < eps:
                        collision_point = vertex
    
                        collision_edge_axis = [
                            edge_vertex_1[0] - edge_vertex_2[0],
                            edge_vertex_1[1] - edge_vertex_2[1],
                        ]
    
                        collision_normal = [
                            -collision_edge_axis[1],
                            collision_edge_axis[0]
                        ]
                        center_to_collision = [
                            collision_point[0] - center_2[0],
                            collision_point[1] - center_2[1]
                        ]
                        if dot(collision_normal, center_to_collision) < 0:
                            collision_normal = [
                                -collision_normal[0],
                                -collision_normal[1]
                            ]
                        magnitude = sqrt(collision_normal[0]**2 + collision_normal[1]**2)
                        collision_normal = [
                            collision_normal[0] / magnitude,
                            collision_normal[1] / magnitude
                        ]
                        return collision_point, collision_normal
            return None, None
    
        # Get vertices and centers for both objects
        self_center = self.get_center_of_mass()
        other_center = other_object.hitbox.get_center_of_mass()
    
        self_vertices = self.vertices
        other_vertices = other_object.hitbox.vertices
    
        # SELF VERTEX / OTHER EDGE COLLISION
        collision_point, collision_normal = find_collision_point_and_normal(
            self_vertices, self_center, other_vertices, other_center
        )
        if collision_point and collision_normal:
            self.contact_point = collision_point
            other_object.hitbox.contact_point = collision_point
            self.collision_normal = collision_normal
            other_object.hitbox.collision_normal = [-collision_normal[0], -collision_normal[1]]
            return
    
        # SELF EDGE / OTHER VERTEX COLLISION
        collision_point, collision_normal = find_collision_point_and_normal(
            other_vertices, other_center, self_vertices, self_center
        )
        if collision_point and collision_normal:
            self.contact_point = collision_point
            other_object.hitbox.contact_point = collision_point
            self.collision_normal = collision_normal
            other_object.hitbox.collision_normal = [-collision_normal[0], -collision_normal[1]]
            return
        else:
            pass


    def calculate_impulse_change(self, other_object):
        deg_to_rad_conversion_constant = pi / 180 # the rotation of each object is in degrees, so we introduce a conversion constant

        self_center = self.get_center_of_mass()
        other_center = other_object.hitbox.get_center_of_mass()

        # OBJECT MASSES
        m_A = self.object.mass
        m_B = other_object.mass

        # COLLISION RESTITUTION
        e = self.restitution

        # SELF COLLISION NORMALS
        n_A = [
            self.collision_normal[0],
            self.collision_normal[1]
        ]
        n_B = [
            other_object.hitbox.collision_normal[0],
            other_object.hitbox.collision_normal[1]
        ]

        # RADIUS VECTORS FROM CENTER TO THE POINT OF COLLISION
        r_AP = [
            self.contact_point[0] - self_center[0],
            self.contact_point[1] - self_center[1]
        ]
        r_BP = [
            self.contact_point[0] - other_center[0],
            self.contact_point[1] - other_center[1]
        ]

        # NORMALIZED RADIUS VECTORS
        self_distance = sqrt(r_AP[0]**2 + r_AP[1]**2)
        r_AP_norm = [
            r_AP[0] / self_distance,
            r_AP[1] / self_distance
        ]
        other_distance = sqrt(r_BP[0]**2 + r_BP[1]**2)
        r_BP_norm = [
            r_BP[0] / other_distance,
            r_BP[1] / other_distance
        ]

        # APPROXIMATING TRANSVERSE RADIUS AXES (WE DO NOT YET KNOW THE CORRECT DIRECTION)
        r_t_AP_norm_approx = [
            -r_AP_norm[1],
            r_AP_norm[0]
        ]
        r_t_BP_norm_approx = [
            -r_BP_norm[1],
            r_BP_norm[0]
        ]

        # CORRECTING TRANSVERSE RADIUS AXES
        spin_direction_A = sign(r_AP_norm[0]*n_A[1] - r_AP_norm[1]*n_A[0])
        if spin_direction_A < 0:
            r_t_AP_norm = [
                r_t_AP_norm_approx[0],
                r_t_AP_norm_approx[1]
            ]
        elif spin_direction_A >= 0:
            r_t_AP_norm = [
                -r_t_AP_norm_approx[0],
                -r_t_AP_norm_approx[1]
            ]
        self.spin_vector = r_t_AP_norm
        r_t_AP = [
            r_t_AP_norm[0] * self_distance,
            r_t_AP_norm[1] * self_distance
        ]

        spin_direction_B = sign(r_BP_norm[0]*n_B[1] - r_BP_norm[1]*n_B[0])
        if spin_direction_B > 0:
            r_t_BP_norm = [
                r_t_BP_norm_approx[0],
                r_t_BP_norm_approx[1]
            ]
        elif spin_direction_B <= 0:
            r_t_BP_norm = [
                -r_t_BP_norm_approx[0],
                -r_t_BP_norm_approx[1]
            ]
        other_object.hitbox.spin_vector = r_t_BP_norm
        r_t_BP = [
            r_t_BP_norm[0] * other_distance,
            r_t_BP_norm[1] * other_distance
        ]

        # RELATIVE SPEED (TRANSLATIONAL ONLY, NOT ACCOUNTING FOR ROTATIONAL MOVEMENT)
        v_AP = [
            self.object.vx,
            self.object.vy
        ]
        v_BP = [
            other_object.vx,
            other_object.vy
        ]
        v_AB = [
            v_AP[0] - v_BP[0],
            v_AP[1] - v_BP[1]
        ]

        # HANDLING DEGENERATE COLLISION CASES
        if abs(dot(v_AB, n_A)) < 1e-8 or abs(dot(n_A, n_A)) < 1e-8:
            return

        # IMPULSE
        dot_product = dot(v_AB, n_A)
        relative_incoming_speed = abs(dot_product)
        j = -(1 + self.restitution) * relative_incoming_speed * sign(dot_product) / (1/m_A + 1/m_B)

        # CHANGE IN LINEAR MOMENTUM
        self.object.vx +=  (j / m_A) * n_A[0]
        self.object.vy +=  (j / m_A) * n_A[1]

        # CHANGE IN ANGULAR MOMENTUM
        self.object.omega += -spin_direction_A * j * self_distance / m_A * abs(dot(r_AP_norm, n_A)) * deg_to_rad_conversion_constant * min(m_B / m_A, self.max_spin_amp)


    def resolve_collision(self, other_object, mtv_axis, overlap):

        tolerance = 5 # tolerance for object minimum obejct collision distance
        self_center = self.get_center_of_mass()
        other_center = other_object.hitbox.get_center_of_mass()

        self_center[0] = self.object.position[0] #sum(vertex[0] for vertex in self.vertices) / len(self.vertices)
        self_center[1] = self.object.position[1] #sum(vertex[1] for vertex in self.vertices) / len(self.vertices)

        other_center[0] = other_object.position[0] #sum(vertex[0] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)
        other_center[1] = other_object.position[1] #sum(vertex[1] for vertex in other_object.hitbox.vertices) / len(other_object.hitbox.vertices)

        if abs(self_center[0] - other_center[0]) < tolerance and abs(self_center[1] - other_center[1]) < tolerance:
                return

        self.collided = True
        other_object.hitbox.collided = True

        direction_x = other_center[0] - self_center[0]
        direction_y = other_center[1] - self_center[1]

        dot = direction_x * mtv_axis[0] + direction_y * mtv_axis[1]
        if dot < 0:
            mtv_axis = [-mtv_axis[0], -mtv_axis[1]]
        mtv_magnitude = sqrt(mtv_axis[0]**2 + mtv_axis[1]**2)
        if abs(mtv_magnitude) > 0.0001:
            mtv_axis_normalized = [mtv_axis[0]/mtv_magnitude, mtv_axis[1]/mtv_magnitude]
        else:
            mtv_axis_normalized = mtv_axis
        

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

        # CALCULATING COLLISION POINT AND NORMAL FOR EACH OBJECT
        self.calculate_contact_point_and_collision_normal(other_object)

        # CONSERVATION OF MOMENTUM
        self.calculate_impulse_change(other_object)


    def render(self, screen, camera, offset=[0, 0]):

        if self.show_hitbox:
            # DRAWING HIBOX VERTICES

            camera_rotation = radians(camera.rotation)
            zoom = camera.zoom
            cam_x, cam_y = camera.position
            cam_w, cam_h = camera.width, camera.height

            self.get_axes()
            for vertex in self.vertices:
                dx = vertex[0] - cam_x
                dy = vertex[1] - cam_y
                rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
                rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
                screen_x =  cam_w // 2 + rot_dx * zoom - vertex[0]
                screen_y =  cam_h // 2 + rot_dy * zoom - vertex[1]
                vertex_offset = [screen_x, screen_y]
                pygame.draw.circle(
                    screen,
                    self.colour,
                    (
                        vertex[0] + vertex_offset[0],
                        vertex[1] + vertex_offset[1] - self.object.position[2]
                    ),
                    2,
                )

            # DRAWING HITBOX EDGES
            for vertex_index in range(len(self.vertices)):
                vertex_1 = self.vertices[vertex_index]
                dx = vertex_1[0] - cam_x
                dy = vertex_1[1] - cam_y
                rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
                rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
                screen_x =  cam_w // 2 + rot_dx * zoom - vertex_1[0]
                screen_y =  cam_h // 2 + rot_dy * zoom - vertex_1[1]
                vertex_1_offset = [screen_x, screen_y]
                vertex_2 = self.vertices[(vertex_index + 1) % len(self.vertices)]
                dx = vertex_2[0] - cam_x
                dy = vertex_2[1] - cam_y
                rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
                rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
                screen_x =  cam_w // 2 + rot_dx * zoom - vertex_2[0]
                screen_y =  cam_h // 2 + rot_dy * zoom - vertex_2[1]
                vertex_2_offset = [screen_x, screen_y]
                pygame.draw.line(
                    screen,
                    self.colour,
                    (vertex_1[0] + vertex_1_offset[0], vertex_1[1] + vertex_1_offset[1] - self.object.position[2]),
                    (vertex_2[0] + vertex_2_offset[0], vertex_2[1] + vertex_2_offset[1] - self.object.position[2]),
                    1
                )
            # DRAWING COLLISION POINT
            if self.collided:
                dx = self.contact_point[0] - cam_x
                dy = self.contact_point[1] - cam_y
                rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
                rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
                screen_x =  cam_w // 2 + rot_dx * zoom - self.contact_point[0]
                screen_y =  cam_h // 2 + rot_dy * zoom - self.contact_point[1]
                collision_point_offset = [screen_x, screen_y]
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        self.contact_point[0] + collision_point_offset[0],
                        self.contact_point[1] + collision_point_offset[1] - self.object.position[2]
                    ),
                    2,
                )

            # DRAWING NORMAL
            if self.collided:
                collision_endpoint = [
                    self.contact_point[0] + self.collision_normal[0]*10,
                    self.contact_point[1] + self.collision_normal[1]*10
                ]
                dx = collision_endpoint[0] - cam_x
                dy = collision_endpoint[1] - cam_y
                rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
                rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
                screen_x =  cam_w // 2 + rot_dx * zoom - collision_endpoint[0]
                screen_y =  cam_h // 2 + rot_dy * zoom - collision_endpoint[1]
                collision_normal_endpoint_offset = [screen_x, screen_y]
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    (self.contact_point[0] + collision_point_offset[0], self.contact_point[1] + collision_point_offset[1] - self.object.position[2]),
                    (collision_endpoint[0] + collision_normal_endpoint_offset[0], collision_endpoint[1] + collision_normal_endpoint_offset[1] - self.object.position[2]),
                    1
                )

            # DRAWING DIRECTION OF APPLIED SPIN
            if self.collided:
                spin_vector_magnitude = sqrt(self.size[0]**2 + self.size[1]**2)
                spin_endpoint = [
                    self.contact_point[0] + self.spin_vector[0]*spin_vector_magnitude,
                    self.contact_point[1] + self.spin_vector[1]*spin_vector_magnitude
                ]
                dx = spin_endpoint[0] - cam_x
                dy = spin_endpoint[1] - cam_y
                rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
                rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
                screen_x =  cam_w // 2 + rot_dx * zoom - spin_endpoint[0]
                screen_y =  cam_h // 2 + rot_dy * zoom - spin_endpoint[1]
                spin_endpoint_offset = [screen_x, screen_y]

                pygame.draw.line(
                    screen,
                    (0, 255, 0),
                    (self.contact_point[0] + collision_point_offset[0], self.contact_point[1] + collision_point_offset[1] - self.object.position[2]),
                    (spin_endpoint[0] + spin_endpoint_offset[0], spin_endpoint[1] + spin_endpoint_offset[1] - self.object.position[2]),
                    1
                )

