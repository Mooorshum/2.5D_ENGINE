from math import sin, cos, radians
from numpy import dot, sign
from itertools import combinations

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
    if start < end:
        return [start, end]
    else:
        return False


""" PERFORMING TOPOLOGICAL DEPTH SORTNG OF OBJECTS """
def depth_sort(objects, camera):

    # CALCULATING CAMERA AXES
    camera_rotation = radians(camera.rotation)
    camera_x_axis = [-cos(camera_rotation), sin(camera_rotation)]
    camera_y_axis = [sin(camera_rotation), cos(camera_rotation)]
    
    # LOOPING THROUGH ALL OBJECTS AND CALCULATING MIN/MAX PROJECTIONS AND CORRESPONDING VERTICES
    projections_x = []
    projections_y = []
    vertices_x = []
    vertices_y = []

    for obj in objects:
        # PROJECTION ONTO CAMERA X AXIS
        min_x, max_x, min_vertex_x, max_vertex_x = project_object(obj, camera_x_axis)
        projections_x.append((min_x, max_x))
        vertices_x.append((min_vertex_x, max_vertex_x))

        # PROJECTION ONTO CAMERA Y AXIS
        min_y, max_y, min_vertex_y, max_vertex_y = project_object(obj, camera_y_axis)
        projections_y.append((min_y, max_y))
        vertices_y.append((min_vertex_y, max_vertex_y))

    # BUILDING A GRAPH FOR ALL OBJECTS
    adjacency_graph = {obj: set() for obj in objects}

    # LOOPING THROUGH ALL OBJECT PAIRS
    for obj_1_index, obj_2_index in combinations(range(len(objects)), 2):

        object_1 = objects[obj_1_index]
        object_2 = objects[obj_2_index]

        obj_1_min_x, obj_1_max_x = projections_x[obj_1_index]
        obj_2_min_x, obj_2_max_x = projections_x[obj_2_index]

        obj_1_min_y, obj_1_max_y = projections_y[obj_1_index]
        obj_2_min_y, obj_2_max_y = projections_y[obj_2_index]

        """ print(f'obj1 min y: {obj_1_min_y}')
        print(f'obj1 max y: {obj_1_max_y}')
        print(f'obj2 min y: {obj_2_min_y}')
        print(f'obj2 max y: {obj_2_max_y}')
        print('------------------') """

        # GETTING THE BOUNDING BOX PROJECTIONS ONTO THE X CAMERA AXIS FOR BOTH OBJECTS
        overlap_x_camera = find_ranges_overlap(obj_1_min_x, obj_1_max_x, obj_2_min_x, obj_2_max_x)

        # CONDITION FOR INTERSECTION OF BOUNDING BOXES ALONG Y AXIS:
        overlap_y_camera = find_ranges_overlap(
            obj_1_min_y - object_1.position[2] - object_1.height,
            obj_1_max_y - object_1.position[2],
            obj_2_min_y - object_2.position[2] - object_2.height,
            obj_2_max_y - object_2.position[2]
        )

        # IF THE PROJECTIONS OF TWO OBJECTS ONTO THE CAMERA X AXIS INTERSECT:
        if overlap_x_camera and overlap_y_camera:

            front_object = None
            back_object = None
    
            """ DETERMINE WHICH LINE COMES FIRST IF WE MOVE ALONG THE CAMERA Y AXIS FROM THE CENTER OF THE OVERLAP """
            # GETTING CAMERA COODRINATES OF THE VERTICES WITH MIN AND MAX X PROJECTIONS FOR OBJECT 1 AND OBJECT 2
            v1_min_x, v1_max_x = vertices_x[obj_1_index]
            v2_min_x, v2_max_x = vertices_x[obj_2_index]

            v1_min_cam_x = transform_to_camera_space(v1_min_x, camera_x_axis, camera_y_axis)
            v1_max_cam_x = transform_to_camera_space(v1_max_x, camera_x_axis, camera_y_axis)
            v2_min_cam_x = transform_to_camera_space(v2_min_x, camera_x_axis, camera_y_axis)
            v2_max_cam_x = transform_to_camera_space(v2_max_x, camera_x_axis, camera_y_axis)

            # FINDING THE OVERLAP OF OBJECT PROJECTIONS ONTO THE CAMERA X AXIS
            x_camera_projections_overlap = find_ranges_overlap(v1_min_cam_x[0], v1_max_cam_x[0], v2_min_cam_x[0], v2_max_cam_x[0])

            # GETTING THE EQUATION FOR OBJECT 2 LINE IN CAMERA COORDINATES
            line_eq_object_1 = compute_line_equation(v1_min_cam_x, v1_max_cam_x)
            line_eq_object_2 = compute_line_equation(v2_min_cam_x, v2_max_cam_x)

            # GETTING THE VALUE OF EACH EQUATION AT THE CENTER OF THE OVERLAP
            line_1_y_at_overlap_centre_x = line_eq_object_1((x_camera_projections_overlap[0] + x_camera_projections_overlap[1])/2)
            line_2_at_overlap_centre_x = line_eq_object_2((x_camera_projections_overlap[0] + x_camera_projections_overlap[1])/2)

            # COMPARING ORDER IN WHICH LINES WILL BE CROSSED
            if line_1_y_at_overlap_centre_x > line_2_at_overlap_centre_x:
                front_object = object_2
                back_object = object_1
            else:
                front_object = object_1
                back_object = object_2

            """ HANDLING CASES WHEN AN OBJECT IS ABOVE A TEXTURE """
            if hasattr(object_1, 'asset') and hasattr(object_2, 'asset'):
                if hasattr(object_1.asset, 'type') and hasattr(object_2.asset, 'type'):
                        if object_1.asset.type == 'texture' and object_2.asset.type != 'texture':
                            if object_1.position[2] <= object_2.position[2]:
                                front_object = object_1
                                back_object = object_2
                        if object_1.asset.type != 'texture' and object_2.asset.type == 'texture':
                            if object_1.position[2] >= object_2.position[2]:
                                front_object = object_2
                                back_object = object_1
                
                if hasattr(object_1.asset, 'type') and not hasattr(object_2.asset, 'type'):
                        if object_1.asset.type == 'texture':
                            if object_1.position[2] <= object_2.position[2]:
                                front_object = object_1
                                back_object = object_2
    
                if not hasattr(object_1.asset, 'type') and hasattr(object_2.asset, 'type'):
                        if object_2.asset.type == 'texture':
                            if object_1.position[2] >= object_2.position[2]:
                                front_object = object_2
                                back_object = object_1




            """ FIGURING OUT WHETHER ONE OBJECT IS EXPLICITLY ABOVE THE OTHER """
            """ EPS = 5
            object_1_bottom_pos = object_1.position[2]
            object_1_top_pos = object_1.position[2] + object_1.height
            object_2_bottom_pos = object_2.position[2]
            object_2_top_pos = object_2.position[2] + object_2.height
            if object_1_bottom_pos > object_2_top_pos - EPS:
                front_object = object_2
                back_object = object_1
            elif object_2_bottom_pos > object_1_top_pos - EPS:
                front_object = object_1
                back_object = object_2 """
            
            """ if object_1.position[2] > object_2.position[2]:
                front_object = object_2
                back_object = object_1
            if object_2.position[2] > object_1.position[2]: 
                front_object = object_1
                back_object = object_2 """

            
            """ if overlap_y_camera:
                print('overlap y')
            print(random.randint(0, 0)) """

            """ if int(object_1.position[0]) == int(object_2.position[0]) and int(object_1.position[1]) == int(object_2.position[1]):
                if object_1.position[2] > object_2.position[2]:
                    front_object = object_2
                    back_object = object_1
                elif object_2.position[2] > object_1.position[2]:
                    front_object = object_1
                    back_object = object_2 """

            # CREATING GRAPH VERTEX
            adjacency_graph[front_object].add(back_object)

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