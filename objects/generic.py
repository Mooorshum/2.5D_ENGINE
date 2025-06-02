import pygame

from math import sin, cos, atan2, degrees, pi, sqrt, radians
from numpy import sign

from general_game_mechanics.collisions import Hitbox

from graphics.sprite_stacks import SpritestackModel

from graphics.topological_sorting import depth_sort


class DynamicObject(SpritestackModel):
    def __init__(self, asset, asset_index, position, rotation, type=None):
        super().__init__(asset, asset_index, position, rotation, type=type)

        self.v_drag = 0.03
        self.omega_drag = 0.05
        self.dt = 0.01

        self.mass = asset.mass

        self.vx = 0
        self.vy = 0
        self.omega = 0

        self.ax = 0
        self.ay = 0
        self.a_omega = 0

        self.ground_effect_particle_system = None


    def move(self):
        if not self.movelocked:

            new_vx = (self.vx + self.ax * self.dt) * ( 1 - self.v_drag)
            new_vy = (self.vy + self.ay * self.dt) * ( 1 - self.v_drag)
            new_omega = (self.omega +  self.a_omega * self.dt) * ( 1 - self.omega_drag)

            new_x = self.position[0] + new_vx * self.dt
            new_y = self.position[1] - new_vy * self.dt
            new_rotation = self.rotation + new_omega * self.dt

            self.vx = new_vx
            self.vy = new_vy
            self.omega = new_omega

            self.position[0] = new_x
            self.position[1] = new_y
            self.rotation = new_rotation

    def render(self, screen, camera, offset=[0, 0]):
        super().render(screen, camera, offset)
        self.hitbox.render(screen, camera, offset)

        if self.ground_effect_particle_system:
            self.ground_effect_particle_system.position = self.position
            self.ground_effect_particle_system.render(screen, camera)
            self.ground_effect_particle_system.update()


