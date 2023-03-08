from pygame.sprite import Sprite, Group
from pygame import image
from pygame import Rect, Surface, Vector2
import pygame
import os
import random

class Platform(Sprite):
    def __init__(self, window, image: Surface, pos: Vector2, *groups: Group) -> None:
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.window = window
        self.pos = pos

    def update(self):
        self.window.blit(self.image, self.pos)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update_y_position(self, y_velocity):
        self.pos.y += y_velocity
    
class Platforms(Group):
    NUMBER_OF_PLATFORMS = 8

    def __init__(self, window: Surface) -> None:
        super().__init__(self)
        self.terrain_and_props = image.load(os.path.join("assets","Fantasy Swamp Forest","Free","Terrain_and_Props.png"))
        self.platforms_sprite_rects = [
            Rect(90, 14, 65, 16)
        ]
        self.window = window
        self.last_pos = Vector2(0, 0)
        self.initial_platforms()

    def initial_platforms(self):
        window_width = self.window.get_width()
        window_height = self.window.get_height()
        initial_positions = [
            Vector2(window_width / 2 - 50, window_height * 0.85),
            Vector2(window_width * 0.4, window_height * 0.75),
            Vector2(window_width * 0.7, window_height * 0.7),
        ]

        for pos in initial_positions:
            image = self.random_image()
            platform = Platform(self.window, image, pos, self)
            self.last_pos = Vector2(int(pos.x), int(pos.y))
            self.add(platform)

    def random_image(self):
        random_number = random.randint(0, len(self.platforms_sprite_rects) - 1)
        random_rect = self.platforms_sprite_rects[random_number]
        image = self.terrain_and_props.subsurface(random_rect)
        image = pygame.transform.scale2x(image)
        return image

    def update(self):
        window_width = self.window.get_width()
        while len(self.sprites()) < Platforms.NUMBER_OF_PLATFORMS:
            image = self.random_image()
            width = random.randint(50, 100)
            image = pygame.transform.scale(image, (width, image.get_height()))

            rand_x = random.randint(int(self.last_pos.x - window_width / 3), int(self.last_pos.x + window_width / 3))
            rand_x = int(max(width, min(rand_x, window_width - width)))
            rand_y = int(random.randint(int(self.last_pos.y) - 120, int(self.last_pos.y) - 100))

            pos = Vector2(rand_x, rand_y)
            platform = Platform(self.window, image, pos, self)
            self.last_pos = pos
            self.add(platform)

        for sprite in self.sprites():
            sprite.update()

    def update_y_position(self, y_velocity):
        for sprite in self.sprites():
            sprite.update_y_position(y_velocity)
            if sprite.rect.top > self.window.get_height():
                sprite.kill()
