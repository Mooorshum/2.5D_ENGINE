from graphics import grass, shrubs


def global_render(screen, objects, bend_objects=[], offset=[0, 0]):

    sorted_objects = sorted(objects, key=lambda obj: obj.position[1] + obj.image_size_y/2)

    for game_object in sorted_objects:
        """ if (game_object.position[0] - offset[0]) and (game_object.position[1] - offset[1]): """
        if (game_object.position[0] < 1000) and (game_object.position[1] < 500):

            if isinstance(game_object, shrubs.Plant):
                game_object.render(screen, bend_objects, offset)

            elif isinstance(game_object, grass.GrassTile):
                game_object.render(screen, bend_objects, offset)
                """ game_object.render_tile_simple(screen, offset) """

            else:
                game_object.render(screen, offset)