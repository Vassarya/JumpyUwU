import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
import os

class Character(Sprite):
    VELOCITY = 5

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.idle_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets","character","2 Owlet_Monster","Owlet_Monster.png")))
        self.running_images = self.load_running_images()
        self.next_running_image_index = 0
        self.pos = Vector2(self.window.get_width() / 2, self.window.get_height() * 0.76)
        self.velocity = Vector2(0, 0)
        self.jumping = False
        self.movement_pressed = False
        self.acceleration = Vector2(0, 0.1)

    def load_running_images(self):
        spritesheet = pygame.image.load(os.path.join("assets","character","2 Owlet_Monster","Owlet_Monster_Run_6.png"))
        running_images = []
        for i in range(6):
            image = spritesheet.subsurface(i * 32, 0, 32, 32)
            image = pygame.transform.scale2x(image)
            running_images.append(image)
        return running_images

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.next_running_image_index = 0
                self.velocity.x = 1.5
                self.movement_pressed = True
            elif event.key == pygame.K_a:
                self.next_running_image_index = 0
                self.velocity.x = -1.5
                self.movement_pressed = True
            elif event.key == pygame.K_SPACE and not self.jumping:
                self.jumping = True
                self.velocity.y = -Character.VELOCITY
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.velocity.x = 0
                self.movement_pressed = False
            elif event.key == pygame.K_a:
                self.velocity.x = 0
                self.movement_pressed = False
    
    def get_pos(self):
        return self.pos

    def update(self):
        if self.jumping:
            self.jump()
        elif self.movement_pressed:
            self.move()
        else:
            self.idle()

        self.window.blit(self.image, self.pos)

    def jump(self):
        self.velocity += self.acceleration
        self.pos += self.velocity
        self.idle()

    def idle(self):
        self.set_image(self.idle_image)
        
    def move(self):
        self.pos.x += self.velocity.x

        image = self.running_images[self.next_running_image_index]
        if self.velocity.x < 0:
            image = pygame.transform.flip(image, True, False)
        self.set_image(image)       
        self.next_running_image_index = (self.next_running_image_index + 1) % len(self.running_images)

    def set_image(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def reset_jumping(self):
        self.jumping = False
        self.velocity.y = 0

    def is_falling(self):
        return self.velocity.y > 0
    
    def is_jumping(self):
        return self.velocity.y < 0
    
    def set_falling(self):
        self.jumping = True
        self.velocity.y = Character.VELOCITY

    def get_velocity(self):
        return self.velocity