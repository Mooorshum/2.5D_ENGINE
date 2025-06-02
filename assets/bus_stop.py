from graphics.sprite_stacks import SpritestackAsset

from objects.generic import CompositeObject


# COMPOSITE OBJECTS
bus_stop_bottom_left = SpritestackAsset(type='bus_stop', name='bottom_left', hitbox_size=(64,64))
bus_stop_bottom_right = SpritestackAsset(type='bus_stop', name='bottom_right', hitbox_size=(64,64))
bus_stop_roof_left = SpritestackAsset(type='bus_stop', name='roof_left', hitbox_size=(64,64))
bus_stop_roof_right = SpritestackAsset(type='bus_stop', name='roof_right', hitbox_size=(64,64))
BUS_STOP = CompositeObject(
    parts_positions_rotations=[
        (bus_stop_bottom_left, [-32,0,0*2], 0),
        (bus_stop_bottom_right, [32,0,0*2], 0),
        (bus_stop_roof_left, [-32,0,64*2], 0),
        (bus_stop_roof_right, [32,0,64*2], 0),
    ],
    hitbox_size=(128, 64),
)