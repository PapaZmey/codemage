import pygame

from codemage import config
from codemage.entity import Entity


class Player(Entity):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 50
        self.height = 50
        self.speed = 200
        # TODO: CHANGE LATER
        self.hp = 100
        self.max_hp = 100
        self.score = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.x += self.speed * dt
        if keys[pygame.K_UP]:
            self.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.y += self.speed * dt

        # Keep player within borders
        self.x = max(0, min(config.SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(config.SCREEN_HEIGHT - self.height, self.y))

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (0, 0, 255),
            (
                self.x - self.width / 2,
                self.y - self.height / 2,
                self.width,
                self.height,
            ),
        )
