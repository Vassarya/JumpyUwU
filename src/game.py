import pygame
import random
from character import Character
from platforms import Platforms
import os


class Game:
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (172, 246, 200)
    COLOR_BLACK = (0, 0, 0)

    def __init__(self) -> None:
        self.width = 600
        self.height = 720
        self.window = None
        self.exit = False
        self.game_over = False
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.key_pressed = False
        self.font_path = os.path.join("assets", "Font", "Planes_ValMore.ttf")
        self.bg_image = self.load_background()
        self.score = 0

    def start(self):
        self.on_init()
        while not self.exit:
            self.start_screen()
            self.run()
            if self.game_over:
                self.game_over_screen()

    def load_background(self):
        bg_image = pygame.image.load(os.path.join("assets", "background", "sun.png"))
        bg_image = pygame.transform.scale(bg_image, (self.width, self.height))
        return bg_image

    def run(self):
        self.game_over = False
        self.score = 0
        character = Character(self.window)
        platforms = Platforms(self.window)

        # Gameloop
        while not self.exit and not self.game_over:
            for event in pygame.event.get():
                self.on_event(event)
                character.on_event(event)

            if character.get_pos().y > self.window.get_height():
                self.game_over = True

            self.window.fill((0, 0, 0))
            self.window.blit(self.bg_image, self.bg_image.get_rect())

            if character.get_pos().y < self.window.get_height() * 0.75:
                velocity = character.get_velocity()
                if velocity.y < 0:
                    killed_platforms = platforms.update_y_position(-velocity.y)
                    self.score += (killed_platforms * 10)
                    character.set_half_speed(True)
                else:
                    character.set_half_speed(False)
            else:
                character.set_half_speed(False)


            character.update()
            platforms.update()

            collided_sprites = pygame.sprite.spritecollide(character, platforms, False)
            if character.is_falling():
                if len(collided_sprites) > 0:
                    lowest_sprite = collided_sprites[0]
                    for sprite in collided_sprites:
                        if sprite.rect.bottom > lowest_sprite.rect.bottom:
                            lowest_sprite = sprite
                    if character.rect.bottom - 10 < lowest_sprite.rect.top:
                        character.reset_jumping()
            elif len(collided_sprites) == 0 and not character.is_jumping():
                character.set_falling()

            self.show_text(f"Score: {self.score: <8}", 36, (0, 0, 0), pygame.Vector2(150, 20))

            pygame.display.update()
            self.clock.tick(self.fps)

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.exit = True
        elif event.type == pygame.KEYDOWN:
            self.key_pressed = True

    def on_init(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("assets", "music", "xDeviruchi - Exploring The Unknown.wav"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("JumpyUwU")
        self.exit = False

    def start_screen(self):
        self.window.fill(Game.COLOR_GREEN)
        self.show_text("JumpyUwU", 40, Game.COLOR_BLACK, pygame.Vector2(self.width / 2, self.height / 2))
        self.show_text("by Katharina Boegeholz @ 2023", 20, Game.COLOR_BLACK,
                       pygame.Vector2(self.width / 2, self.height / 2 + 40))
        pygame.display.update()
        self.key_pressed = False
        while not self.key_pressed and not self.exit:
            for event in pygame.event.get():
                self.on_event(event)

    def game_over_screen(self):
        self.window.fill(Game.COLOR_RED)
        self.show_text("Game Over", 40, Game.COLOR_BLACK, pygame.Vector2(self.width / 2, self.height / 2))
        self.show_text(f"Your Score {self.score}", 30, Game.COLOR_BLACK, pygame.Vector2(self.width / 2,
                                                                                        self.height / 2 + 60))
        pygame.display.update()
        self.key_pressed = False
        while not self.key_pressed and not self.exit:
            for event in pygame.event.get():
                self.on_event(event)

    def show_text(self, text, size, color, pos: pygame.Vector2):
        font = pygame.font.Font(self.font_path, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (pos.x, pos.y)
        self.window.blit(text_surface, text_rect)
