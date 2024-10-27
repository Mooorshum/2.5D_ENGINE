from math import sqrt, sin, cos, atan2, pi, degrees
import random

import os

import pygame


from graphics.particles import ParticleSystem


class BasicCharacter:
    def __init__(self, character_folder=None):
        self.character_folder = character_folder
        self.name = 'character'
        self.health = 100
        self.dt = 0.1

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
            # 'jumping',
        ]
        

        self.current_state = 'idle'
        self.idle_state = 'idle'
        self.idle_animation_speed = 3
        self.current_frame_number = 0

        self.x = 300
        self.y = 300

        self.movespeed = 10
        self.speed_limit = 40
        
        self.shake = 2

        self.jumping = False
        self.vertical_offset = 0
        

        self.slice_images_folder = 'assets/3d_models/hippie_bus/'
        self.slice_images = [
            pygame.image.load(
                    self.slice_images_folder + img
                ) for img in sorted(os.listdir(self.slice_images_folder), key=lambda x: int(os.path.splitext(x)[0]))
            ]







        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = 0

        self.drag = 0.02
        self.gravity = 0

        self.current_image = None
        self.state_images, self.state_num_frames = self.get_images()


        self.dust = ParticleSystem()
        DUST_BROWN_1 = (184, 160, 133)
        DUST_BROWN_2 = (181, 153, 140)
        DUST_BROWN_3 = (181, 153, 140)
        DUST_BROWN_4 = (199, 186, 151)

        self.dust.colours = (
            DUST_BROWN_1, DUST_BROWN_2, DUST_BROWN_3, DUST_BROWN_4,
        )
        
        self.dust.lifetime_range = (10, 100)
        self.dust.acceleration_range = (10, 50)
        self.dust.ay_system = -30
        self.max_dustcloud_size = 20
        self.dust_particles_max_count = 50


    def get_images(self):
        state_images = {}
        state_num_frames = {}
        for state in self.states:
            images = []
            num_frames = len(os.listdir(f'{self.character_folder}/state_images/{state}/frames/'))
            for i in range(num_frames):
                images.append(pygame.image.load(f'{self.character_folder}/state_images/{state}/frames/frame_{i}.png').convert_alpha())
            state_images.update({state: images}) 
            state_num_frames.update({state: num_frames}) 
        return state_images, state_num_frames


    def handle_movement(self, keys):
        if keys[pygame.K_SPACE]:
            self.jump()

        self.handle_state() # change the state of the object based on the direction it is moving

        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]
        move_up = keys[pygame.K_UP]
        move_down = keys[pygame.K_DOWN]

        ax, ay = 0, 0
        if move_left:
            ax = -self.movespeed
        if move_right:
            ax = self.movespeed
        if move_up:
            ay = -self.movespeed
        if move_down:
            ay = self.movespeed
        
        # limiting the object's speed
        if sqrt(self.vx**2 + self.vy**2) > self.speed_limit:
            ax = 0
            ay = 0

        vx_new = self.vx + ax * self.dt - self.vx*self.drag
        vy_new = self.vy + ay * self.dt - self.vy*self.drag


        self.vx, self.vy = vx_new, vy_new

        new_x = self.x + self.vx * self.dt
        new_y = self.y + self.vy * self.dt

        self.x = new_x
        self.y = new_y


    def handle_state(self):

        if sqrt(self.vx**2 + self.vy**2) < self.idle_animation_speed:
            self.current_state = self.idle_state
            return

        movement_angle = atan2(self.vx, -self.vy)

        if -pi/8 <= movement_angle < pi/8:
            self.current_state = 'moving_up'
        elif pi/8 <= movement_angle < 3*pi/8:
            self.current_state = 'moving_up_right'
        elif 3*pi/8 <= movement_angle < 5*pi/8:
            self.current_state = 'moving_right'
        elif 5*pi/8 <= movement_angle < 7*pi/8:
            self.current_state = 'moving_down_right'
        elif -7*pi/8 <= movement_angle < -5*pi/8:
            self.current_state = 'moving_down_left'
        elif -5*pi/8 <= movement_angle < -3*pi/8:
            self.current_state = 'moving_left'
        elif -3*pi/8 <= movement_angle < -pi/8:
            self.current_state = 'moving_up_left'
        elif 7*pi/8 <= movement_angle <= 9*pi/8:
            self.current_state = 'moving_down'

        self.idle_state = self.current_state

    def jump(self):
        pass


    def draw(self, screen):
        num_frames = self.state_num_frames[self.current_state]
        # looping frames for current state
        if self.current_frame_number < num_frames-1:
            self.current_frame_number += 1
        else:
            self.current_frame_number = 0
        image = self.state_images[self.current_state][self.current_frame_number]
        centered_image_position_x = self.x - image.get_width()//2
        centered_image_position_y = self.y - image.get_height() - self.vertical_offset

        # Creating dust particles
        self.dust.x = centered_image_position_x + image.get_width()//2
        self.dust.y = centered_image_position_y + image.get_height()*7//10
        factor = sqrt(self.vx**2 + self.vy**2)/self.speed_limit
        self.dust.r_range = (0, round(self.max_dustcloud_size*factor))
        self.dust.max_count = self.dust_particles_max_count * factor
        self.dust.create_particle()
        self.dust.update_particles()
        self.dust.draw_particles(screen)
        
        screen.blit(
            image,
            (
                centered_image_position_x + random.randint(0, round(self.shake * factor**8)),
                centered_image_position_y + random.randint(0, round(self.shake * factor**8))
            )
        )






    def render_stack(self, screen, spread=2, scale=1):

        self.dust.x = self.x
        self.dust.y = self.y
        factor = sqrt(self.vx**2 + self.vy**2)/self.speed_limit
        self.dust.r_range = (0, round(self.max_dustcloud_size*factor))
        self.dust.max_count = self.dust_particles_max_count * factor
        self.dust.create_particle()
        self.dust.update_particles()
        self.dust.draw_particles(screen)

        rotation = degrees(-atan2(self.vy, self.vx))
        for i, img in enumerate(self.slice_images):
            if scale != 1:
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            rotated_img = pygame.transform.rotate(img, rotation)
            screen.blit(
                rotated_img,
                (self.x - rotated_img.get_width() // 2, self.y - rotated_img.get_height() // 2 - i * spread * scale)
            )





