from graphics.sprite_stacks import SpritestackAsset

from objects.generic import CompositeObject


diner_wall_corner = SpritestackAsset(type='diner', name='wall_corner', hitbox_size=(64,64))
diner_wall_window = SpritestackAsset(type='diner', name='wall_window', hitbox_size=(64,64))
diner_wall_front_entrance = SpritestackAsset(type='diner', name='wall_front_entrance', hitbox_size=(64,64))
diner_wall_back = SpritestackAsset(type='diner', name='wall_back', hitbox_size=(64,64))
diner_roof_corner = SpritestackAsset(type='diner', name='roof_corner', hitbox_size=(64,64))
diner_roof_side = SpritestackAsset(type='diner', name='roof_side', hitbox_size=(64,64))
diner_roof_middle = SpritestackAsset(type='diner', name='roof_middle', hitbox_size=(64,64))
diner_roof_sign_left = SpritestackAsset(type='diner', name='roof_sign_left', hitbox_size=(64,64))
diner_roof_sign_middle = SpritestackAsset(type='diner', name='roof_sign_middle', hitbox_size=(64,64))
diner_roof_sign_right = SpritestackAsset(type='diner', name='roof_sign_right', hitbox_size=(64,64))
DINER_WALLS = CompositeObject(
    parts_positions_rotations=[
        (diner_wall_corner, [-128,64,0], 0),
        (diner_wall_window, [-64,64,0], 0),
        (diner_wall_front_entrance, [0,64,0], 0),
        (diner_wall_window, [64,64,0], 0),
        (diner_wall_corner, [128,64,0], 90),
        (diner_wall_window, [128,0,0], 90),
        (diner_wall_corner, [128,-64,0], 180),
        (diner_wall_back, [64,-64,0], 180),
        (diner_wall_back, [0,-64,0], 180),
        (diner_wall_back, [-64,-64,0], 180),
        (diner_wall_corner, [-128,-64,0], 270),
        (diner_wall_window, [-128,0,0], 270),
    ],
    hitbox_size=(320, 192),
)
DINER_ROOF = CompositeObject(
    parts_positions_rotations=[
        (diner_roof_corner, [-128,64,0], 0),
        (diner_roof_sign_left, [-64,64,0], 0),
        (diner_roof_sign_middle, [0,64,0], 0),
        (diner_roof_sign_right, [64,64,0], 0),
        (diner_roof_corner, [128,64,0], 90),
        (diner_roof_side, [128,0,0], 90),
        (diner_roof_corner, [128,-64,0], 180),
        (diner_roof_side, [64,-64,0], 180),
        (diner_roof_side, [0,-64,0], 180),
        (diner_roof_side, [-64,-64,0], 180),
        (diner_roof_corner, [-128,-64,0], 270),
        (diner_roof_side, [-128,0,0], 270),
        (diner_roof_middle, [-64,0,0], 0),
        (diner_roof_middle, [0,0,0], 0),
        (diner_roof_middle, [64,0,0], 0),
    ],
    hitbox_size=(320, 192),
)