""" SPECIAL CLASS OF OBJECT CONSISTING OF MULTIPLE SEPARATELY RENDERABLE PARTS """
class CompositeObject():
    def __init__(self, parts_positions_rotations, type=None, position=[0,0,0], rotation=0, hitbox_size=[64,64], hitbox_offset=(0,0), hitbox_type='rectangle', asset_index=None):

        self.type = type

        self.asset_index = asset_index

        self.movelocked = True
        self.collidable = False

        self.position = position
        self.rotation = rotation

        # Initializing component parts
        self.parts_positions_rotations_for_copy = parts_positions_rotations
        self.parts = []
        self.part_assets = []
        self.part_positions_nonrotated = []
        self.part_rotations_nonrotated = []
        
        for part_id in range(len(parts_positions_rotations)):
            part_info = parts_positions_rotations[part_id]
            part_asset_index = part_id # REWORK THIS WHEN IMPLEMENTING SERIALIZATION
            part_asset = part_info[0]
            if part_asset not in self.part_assets:
                self.part_assets.append(part_asset)
            part = DynamicObject(part_asset, part_asset_index, [0,0,0], 0)
            self.parts.append(part)
            self.part_positions_nonrotated.append(part_info[1])
            self.part_rotations_nonrotated.append(part_info[2])
        
        # Placing component parts in predefined positions & calculating object height
        max_ceiling = 0
        for part_index in range(len(self.parts)):
            part = self.parts[part_index]
            x_rel, y_rel, z_rel = self.part_positions_nonrotated[part_index]
            #z_rel *= 2 # MULTIPLYING RELATIVE POSITION TO ACCOUNT FOR SLICE DOUBLING (IN SpriteStackAsset CLASS)
            part_rotation = self.part_rotations_nonrotated[part_index]
            part.position[0] = self.position[0] + x_rel
            part.position[1] = self.position[1] + y_rel
            part.position[2] = self.position[2] + z_rel
            part.rotation = part_rotation
            part.hitbox.update() # UPDATING PART HITBOX VERTICES TO MATCH ITS POSITION

            ceiling = z_rel + part.height
            if ceiling > max_ceiling:
                max_ceiling = ceiling
        self.height = max_ceiling

        # Creating a single hitbox for the whole object
        self.hitbox_size_for_copy = hitbox_size
        self.hitbox = Hitbox(
            object=self,
            size=hitbox_size,
            hitbox_offset=hitbox_offset,
            type=hitbox_type
        )

        self.mass = sum(part.mass for part in self.parts)

        self.v_drag = 0.03
        self.omega_drag = 0.05
        self.dt = 0.01

        self.vx = 0
        self.vy = 0
        self.omega = 0

        self.ax = 0
        self.ay = 0
        self.a_omega = 0

        # TOPOLOGICAL DEPTH SORT SETTINGS
        self.depth_sort_pause_time = 10 # Number of iterations between depth sort calls
        self.depth_sort_timer = 0
        self.depth_sorted_parts = []
        self.asset_placement_mode = True # if this is false, the depth sort will be called every interation (used to render a level asset during editing)
        
    def load_asset(self):
        for asset in self.part_assets:
            asset.load_asset()

    def move(self):
        if not self.movelocked:

            new_vx = (self.vx + self.ax * self.dt) * ( 1 - self.v_drag)
            new_vy = (self.vy + self.ay * self.dt) * ( 1 - self.v_drag)
            new_omega = (self.omega +  self.a_omega * self.dt) * ( 1 - self.omega_drag)

            new_x = self.position[0] + new_vx * self.dt
            new_y = self.position[1] - new_vy * self.dt
            new_rotation = self.rotation + new_omega * self.dt

            self.vx = new_vx
            self.vy = new_vy
            self.omega = new_omega

            self.position[0] = new_x
            self.position[1] = new_y
            self.rotation = new_rotation

            # UPDATING THE POSITIONS OF COMPONENT PARTS
            cos_r = cos(radians(self.rotation))
            sin_r = -sin(radians(self.rotation))

            for part_index in range(len(self.parts)):
                part = self.parts[part_index]
                x_rel, y_rel, z_rel = self.part_positions_nonrotated[part_index]
                x_rot = cos_r * x_rel - sin_r * y_rel
                y_rot = sin_r * x_rel + cos_r * y_rel
                part.position[0] = self.position[0] + x_rot
                part.position[1] = self.position[1] + y_rot
                part.position[2] = self.position[2] + z_rel
                part_rotation = self.part_rotations_nonrotated[part_index]
                part.rotation = part_rotation + self.rotation

            # UPDATING COMPONENT HITBOX VERTICES
            EPS = 1 # Speed threshold
            if sqrt(self.vx**2 + self.vy**2) > EPS:
                for part in self.parts:
                    part.hitbox.update()

    def render(self, screen, camera, offset):
        # rendering hitbox
        if self.collidable or not self.movelocked:
            if self.collidable:
                self.hitbox.colour = (255, 0, 0)
            if not self.movelocked:
                self.hitbox.colour = (0, 255, 0)
            camera_rotation = radians(camera.rotation)
            zoom = camera.zoom
            cam_x, cam_y = camera.position
            cam_w, cam_h = camera.width, camera.height
            dx = self.position[0] - cam_x
            dy = self.position[1] - cam_y
            rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
            rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
            screen_x =  cam_w // 2 + rot_dx * zoom - self.position[0]
            screen_y =  cam_h // 2 + rot_dy * zoom - self.position[1]
            self_offset = [screen_x, screen_y]
            self.hitbox.render(screen, camera, self_offset)
        else:
            self.hitbox.show_hitbox = False

        # Individual depth sorting
        if not self.asset_placement_mode: # reordering is done once every N iterations
            if self.depth_sort_timer > self.depth_sort_pause_time: 
                self.depth_sorted_parts = depth_sort(self.parts, camera)
                self.depth_sort_timer = 0
            self.depth_sort_timer += 1
        else: # reordering every iteration
            self.asset_placement_mode = False
            self.depth_sorted_parts = depth_sort(self.parts, camera)
        camera_rotation = radians(camera.rotation)
        zoom = camera.zoom
        for part in self.depth_sorted_parts:

            camera_rotation = radians(camera.rotation)
            zoom = camera.zoom
            cam_x, cam_y = camera.position
            cam_w, cam_h = camera.width, camera.height
            dx = part.position[0] - cam_x
            dy = part.position[1] - cam_y
            rot_dx = dx * cos(camera_rotation) - dy * sin(camera_rotation)
            rot_dy = dx * sin(camera_rotation) + dy * cos(camera_rotation)
            screen_x =  cam_w // 2 + rot_dx * zoom - part.position[0]
            screen_y =  cam_h // 2 + rot_dy * zoom - part.position[1]
            part_offset = [screen_x, screen_y]
            """ part_offset_x = camera.position[0] - part.position[0] + (part.position[0] - camera.position[0])*cos(camera_rotation) - (part.position[1] - camera.position[1])*sin(camera_rotation)
            part_offset_y = camera.position[1] - part.position[1] + (part.position[0] - camera.position[0])*sin(camera_rotation) + (part.position[1] - camera.position[1])*cos(camera_rotation)
            part_offset = [part_offset_x - camera.position[0] + camera.width/2, part_offset_y - camera.position[1] + camera.height/2] """
            part.render(screen, camera, part_offset)

    def get_data(self):
        data = {}
        data['position'] = self.position
        data['rotation'] = self.rotation

        data['asset_index'] = self.asset_index
        return data










