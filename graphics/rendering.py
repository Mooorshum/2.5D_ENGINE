import pygame

from math import sin, cos, radians, sqrt

from objects.grass import GrassTile
from objects.plants import Plant
from objects.particles import ParticleSystem
from objects.generic import SpritestackModel, CompositeObject
from world_builder.loadpoints import LoadPoint


""" GETTING A LIST OF VISIBLE OBJECTS """
def get_visible_objects(screen, camera, objects):
    extra_padding = 100  # in world units

    # Calculate visible area in world space
    world_half_width = (screen.get_width() / 2) / camera.zoom + extra_padding
    world_half_height = (screen.get_height() / 2) / camera.zoom + extra_padding

    cam_x, cam_y = camera.position[0], camera.position[1]

    visible_objects = []
    for game_object in objects:
        obj_x, obj_y = game_object.position[0], game_object.position[1]

        is_in_frame_x = (cam_x - world_half_width <= obj_x <= cam_x + world_half_width)
        is_in_frame_y = (cam_y - world_half_height <= obj_y <= cam_y + world_half_height)

        if is_in_frame_x and is_in_frame_y:
            visible_objects.append(game_object)

    return visible_objects


""" RENDERING ALL DEPTH SORTED OBJECTS """
def global_render(screen, camera, sorted_objects, bend_objects=[], map_size=(1024, 1024), background=None):
    # CALCULATING ROTATED CAMERA X AND Y AXES
    camera_rotation = radians(camera.rotation)
    cam_x, cam_y = camera.position
    cam_w, cam_h = camera.width, camera.height

    # RENDERING BACKGROUND
    if background:
        tile_w = background.get_width()
        tile_h = background.get_height()
        half_w_world = cam_w / (2 * camera.zoom)
        half_h_world = cam_h / (2 * camera.zoom)
        extra_padding = sqrt(tile_w**2 + tile_h**2)
        min_x = int((cam_x - half_w_world - extra_padding) // tile_w) * tile_w
        max_x = int((cam_x + half_w_world + extra_padding) // tile_w + 1) * tile_w
        min_y = int((cam_y - half_h_world - extra_padding) // tile_h) * tile_h
        max_y = int((cam_y + half_h_world + extra_padding) // tile_h + 1) * tile_h

        rotated = pygame.transform.rotate(background, -camera.rotation)
        w, h = rotated.get_size()
        scaled = pygame.transform.scale(rotated, (int(w * camera.zoom), int(h * camera.zoom)))

        for x in range(min_x, max_x, tile_w):
            for y in range(min_y, max_y, tile_h):
                dx = x - cam_x
                dy = y - cam_y
                rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
                rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
                screen_x = cam_w // 2 + rot_dx * camera.zoom
                screen_y = cam_h // 2 + rot_dy * camera.zoom
                rect = scaled.get_rect(center=(screen_x, screen_y))
                screen.blit(scaled, rect)

    # RENDERING OBJECTS IN SORTED ORDER
    for game_object in sorted_objects:
        dx = game_object.position[0] - cam_x
        dy = game_object.position[1] - cam_y
        rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
        rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
        screen_x =  cam_w // 2 + rot_dx * camera.zoom - game_object.position[0]
        screen_y =  cam_h // 2 + rot_dy * camera.zoom - game_object.position[1]
        offset = [screen_x, screen_y]

        # UNIQUE RENDER FUNCTIONS
        if isinstance(game_object, Plant):
            game_object.render(screen, bend_objects, offset)
        elif isinstance(game_object, GrassTile):
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
