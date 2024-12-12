import os

import pygame

from math import sin, cos, sqrt, atan2, radians, copysign, degrees


def split_stack_image(stack_image):
    images = []
    resolution = stack_image.get_height()
    num_img = stack_image.get_width()//resolution
    for i in range(num_img):
        rect = pygame.Rect(i * resolution, 0, resolution, resolution)
        sub_image = stack_image.subsurface(rect).copy()
        images.append(sub_image)
    return images


def render_stack(images, position, rotation, screen, spread=1, scale=1):
    for i, img in enumerate(images):
        if scale != 1:
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        rotated_img = pygame.transform.rotate(img, rotation)
        screen.blit(
            rotated_img,
            (
                position[0] - rotated_img.get_width() // 2,
                position[1] - rotated_img.get_height() // 2 - i * spread * scale
            )
        )




class SpritestackModel:
    def __init__(self, type=None, name=None, scale=1):
        self.type = type
        self.name = name
        self.position = [100, 100]
        
        self.scale = scale
        self.hitbox_size = (0, 0)

        self.y0_offset = 0

        # Load stack images
        self.stack_index = 0
        self.stack_image_multiple = []
        self.slice_images_folder = f'assets/{self.type}/{self.name}/sprite_stacks/'
        self.num_stacks = len(os.listdir(f'assets/{self.type}/{self.name}/sprite_stacks/'))
        for i in range(self.num_stacks):
            stack_image = (
                pygame.image.load(
                    f'{self.slice_images_folder}stack_{i}.png'
                ).convert_alpha()
            )
            self.stack_image_multiple.append(split_stack_image(stack_image))

        # setting hitbox to the same size as the width of a spritestack image
        self.hitbox_size = (
            self.stack_image_multiple[0][0].get_width() * self.scale,
            self.stack_image_multiple[0][0].get_height() * self.scale
        )


    def render(self, screen, camera, offset=[0, 0], spread=0.8):
        if self.stack_index >= self.num_stacks:
            self.stack_index = 0
        stack_images = self.stack_image_multiple[self.stack_index]
        render_stack(
            stack_images,
            [
                self.position[0] + offset[0],
                self.position[1] + offset[1]
            ],
            self.rotation - camera.rotation,
            screen,
            spread,
            scale=self.scale
        )

        """ GETTING THE TOTAL OFFSET OF THE STACK """
        h = stack_images[0].get_height() / 2
        w = stack_images[0].get_width() / 2
        L = sqrt(h**2 + w**2)
        beta = atan2(h, w)
        self.y0_offset =  L * ( abs(sin(radians(self.rotation))) + abs(beta)) / 2 * self.scale 