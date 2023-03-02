import pygame

class App:
    def __init__(self) -> None:
        self.width = 640
        self.height = 400

    def on_execute(self):
        self.on_init()

        # Gameloop
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.K_ESCAPE or event.type == pygame.QUIT:
            self.running = False

    def on_init(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        self.running = True
