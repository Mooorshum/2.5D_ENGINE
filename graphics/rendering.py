import pygame

from graphics import grass, shrubs


def global_render(screen, objects, camera_size, camera_position, bend_objects=[], offset=[0, 0]):
    render_padding = 10

    sorted_objects = sorted(objects, key=lambda obj: obj.position[1] + obj.y0_offset)

    for game_object in sorted_objects:

        is_in_frame_x = (game_object.position[0] > camera_position[0] - camera_size[0] / 2 - render_padding) and \
                        (game_object.position[0] < camera_position[0] + camera_size[0] / 2 + render_padding)

        is_in_frame_y = (game_object.position[1] > camera_position[1] - camera_size[1] / 2 - render_padding) and \
                        (game_object.position[1] < camera_position[1] + camera_size[1] / 2 + render_padding)
        
        if is_in_frame_x and is_in_frame_y:

            if isinstance(game_object, shrubs.Plant):
                game_object.render(screen, bend_objects, offset)
                colour = (0, 0, 255)

            elif isinstance(game_object, grass.GrassTile):
                game_object.render(screen, bend_objects, offset)
                """ game_object.render_tile_simple(screen, offset) """
                colour = (0, 255, 255)

            else:
                game_object.render(screen, offset)
                colour = (255, 0, 0)

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