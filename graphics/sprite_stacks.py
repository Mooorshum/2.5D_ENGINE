import os

import pygame

from copy import deepcopy

from math import sin, cos, sqrt, atan2, radians, copysign, degrees

from general_game_mechanics.collisions import Hitbox


pygame.init()


class SpritestackAsset:
    def __init__(self, type=None, name=None, hitbox_size=(64, 64), hitbox_offset=(0,0), hitbox_type='rectangle', mass=1000, spread=1, scale=1, y0_base_offset=0):
        self.type = type
        self.name = name

        self.scale = scale

        self.mass = mass

        self.slice_size = (0, 0)

        self.y0_base_offset = y0_base_offset
        self.y0_offset = 0

        self.height = 0

        # caching prerendered images of stacks for discrete angles
        self.spread = spread
        self.num_unique_angles = 180
        self.stack_angle_image = None

        # hitbox properties
        self.hitbox_size = hitbox_size
        self.hitbox_offset = hitbox_offset
        self.hitbox_type = hitbox_type

    def load_asset(self):  
        self.stack_angle_image = self.generate_images_cache(self.num_unique_angles, self.spread)
        

    def split_sheet_image(self, sheet_image):
        images = []
        resolution = sheet_image.get_height()
        num_img = sheet_image.get_width()//resolution
        for i in range(num_img):
            rect = pygame.Rect(i * resolution, 0, resolution, resolution)
            sub_image = sheet_image.subsurface(rect).copy()
            images.append(sub_image)
            images.append(sub_image) # DOUBLING EACH LAYER TO GET TILTED ORTHOGRAHIC PRESPECTIVE WITH HORIZONTALLY STRETCHED SCREEN
        self.height = len(images)
        return images


    def render_stack(self, images, spread, rotation):
        self.slice_size = (images[0].get_width(), images[0].get_height())
        slice_diagonal = sqrt(self.slice_size[0]**2 + self.slice_size[1]**2)
        render_surface = pygame.Surface(
            (
                slice_diagonal,
                slice_diagonal + len(images)*spread
            ),
            #pygame.SRCALPHA
        )

        for i, img in enumerate(images):
            rotated_img = pygame.transform.rotate(img, rotation)
            render_surface.blit(
                rotated_img,
                (
                    render_surface.get_width()/2 - rotated_img.get_width() // 2,
                    render_surface.get_height() - slice_diagonal/2 - rotated_img.get_height() // 2 - i * spread
                )
            )
        
        return render_surface


    def generate_images_cache(self, num_unique_angles, spread):
        stack_angle_image = []

        sheet_images_folder = f'asset_files/{self.type}/{self.name}/sprite_stacks'
        num_sheets = len(os.listdir(sheet_images_folder))
        for i in range(num_sheets):
            sheet_image = (
                pygame.image.load(
                    f'{sheet_images_folder}/stack_{i}.png'
                ).convert_alpha()
            )

            # Getting slice images for each sheet
            sheet_slices = self.split_sheet_image(sheet_image)

            # Generating images for all rotations
            rotation_image = {}
            angle_step = 360 / num_unique_angles
            rotation = 0
            for i in range(0, num_unique_angles):
                rotation += angle_step
                rotation_rendered_image = self.render_stack(sheet_slices, spread, rotation)
                rotation_image[rotation] = rotation_rendered_image
            stack_angle_image.append(rotation_image)
        
        return stack_angle_image




class SpritestackModel:
    def __init__(self, asset, asset_index, position, rotation, type=None, movelocked=True, collidable=False):
        self.type = type
        if hasattr(asset, 'type'):
            self.type = asset.type

        self.asset = asset
        self.asset_index = asset_index

        self.rotation = rotation
        self.position = position

        self.height = asset.height

        self.mass = self.asset.mass

        self.movelocked = movelocked
        self.collidable = collidable

        self.stack_index = 0
        self.internal_time = 0

        self.hitbox = Hitbox(
            object=self,
            size=self.asset.hitbox_size,
            hitbox_offset=self.asset.hitbox_offset,
            type=self.asset.hitbox_type
        )



    def render(self, screen, camera, offset=[0, 0]):
        true_rotation = ((self.rotation + 360)  - camera.rotation) % 360
        rounded_rotation = min(self.asset.stack_angle_image[self.stack_index].keys(), key=lambda k: abs(k - true_rotation))
        image = self.asset.stack_angle_image[self.stack_index][rounded_rotation]
        image.set_colorkey((0, 0, 0))


        zoom = camera.zoom
        w, h = image.get_width(), image.get_height()
        scaled_w, scaled_h = int(w * zoom), int(h * zoom)
        image = pygame.transform.scale(image, (scaled_w, scaled_h))

        draw_x = self.position[0] + offset[0] - scaled_w // 2
        draw_y = (self.position[1] + offset[1] - scaled_h + sqrt(self.asset.slice_size[0]**2 + self.asset.slice_size[1]**2) * 0.5 * zoom - self.position[2] * zoom)
    
        screen.blit(image, (draw_x, draw_y))



    def get_data(self):
        data = {}
        data['position'] = self.position
        data['rotation'] = self.rotation
        data['asset_index'] = self.asset_index
        return data
