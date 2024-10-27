import sys
import os
import pygame

pygame.init()

screen = pygame.display.set_mode((900, 640))
display = pygame.Surface((1000, 1000))

images_folder = 'assets/3d_models/hippie_bus/'
images = [pygame.image.load(images_folder + img) for img in sorted(os.listdir(images_folder), key=lambda x: int(os.path.splitext(x)[0]))]

clock = pygame.time.Clock()

def render_stack(surf, images, pos, rotation, spread=1, scale=1):
    for i, img in enumerate(images):
        if scale != 1:
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        rotated_img = pygame.transform.rotate(img, rotation)
        surf.blit(
            rotated_img,
            (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread * scale)
        )

frame = 0

while True:
    frame += 1
    
    display.fill((0, 0, 0))
    
    render_stack(display, images, (300, 300), frame, spread=7, scale=0.5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)
