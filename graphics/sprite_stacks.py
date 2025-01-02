import os

import pygame

from math import sin, cos, sqrt, atan2, radians, copysign, degrees


class SpritestackModel:
    def __init__(self, type=None, name=None, hitbox_size=(64, 64), spread=1, scale=1, y0_base_offset=0):
        self.type = type
        self.name = name

        self.stack_index = 0
        self.internal_time = 0

        self.rotation = 0
        self.position = [0, 0]
        
        self.scale = scale

        self.slice_size = (0, 0)

        self.y0_base_offset = y0_base_offset
        self.y0_offset = 0

        # caching prerendered images of stacks for discrete angles
        num_unique_angles = 90
        self.stack_angle_image = self.generate_images_cache(num_unique_angles, spread)

        # providing scaled hitbox size
        self.hitbox_size = (hitbox_size[0]*scale, hitbox_size[1]*scale)


    def split_sheet_image(self, sheet_image):
        images = []
        resolution = sheet_image.get_height()
        num_img = sheet_image.get_width()//resolution
        for i in range(num_img):
            rect = pygame.Rect(i * resolution, 0, resolution, resolution)
            sub_image = sheet_image.subsurface(rect).copy()
            images.append(sub_image)
        return images


    def render_stack(self, images, spread, rotation):
        self.slice_size = (images[0].get_width(), images[0].get_height())
        slice_diagonal = sqrt(self.slice_size[0]**2 + self.slice_size[1]**2)
        render_surface = pygame.Surface(
            (
                slice_diagonal,
                slice_diagonal + len(images)*spread,
            ),
            pygame.SRCALPHA
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
                rotation_image[rotation] = self.render_stack(sheet_slices, spread, rotation)
            stack_angle_image.append(rotation_image)
        
        return stack_angle_image




    def render(self, screen, camera, offset=[0, 0]):

        true_rotation = ((self.rotation + 360)  - camera.rotation) % 360
        rounded_rotation = min(self.stack_angle_image[self.stack_index].keys(), key=lambda k: abs(k - true_rotation))
        image = self.stack_angle_image[self.stack_index][rounded_rotation]

        screen.blit(
            image,
            (
                self.position[0] - image.get_width() // 2 + offset[0],
                self.position[1] - image.get_height() + sqrt(self.slice_size[0]**2 + self.slice_size[1]**2)/2 + offset[1]
            )
        )

        """ # DRAWING OBJECT HITBOX
        rect_surface = pygame.Surface((self.hitbox_size[0], self.hitbox_size[1]), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, (255, 0, 0), rect_surface.get_rect(), 1)
        rotated_surface = pygame.transform.rotate(rect_surface, self.rotation - camera.rotation)
        rotated_rect = rotated_surface.get_rect(center=(self.position[0] + offset[0], self.position[1] + offset[1]))
        screen.blit(rotated_surface, rotated_rect.topleft) """


        """ UPDATING THE TOTAL Y0_OFFSET OF THE OBJECT """
        h = self.hitbox_size[1]/ 2
        w = self.hitbox_size[0] / 2
        L = sqrt(h**2 + w**2)
        beta = atan2(h, w)
        self.y0_offset =  self.y0_base_offset + L * ( abs(sin(radians(self.rotation))) + abs(beta)) / 2 * self.scale


