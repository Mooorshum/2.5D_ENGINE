from graphics.sprite_stacks import SpritestackAsset

from objects.vehicles import Vehicle


MINIVAN = Vehicle(
    parts_positions_rotations=[
        (SpritestackAsset(type='minivan', name='back', hitbox_size=(64,64)), [-32,0,0], 0),
        (SpritestackAsset(type='minivan', name='front', hitbox_size=(64,64)), [32,0,0], 0),
    ],
    hitbox_size=(128, 64)
)


DELIVERY_TRUCK = Vehicle(
    parts_positions_rotations=[
        (SpritestackAsset(type='delivery_truck', name='front', hitbox_size=(64,64)), [64,0,0], 0),
        (SpritestackAsset(type='delivery_truck', name='middle', hitbox_size=(64,64)), [0,0,0], 0),
        (SpritestackAsset(type='delivery_truck', name='back', hitbox_size=(64,64)), [-64,0,0], 0),
    ],
    hitbox_size=(192, 64),
)