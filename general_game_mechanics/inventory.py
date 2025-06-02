import pygame

class GridInventory:
    def __init__(self, size=(256, 256), grid_size=(1, 1), items=None):
        self.size = size
        self.grid_size = grid_size
        self.items = items if items else []

        # Calculating size of each cell
        self.cell_width = self.size[0] / self.grid_size[0]
        self.cell_height = self.size[1] / self.grid_size[1]

        # Calculating item grid positions - from right to left, top to bottom, xy coordinates are the same as in pygame
        self.item_grid_position = {}
        x_grid = -self.size[0]/2 + self.cell_width / 2
        y_grid = self.size[1]/2 - self.cell_height / 2
        for item in self.items:
            if x_grid > self.size[0]/2 - self.cell_width / 2:
                x_grid = -self.size[0]/2 + self.cell_width / 2
            self.item_grid_position[item] = (x_grid, y_grid)
            x_grid += self.cell_width
            y_grid -= self.cell_height


    def render(self, screen, position):

        # Drawing inventory bounding box
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                [position[0] - self.size[0]/2, position[1] - self.size[1]/2], 
                self.size
            ),
            width=1,
        )

        # Rendering items
        for item in self.items:
            grid_pos = self.item_grid_position[item]

            cell_centre_screen = (
                position[0] + grid_pos[0],
                position[1] + grid_pos[1]
            )

            # Item bounding box
            pygame.draw.rect(
                screen,
                (0, 255, 255),
                (
                    [cell_centre_screen[0] - self.cell_width/2, cell_centre_screen[1] - self.cell_width/2], 
                    [self.cell_width, self.cell_height]
                ),
                width=1,
            )

            """ # Drawing item icon centered in the cell
            if hasattr(item, 'inventory_icon'):
                icon = pygame.transform.scale(item.inventory_icon, (int(self.cell_width), int(self.cell_height)))
                icon_rect = icon.get_rect(center=item_rect.center)
                screen.blit(icon, icon_rect) """
