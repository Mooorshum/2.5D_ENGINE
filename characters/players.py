from math import sqrt

import os

import pygame


class BasicCharacter:
    def __init__(self, character_folder=None):
        self.character_folder = character_folder
        self.name = 'character'
        self.health = 100

        self.states = [
            'idle',
            'moving_up',
            'moving_down',
            'moving_left',
            'moving_right',
            'moving_up_left',
            'moving_up_right',
            'moving_down_left',
            'moving_down_right',
            'jumping',
        ]

        self.current_state = 'idle'
        self.state_animation_frame_number = 0

        self.x = 0
        self.y = 0

        self.movespeed = 10

        self.jumping = False
        self.vertical_offset = 0

        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = 0

        self.drag = 0
        self.gravity = 0

        self.current_image = None
        self.state_images = self.get_character_images()


    def get_images(self):
        state_images = {}
        for state in self.states:
            images = []
            num_images = len(os.listdir(f'{self.character_folder}/state_images/{state}/'))
            for i in range(num_images):
                images.append(pygame.image.load(f'{self.character_folder}/state_images/{state}/frames/frame_{i}.png').convert_alpha())
            state_images.update({state: [images, num_images]}) 
        return state_images


    def handle_movement(self, keys):
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]
        move_up = keys[pygame.K_UP]
        move_down = keys[pygame.K_DOWN]

        vx, vy = 0, 0

        if move_left:
            vx = -self.movespeed
        if move_right:
            vx = self.movespeed

        if move_up:
            vy = -self.movespeed
        if move_down:
            vy = self.movespeed

        if vx != 0 and vy != 0:
            factor = sqrt(2) / 2
            vx *= factor
            vy *= factor

        self.player.vx = vx
        self.player.vy = vy

        if keys[pygame.K_SPACE]:
            self.player.jump()


    def handle_state(self):
        pass


    def jump(self):
        pass


    def draw(self, screen):
        num_frames = self.state_images[self.current_state][1]
        frame_number = self.state_animation_frame_number
        image = self.state_images[self.current_state][0][frame_number]
        screen.blit(image, self.x + image.get_width()//2, self.y - image.get_height() - self.vertical_offset)
        if frame_number < num_frames:
            self.state_animation_frame_number += 1
        else:
            self.state_animation_frame_number = 0
