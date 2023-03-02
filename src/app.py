import pygame
import random

class App:
    def __init__(self) -> None:
        self.width = 640
        self.height = 400
        self.mouse_pos = (0, 0)

    def on_execute(self):
        self.on_init()

        circle_center = [self.width / 2, self.height / 2]
        circle_radius = 50
        clock = pygame.time.Clock()

        # Gameloop
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            if self.mouse_pos[0] >= (circle_center[0] - circle_radius) and \
                self.mouse_pos[0] <= (circle_center[0] + circle_radius) and \
                self.mouse_pos[1] >= (circle_center[1] - circle_radius) and \
                self.mouse_pos[1] <= (circle_center[1] + circle_radius):
                circle_radius = random.randint(30, 80)
                circle_center = [random.randint(circle_radius, self.width - circle_radius), random.randint(circle_radius, self.height - circle_radius)]

            self.window.fill((0, 0, 0))
            pygame.draw.circle(self.window, (69,122,83), circle_center, circle_radius)
            pygame.display.update()
            clock.tick(60)

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.K_ESCAPE or event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos

    def on_init(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        self.running = True
