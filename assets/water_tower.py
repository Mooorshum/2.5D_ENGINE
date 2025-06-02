from graphics.sprite_stacks import SpritestackAsset

from objects.generic import CompositeObject


# COMPOSITE OBJECTS
water_tower_bottom = SpritestackAsset(type='water_tower_large', name='bottom', hitbox_size=(64,64))
water_tower_middle = SpritestackAsset(type='water_tower_large', name='middle', hitbox_size=(64,64))
water_tower_top = SpritestackAsset(type='water_tower_large', name='top', hitbox_size=(64,64))
water_tower_roof = SpritestackAsset(type='water_tower_large', name='roof', hitbox_size=(64,64))
WATER_TOWER_BOTTOM = CompositeObject(
    parts_positions_rotations=[
        (water_tower_bottom, [-32,32,0], 0),
        (water_tower_bottom, [-32,-32,0], -90),
        (water_tower_bottom, [32,-32,0], -180),
        (water_tower_bottom, [32,32,0], -270),
    ],
    hitbox_size=(128, 128),
)
WATER_TOWER_MIDDLE = CompositeObject(
    parts_positions_rotations=[
        (water_tower_middle, [-32,32,0], 0),
        (water_tower_middle, [-32,-32,0], -90),
        (water_tower_middle, [32,-32,0], -180),
        (water_tower_middle, [32,32,0], -270),
    ],
    hitbox_size=(128, 128),
)
WATER_TOWER_TOP = CompositeObject(
    parts_positions_rotations=[
        (water_tower_top, [-32,32,0], 0),
        (water_tower_top, [-32,-32,0], -90),
        (water_tower_top, [32,-32,0], -180),
        (water_tower_top, [32,32,0], -270),
    ],
    hitbox_size=(128, 128),
)
WATER_TOWER_ROOF = CompositeObject(
    parts_positions_rotations=[
        (water_tower_roof, [-32,32,0], 0),
        (water_tower_roof, [-32,-32,0], -90),
        (water_tower_roof, [32,-32,0], -180),
        (water_tower_roof, [32,32,0], -270),
    ],
    hitbox_size=(128, 128),
)
