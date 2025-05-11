import pygame

from math import sin, cos, radians, sqrt

from graphics import grass, plants
from graphics.particles import ParticleSystem
from graphics.sprite_stacks import SpritestackModel
from world_builder.loadpoints import LoadPoint

from general_game_mechanics.dynamic_objects import CompositeObject


""" GETTING A LIST OF VISIBLE OBJECTS """
def get_visible_objects(screen, camera, objects):
    extra_padding = 100
    render_padding_x = screen.get_width() / 2 + extra_padding
    render_padding_y = screen.get_height() / 2 + extra_padding

    visible_objects = []
    for game_object in objects:
        is_in_frame_x = (game_object.position[0] > camera.position[0] - render_padding_x) and \
                        (game_object.position[0] < camera.position[0] + render_padding_x)

        is_in_frame_y = ((game_object.position[1] > camera.position[1] - render_padding_y) and \
                        (game_object.position[1] < camera.position[1] + render_padding_y)) 
                            
        
        if is_in_frame_x and is_in_frame_y:

            visible_objects.append(game_object)
    return visible_objects


""" RENDERING ALL DEPTH SORTED OBJECTS """
def global_render(screen, camera, sorted_objects, bend_objects=[], map_size=(1024, 1024), background=None):
    # CALCULATING ROTATED CAMERA X AND Y AXES
    camera_rotation = radians(camera.rotation)

    # RENDERING BACKGROUND
    if background:
        padding = sqrt(background.get_width()**2 + background.get_height()**2) // 2
        cam_x, cam_y = camera.position
        cam_w, cam_h = camera.width, camera.height
        cam_rot_rad = radians(camera.rotation)
        cam_rot_deg = -camera.rotation
        tile_w = background.get_width()
        tile_h = background.get_height()
        for x in range(0, map_size[0], tile_w):
            for y in range(0, map_size[1], tile_h):
                # Simple visibility check (AABB)
                if cam_x - cam_w//2 - padding <= x <= cam_x + padding + cam_w//2 and cam_y - cam_h//2 - padding <= y <= cam_y + cam_h//2 + padding:
                    # CALCULATING OFFSET POSITION
                    dx = x - cam_x
                    dy = y - cam_y
                    rot_dx = dx * cos(cam_rot_rad) - dy * sin(cam_rot_rad)
                    rot_dy = dx * sin(cam_rot_rad) + dy * cos(cam_rot_rad)
                    screen_x = cam_w // 2 + rot_dx
                    screen_y = cam_h // 2 + rot_dy
                    # Rotate the tile and blit it centered
                    rotated = pygame.transform.rotate(background, -camera.rotation)
                    rect = rotated.get_rect(center=(screen_x, screen_y))
                    screen.blit(rotated, rect)

    # RENDERING OBJECTS IN SORTED ORDER
    for game_object in sorted_objects:
        # GETTING CAMERA TRANSLATIONAL + ROTATIONAL OFFSET
        offset_x = camera.position[0] - game_object.position[0] + (game_object.position[0] - camera.position[0])*cos(camera_rotation) - (game_object.position[1] - camera.position[1])*sin(camera_rotation)
        offset_y = camera.position[1] - game_object.position[1] + (game_object.position[0] - camera.position[0])*sin(camera_rotation) + (game_object.position[1] - camera.position[1])*cos(camera_rotation)
        offset = [offset_x - camera.position[0] + camera.width/2, offset_y - camera.position[1] + camera.height/2]

        # UNIQUE RENDER FUNCTIONS
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
        elif isinstance(game_object, CompositeObject):
            game_object.render(screen, camera, offset)

    """ rect_width, rect_height = 60, 40
    rect_image = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    rect_image.fill((255, 0, 0))  # Red rectangl
    horizontal_stretch = pygame.transform.scale(rect_image, (rect_width * 2, rect_height))
    vertical_stretch = pygame.transform.scale(rect_image, (rect_width, rect_height * 2))
    x0, y0 = screen.get_width()/2, screen.get_height()/2

    screen.blit(rect_image, (x0, y0))
    screen.blit(horizontal_stretch, (x0 + 200, y0))
    screen.blit(vertical_stretch, (x0 + 400, y0)) """
