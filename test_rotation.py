import pygame
import random
from math import sin, cos, radians

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Camera Rotation Demo")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Camera class
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = [width//2, height//2]  # Initial position in the center
        self.rotation = 0  # Angle in degrees

# Generate random circles
circles = []
for x in range(WIDTH//10, WIDTH, WIDTH//10):
    for y in range(HEIGHT//10, HEIGHT, HEIGHT//10):
        circles.append(
            {
                "position": [x, y],  # Use list to update position
                "radius": 5,
            }
        )

# Initialize camera
camera = Camera(WIDTH, HEIGHT)

# Velocity for camera's linear movement in the x-direction (before rotation)
velocity_x = 2  # Move 2 units per frame

# Main loop
running = True
clock = pygame.time.Clock()
camera_angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(WHITE)

    # Move the camera in the x-direction (before applying rotation)
    camera.position[0] += 1

    # Rotate the camera
    camera.rotation += 1
    camera_angle = radians(camera.rotation)

    # Render circles, applying the camera's rotation
    for circle in circles:
        # Get position relative to camera's center
        x, y = circle["position"]

        # Translate back to screen coordinates
        offset_x = camera.position[0] - x + (x - camera.position[0])*cos(camera_angle) - (y - camera.position[1])*sin(camera_angle)
        offset_y = camera.position[1] - y + (x - camera.position[0])*sin(camera_angle) + (y - camera.position[1])*cos(camera_angle)

        # Draw the rotated circle
        pygame.draw.circle(screen, RED, (x + offset_x, y + offset_y), circle["radius"])

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
