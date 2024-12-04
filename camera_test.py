import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Camera Viewport Example with Object")

# Load a background image
background_image = pygame.image.load("background.png").convert()
background_width, background_height = background_image.get_size()

# Camera class
class Camera:
    def __init__(self, width, height, max_width, max_height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.max_width = max_width
        self.max_height = max_height

    def move(self, dx, dy):
        """Move the camera while keeping it within bounds."""
        self.rect.x = max(0, min(self.rect.x + dx, self.max_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + dy, self.max_height - self.rect.height))

# Create a camera
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, background_width, background_height)

# Define a rectangle at the center of the background
rectangle_width, rectangle_height = 50, 50
rectangle_color = (255, 0, 0)
rectangle_position = (
    background_width // 2 - rectangle_width // 2,
    background_height // 2 - rectangle_height // 2,
)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle keys for camera movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        camera.move(5, 0)
    if keys[pygame.K_UP]:
        camera.move(0, -5)
    if keys[pygame.K_DOWN]:
        camera.move(0, 5)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the portion of the background visible through the camera
    screen.blit(background_image, (0, 0), camera.rect)

    # Calculate rectangle position relative to the camera
    rect_x = rectangle_position[0] - camera.rect.x
    rect_y = rectangle_position[1] - camera.rect.y

    # Draw the rectangle
    pygame.draw.rect(screen, rectangle_color, (rect_x, rect_y, rectangle_width, rectangle_height))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
