import os

import pygame

from copy import deepcopy

from math import sin, cos, sqrt, atan2, radians, copysign, degrees

from general_game_mechanics.collisions import Hitbox


class SpritestackAsset:
    def __init__(self, type=None, name=None, hitbox_size=(32, 32), render_box_size=None, render_layer_offset=0, hitbox_type='circle', mass=10, spread=1, scale=1, y0_base_offset=0, movelocked=True, interactable=True):
        self.type = type
        self.name = name

        self.scale = scale

        self.mass = mass

        self.movelocked = movelocked
        self.interactable = interactable

        self.slice_size = (0, 0)

        self.y0_base_offset = y0_base_offset
        self.y0_offset = 0

        self.height = 0

        self.render_layer_offset = render_layer_offset

        # caching prerendered images of stacks for discrete angles
        self.spread = spread
        self.num_unique_angles = 180
        self.stack_angle_image = self.generate_images_cache(self.num_unique_angles, self.spread)

        # providing scaled hitbox size
        self.hitbox_size = hitbox_size
        self.render_box_size = render_box_size if render_box_size is not None else hitbox_size
        self.hitbox_type = hitbox_type
        

    def split_sheet_image(self, sheet_image):
        images = []
        resolution = sheet_image.get_height()
        num_img = sheet_image.get_width()//resolution
        for i in range(num_img):
            rect = pygame.Rect(i * resolution, 0, resolution, resolution)
            sub_image = sheet_image.subsurface(rect).copy()
            images.append(sub_image)
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

        sheet_images_folder = f'assets/{self.type}/{self.name}/sprite_stacks'
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
                if self.scale != 1:
                    rotation_rendered_image = pygame.transform.scale(
                        rotation_rendered_image,
                        (
                            (rotation_rendered_image.get_width() * self.scale),
                            (rotation_rendered_image.get_height() * self.scale)
                        )
                    )
                rotation_image[rotation] = rotation_rendered_image
            stack_angle_image.append(rotation_image)
        
        return stack_angle_image




class SpritestackModel:
    def __init__(self, asset, asset_index, position, rotation):

        self.asset = asset
        self.asset_index = asset_index

        self.rotation = rotation
        self.position = position

        self.height = asset.height

        self.mass = self.asset.mass

        self.movelocked = self.asset.movelocked
        self.interactable = self.asset.interactable

        self.stack_index = 0
        self.internal_time = 0

        self.render_layer_offset = self.asset.render_layer_offset
        self.hitbox = Hitbox(
            object=self,
            size=self.asset.hitbox_size,
            render_box_size=self.asset.render_box_size,
            type=self.asset.hitbox_type
        )



    def render(self, screen, camera, offset=[0, 0]):

        true_rotation = ((self.rotation + 360)  - camera.rotation) % 360
        rounded_rotation = min(self.asset.stack_angle_image[self.stack_index].keys(), key=lambda k: abs(k - true_rotation))
        image = self.asset.stack_angle_image[self.stack_index][rounded_rotation]
        image.set_colorkey((0, 0, 0))
        screen.blit(
            image,
            (
                self.position[0] - image.get_width() // 2 + offset[0],
                self.position[1] - image.get_height() + sqrt(self.asset.slice_size[0]**2 + self.asset.slice_size[1]**2)/2 + offset[1] - self.position[2]
            )
        )


    def get_data(self):
        data = {}
        data['position'] = self.position
        data['rotation'] = self.rotation
        data['asset_index'] = self.asset_index
        return data
