import pygame

from math import sin, cos, radians, atan2
from numpy import dot
from itertools import combinations

from graphics import grass, plants
from graphics.particles import ParticleSystem
from graphics.sprite_stacks import SpritestackModel
from world_builder.loadpoints import LoadPoint




""" CALCULATE MIN AND MAX PROJECTIONS AND CORRESPONDING VERTICES AMONG AN OBJECT'S VERTICES """
def project_object(obj, axis):
    min_projection = float('inf')
    max_projection = -float('inf')
    min_vertex = None
    max_vertex = None
    for vertex in obj.hitbox.vertices:
        vertex_projection = dot(vertex, axis)
        if vertex_projection < min_projection:
            min_projection = vertex_projection
            min_vertex = vertex
        if vertex_projection > max_projection:
            max_projection = vertex_projection
            max_vertex = vertex
    return min_projection, max_projection, min_vertex, max_vertex

""" CALCULATE COORDINATES OF A VERTEX IN CAMERA COORDINATES """
def transform_to_camera_space(vertex, camera_x_axis, camera_y_axis):
    x_camera = dot(vertex, camera_x_axis)
    y_camera = dot(vertex, camera_y_axis)
    return x_camera, y_camera

""" CALCULATE EQUATION FOR A LINE FORMED BY TWO VERTICES """
def compute_line_equation(vertex1, vertex2):
    x1, y1 = vertex1
    x2, y2 = vertex2
    if x1 == x2:
        return None # VERTICAL LINE CASE
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1 
    return lambda x: slope * x + intercept

""" FINDING THE OVERLAP OF TWO RANGES (IN OUR CASE - PROJECTIONS) """
def find_ranges_overlap(range_1_min, range_1_max, range_2_min, range_2_max):
    start = max(range_1_min, range_2_min)
    end = min(range_1_max, range_2_max)
    return [start, end]





def depth_sort(objects, camera):

    # CALCULATING CAMERA AXES
    camera_rotation = radians(camera.rotation)
    camera_x_axis = [-cos(camera_rotation), sin(camera_rotation)]
    camera_y_axis = [sin(camera_rotation), cos(camera_rotation)]
    
    # LOOPING THROUGH ALL OBJECTS AND CALCULATING MIN/MAX PROJECTIONS AND CORRESPONDING VERTICES
    projections = []
    vertices = []
    for obj in objects:
        min_x, max_x, min_vertex, max_vertex = project_object(obj, camera_x_axis)
        projections.append((min_x, max_x))
        vertices.append((min_vertex, max_vertex))
    
    # BUILDING A GRAPH FOR ALL OBJECTS
    adjacency_graph = {obj: set() for obj in objects}
    
    # LOOPING THROUGH ALL OBJECT PAIRS
    for obj_1_index, obj_2_index in combinations(range(len(objects)), 2):

        obj_1_min_x, obj_1_max_x = projections[obj_1_index]
        obj_2_min_x, obj_2_max_x = projections[obj_2_index]

        object_1 = objects[obj_1_index]
        object_2 = objects[obj_2_index]

        # IF THE PROJECTIONS OF TWO OBJECTS ONTO THE CAMERA_X AXIS INTERSECT:
        if obj_1_max_x >= obj_2_min_x and obj_2_max_x >= obj_1_min_x:
            v1_min, v1_max = vertices[obj_1_index]
            v2_min, v2_max = vertices[obj_2_index]
            # GETTING CAMERA COODRINATES OF THE VERTICES WITH MIN AND MAX PROJECTIONS FOR OBJECT 1 AND OBJECT 2
            v1_min_cam = transform_to_camera_space(v1_min, camera_x_axis, camera_y_axis)
            v1_max_cam = transform_to_camera_space(v1_max, camera_x_axis, camera_y_axis)
            v2_min_cam = transform_to_camera_space(v2_min, camera_x_axis, camera_y_axis)
            v2_max_cam = transform_to_camera_space(v2_max, camera_x_axis, camera_y_axis)
            # FINDING THE OVERLAP OF OBJECT PROJECTIONS ONTO THE CAMERA X AXIS
            x_camera_projections_overlap = find_ranges_overlap(v1_min_cam[0], v1_max_cam[0], v2_min_cam[0], v2_max_cam[0])
            # GETTING THE EQUATION FOR OBJECT 2 LINE IN CAMERA COORDINATES
            line_eq_object_1 = compute_line_equation(v1_min_cam, v1_max_cam)
            line_eq_object_2 = compute_line_equation(v2_min_cam, v2_max_cam)
            # GETTING THE VALUE OF EACH EQUATION AT THE START AND END OF THE OVERLAP
            y_object_1_line_at_overlap_start = line_eq_object_1(x_camera_projections_overlap[0])
            y_object_2_line_at_overlap_start = line_eq_object_2(x_camera_projections_overlap[0])
            y_object_1_line_at_overlap_end = line_eq_object_1(x_camera_projections_overlap[1])
            y_object_2_line_at_overlap_end = line_eq_object_2(x_camera_projections_overlap[1])
            # DETERMINE WHICH LINE COMES FIRST IF WE MOVE ALONG THE CAMERA Y AXIS
            dz = object_1.position[2] - object_2.position[2] # ACCOUNTING FOR Z COORDINATE (this kind of works for most cases, if dz is not too large)
            if (y_object_1_line_at_overlap_start + dz > y_object_2_line_at_overlap_start) or \
            (y_object_1_line_at_overlap_end + dz > y_object_2_line_at_overlap_end):
                adjacency_graph[object_2].add(object_1)
            else:
                adjacency_graph[object_1].add(object_2)

                
    # RUNNING THROUGH CONSTRUCTED GRAPH
    sorted_objects = []
    while adjacency_graph:
        no_dependency = [obj for obj in adjacency_graph if not adjacency_graph[obj]]
        if not no_dependency:
            # RESOLVING CYCLES BY CHOOSING AN ARBITRATY OBJECT AND REMOVING ITS DEPENDENCIES
            obj_to_remove = next(iter(adjacency_graph))
            sorted_objects.append(obj_to_remove)
            del adjacency_graph[obj_to_remove]
            for remaining in adjacency_graph:
                adjacency_graph[remaining].discard(obj_to_remove)
        else:
            for obj in no_dependency:
                sorted_objects.insert(0, obj)
                del adjacency_graph[obj]
            for remaining in adjacency_graph:
                adjacency_graph[remaining] -= set(no_dependency)
    
    return sorted_objects



