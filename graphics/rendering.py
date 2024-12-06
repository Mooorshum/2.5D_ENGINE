from graphics import grass, shrubs

import pygame


def global_render(screen, objects, bend_objects=[], offset=[0, 0]):

    sorted_objects = sorted(objects, key=lambda obj: obj.position[1])

    for game_object in sorted_objects:
        if (game_object.position[1] - offset[1]) and (game_object.position[1] - offset[1]):

            if isinstance(game_object, shrubs.Plant):
                game_object.render(screen, bend_objects, offset)

            elif isinstance(game_object, grass.GrassTile):
                game_object.render(screen, bend_objects, offset)
                
            else:
                game_object.render(screen, offset)