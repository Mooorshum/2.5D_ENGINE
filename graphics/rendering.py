import pygame

from math import sin, cos, radians

from graphics import grass, shrubs
from graphics.particles import ParticleSystem, FogCloud
from graphics.sprite_stacks import SpritestackModel

from general_game_mechanics.dynamic_objects import Vehicle




def global_render(screen, camera, objects, bend_objects=[]):
    render_padding_x = screen.get_width() / 2 + 100
    render_padding_y = screen.get_height() / 2 + 100

    """ SORTING THE LIST OF RENDERED OBJECTS TO EMULATE DEPTH """
    def calculate_sort_key(object):
        camera_rotation = radians(camera.rotation)
        rotated_y = (object.position[0] - camera.position[0]) * sin(camera_rotation) + (object.position[1] - camera.position[1]) * cos(camera_rotation)
        return rotated_y + object.y0_offset
    sorted_objects = sorted(objects, key=calculate_sort_key)

    for game_object in sorted_objects:

        is_in_frame_x = (game_object.position[0] > camera.position[0] - render_padding_x) and \
                        (game_object.position[0] < camera.position[0] + render_padding_x)

        is_in_frame_y = (game_object.position[1] > camera.position[1] - render_padding_y) and \
                        (game_object.position[1] < camera.position[1] + render_padding_y)
        
        if is_in_frame_x and is_in_frame_y:
            
            """ CALCULATING EACH OBJECT'S OFFSET AND ROTATION,
            WHICH DEPENDS ON IT'S POSITION RELATIVE TO THE CAMERA,
            AS WELL AS THE CAMERA ROTATION ANGLE """
            camera_rotation = radians(camera.rotation)
            offset_x = camera.position[0] - game_object.position[0] + (game_object.position[0] - camera.position[0])*cos(camera_rotation) - (game_object.position[1] - camera.position[1])*sin(camera_rotation)
            offset_y = camera.position[1] - game_object.position[1] + (game_object.position[0] - camera.position[0])*sin(camera_rotation) + (game_object.position[1] - camera.position[1])*cos(camera_rotation)
            offset = [offset_x - camera.position[0] + camera.width/2, offset_y - camera.position[1] + camera.height/2]

            if isinstance(game_object, shrubs.Plant):
                game_object.render(screen, bend_objects, offset)
                colour = (0, 0, 255)

            elif isinstance(game_object, grass.GrassTile):
                game_object.render(screen, bend_objects, offset)
                colour = (0, 255, 255)

            elif isinstance(game_object, SpritestackModel):
                game_object.render(screen, camera, offset)

            elif isinstance(game_object, ParticleSystem):
                game_object.render(screen, camera)
            
            elif isinstance(game_object, FogCloud):
                game_object.render(screen, camera)





            # circle indicator
            """ pygame.draw.circle(
                screen,
                colour,
                (
                    game_object.position[0] + offset[0],
                    game_object.position[1] + offset[1] + game_object.y0_offset
                ),
                3,
            ) """