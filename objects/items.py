import pygame

class Item():
    def __init__(self, icon=None):
        self.inventory_icon = pygame.image.load('default_item_icon.png').convert_alpha()
