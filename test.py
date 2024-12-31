import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))

# Define rectangle parameters
rect_color = (255, 0, 0)  # Red color (RGB)
rect_position = (400, 300)  # Position of the center of the rectangle (x, y)
rect_size = (200, 100)  # Width and height of the rectangle (width, height)
rotation_angle = 45  # Rotation angle in degrees
rect_width = 5  # Width of the rectangle outline

# Create a surface for the rectangle
rect_surface = pygame.Surface(rect_size, pygame.SRCALPHA)  # SRCALPHA to support transparency
rect_surface.fill((0, 0, 0, 0))  # Transparent background

# Main game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear the screen with white

    # Rotate the rectangle surface
    rotated_surface = pygame.transform.rotate(rect_surface, rotation_angle)

    # Get the new rectangle's position to keep the center of rotation in the same place
    rotated_rect = rotated_surface.get_rect(center=rect_position)

    # Draw the non-filled rectangle by drawing a line around the rotated surface's edges
    pygame.draw.rect(screen, rect_color, rotated_rect, rect_width)

    # Update the display
    pygame.display.flip()

    # Check for events to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()