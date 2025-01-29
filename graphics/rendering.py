import pygame

from math import sin, cos, radians

from graphics import grass, plants
from graphics.particles import ParticleSystem
from graphics.sprite_stacks import SpritestackModel

from world_builder.loadpoints import LoadPoint

from general_game_mechanics.water import WaterBody


def global_render(screen, camera, objects, bend_objects=[], background=None):
    extra_padding = 100
    render_padding_x = screen.get_width() / 2 + extra_padding
    render_padding_y = screen.get_height() / 2 + extra_padding


    """ RENDERING BACKGROUND IN CAMERA REFERENCE FRAME """
    if background:
        camera_rotation = radians(camera.rotation)
        background_position = (
            camera.map_width/2,
            camera.map_height/2
        )
        background_offset_x = camera.position[0] - background_position[0] + (background_position[0] - camera.position[0])*cos(camera_rotation) - (background_position[1] - camera.position[1])*sin(camera_rotation)
        background_offset_y = camera.position[1] - background_position[1] + (background_position[0] - camera.position[0])*sin(camera_rotation) + (background_position[1] - camera.position[1])*cos(camera_rotation)
        background_offset = [background_offset_x - camera.position[0] + camera.width/2, background_offset_y - camera.position[1] + camera.height/2]

        background_position = (
            camera.map_width/2 + background_offset[0],
            camera.map_height/2 + background_offset[1]
        )

        background_rotated = pygame.transform.rotate(background, -camera.rotation)

        screen.blit(
            background_rotated,
            (
                background_position[0] - background_rotated.get_width() // 2,
                background_position[1] - background_rotated.get_height() // 2
            )
        )


    """ SORTING THE LIST OF RENDERED OBJECTS TO EMULATE DEPTH """
    def calculate_sort_key(object):
        camera_rotation = radians(camera.rotation)
        rotated_y = (object.position[0] - camera.position[0]) * sin(camera_rotation) + (object.position[1] - camera.position[1]) * cos(camera_rotation)
        return rotated_y + object.y0_offset
    
    if len(objects) > 0:
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
    
                if isinstance(game_object, plants.Plant):
                    game_object.render(screen, bend_objects, offset)
    
                elif isinstance(game_object, grass.GrassTile):
                    game_object.render(screen, bend_objects, offset)
    
                elif isinstance(game_object, SpritestackModel):
                    game_object.render(screen, camera, offset)

                elif isinstance(game_object, WaterBody):
                    game_object.render(screen, camera, offset)
                
                elif isinstance(game_object, ParticleSystem):
                    game_object.render(screen, camera)

                elif isinstance(game_object, LoadPoint):
                    game_object.render(screen, offset)
    
    
    
    
    
                # circle indicator of object y0_offset for depth sorting
                """ pygame.draw.circle(
                    screen,
                    colour,
                    (
                        game_object.position[0] + offset[0],
                        game_object.position[1] + offset[1] + game_object.y0_offset
                    ),
                    3,
                ) """