from graphics.sprite_stacks import SpritestackAsset

from objects.generic import CompositeObject

# COMPOSITE_OBJECTS
road_edge = SpritestackAsset(type='texture', name='road_1', hitbox_size=(64,64))
road_centre = SpritestackAsset(type='texture', name='road_2', hitbox_size=(64,64))
road_midway = SpritestackAsset(type='texture', name='road_3', hitbox_size=(64,64))

TWO_WAY_ROAD = CompositeObject(
    parts_positions_rotations=[
        (road_edge, [-128,-64,0], 0),
        (road_centre, [-128,0,0], 0),
        (road_edge, [-128,64,0], 180),
        (road_edge, [-64,-64,0], 0),
        (road_centre, [0-64,0,0], 0),
        (road_edge, [-64,64,0], 180),
        (road_edge, [0,-64,0], 0),
        (road_centre, [0,0,0], 0),
        (road_edge, [0,64,0], 180),
        (road_edge, [64,-64,0], 0),
        (road_centre, [64,0,0], 0),
        (road_edge, [64,64,0], 180),
        (road_edge, [128,-64,0], 0),
        (road_centre, [128,0,0], 0),
        (road_edge, [128,64,0], 180),
    ],
    type='texture',
    hitbox_size=(320, 192),
)