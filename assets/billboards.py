from graphics.sprite_stacks import SpritestackAsset

from objects.generic import CompositeObject


# COMPOSITE OBJECTS
beanz_billboard_pillar_bottom = SpritestackAsset(type='billboard_beans', name='pillar_bottom', hitbox_size=(64,64))
beanz_billboard_pillar_top = SpritestackAsset(type='billboard_beans', name='pillar_top', hitbox_size=(64,64))
beanz_billboard_sign_left = SpritestackAsset(type='billboard_beans', name='sign_left', hitbox_size=(64,64))
beanz_billboard_sign_middle = SpritestackAsset(type='billboard_beans', name='sign_middle', hitbox_size=(64,64))
beanz_billboard_sign_right = SpritestackAsset(type='billboard_beans', name='sign_right', hitbox_size=(64,64))
BEANZ_BILLBOARD = CompositeObject(
    parts_positions_rotations=[
        (beanz_billboard_pillar_bottom, [0,0,0*2], 0),
        (beanz_billboard_pillar_top, [0,0,64*2], 0),
        (beanz_billboard_sign_left, [-64,0,128*2], 0),
        (beanz_billboard_sign_middle, [0,0,128*2], 0),
        (beanz_billboard_sign_right, [64,0,128*2], 0),
    ],
    hitbox_size=(32, 32),
)
