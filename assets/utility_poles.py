from graphics.sprite_stacks import SpritestackAsset

from objects.generic import CompositeObject

# COMPOSITE OBJECTS
utility_pole_bottom = SpritestackAsset(type='building_decor', name='utility_pole_bottom', hitbox_size=(10,10), hitbox_type='rectangle')
utility_pole_middle = SpritestackAsset(type='building_decor', name='utility_pole_middle', hitbox_size=(10,10), hitbox_type='rectangle')
utility_pole_top = SpritestackAsset(type='building_decor', name='utility_pole_top_multiple', hitbox_size=(32,32), hitbox_type='rectangle')
utility_pole_wires = SpritestackAsset(type='building_decor', name='wires_straight', hitbox_size=(10,32), hitbox_type='rectangle')
WOODEN_POLE = CompositeObject(
    parts_positions_rotations=[
        (utility_pole_bottom, [0,0,0], 0),
        (utility_pole_middle, [0,0,64*2], 0),
        (utility_pole_top, [0,0,128*2], 0),
    ],
    hitbox_size=(32, 32),
    hitbox_type='circle',
)
WIRELINE = CompositeObject(
    parts_positions_rotations=[
        (utility_pole_wires, [-96,0,0], 90),
        (utility_pole_wires, [-64,0,0], 90),
        (utility_pole_wires, [-32,0,0,], 90),
        (utility_pole_wires, [0,0,0], 90),
        (utility_pole_wires, [32,0,0], 90),
        (utility_pole_wires, [64,0,0], 90),
        (utility_pole_wires, [96,0,0], 90),
    ],
    hitbox_size=(224, 32),
)