def global_render(screen, camera, objects, bend_objects=[]):
    extra_padding = 100
    render_padding_x = screen.get_width() / 2 + extra_padding
    render_padding_y = screen.get_height() / 2 + extra_padding

    # CALCULATING ROTATED CAMERA X AND Y AXES
    camera_rotation = radians(camera.rotation)
    camera_x_axis = [-cos(camera_rotation), sin(camera_rotation)]
    camera_y_axis = [sin(camera_rotation), cos(camera_rotation)]

    if len(objects) > 0:
        sorted_objects = depth_sort(objects, camera)
        
        for game_object in sorted_objects:
            is_in_frame_x = (game_object.position[0] > camera.position[0] - render_padding_x) and \
                            (game_object.position[0] < camera.position[0] + render_padding_x)
    
            is_in_frame_y = (game_object.position[1] > camera.position[1] - render_padding_y) and \
                            (game_object.position[1] < camera.position[1] + render_padding_y)
            
            if is_in_frame_x and is_in_frame_y:
                offset_x = camera.position[0] - game_object.position[0] + (game_object.position[0] - camera.position[0])*cos(camera_rotation) - (game_object.position[1] - camera.position[1])*sin(camera_rotation)
                offset_y = camera.position[1] - game_object.position[1] + (game_object.position[0] - camera.position[0])*sin(camera_rotation) + (game_object.position[1] - camera.position[1])*cos(camera_rotation)
                offset = [offset_x - camera.position[0] + camera.width/2, offset_y - camera.position[1] + camera.height/2]
    
                if isinstance(game_object, plants.Plant):
                    game_object.render(screen, bend_objects, offset)
    
                elif isinstance(game_object, grass.GrassTile):
                    game_object.render(screen, bend_objects, offset)
    
                elif isinstance(game_object, SpritestackModel):
                    game_object.render(screen, camera, offset)
                
                elif isinstance(game_object, ParticleSystem):
                    game_object.render(screen, camera)

                elif isinstance(game_object, LoadPoint):
                    game_object.render(screen, offset)

            min_x, max_x, best_line_vertice_1, best_line_vertice_2 = project_object(game_object, camera_x_axis)
            best_line_vertices = [best_line_vertice_1, best_line_vertice_2]
            for vertex in best_line_vertices:
                vertex_offset_x = camera.position[0] - vertex[0] + (vertex[0] - camera.position[0])*cos(camera_rotation) - (vertex[1] - camera.position[1])*sin(camera_rotation)
                vertex_offset_y = camera.position[1] - vertex[1] + (vertex[0] - camera.position[0])*sin(camera_rotation) + (vertex[1] - camera.position[1])*cos(camera_rotation)
                vertex_offset = [vertex_offset_x - camera.position[0] + camera.width/2, vertex_offset_y - camera.position[1] + camera.height/2]
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        vertex[0] + vertex_offset[0],
                        vertex[1] + vertex_offset[1] - game_object.position[2]
                    ),
                    3,
                )
