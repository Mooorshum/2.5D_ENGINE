import pygame


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
