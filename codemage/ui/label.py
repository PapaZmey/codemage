import pygame

from codemage import config
from codemage.ui import UIElement


class Label(UIElement):
    def __init__(self, x, y, text, font_size=24, color=None):
        self.font = pygame.font.Font(config.UI_FONT, font_size)
        text_surface = self.font.render(text, True, (0, 0, 0))
        width, height = text_surface.get_size()
        super().__init__(x, y, width, height)
        self.text = text
        self.color = color or config.UI_TEXT_COLOR

    def set_text(self, text):
        self.text = text
        text_surface = self.font.render(text, True, (0, 0, 0))
        self.width, self.height = text_surface.get_size()

    def draw(self, screen):
        if not self.visible:
            return

        abs_x, abs_y = self.get_absolute_position()
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (abs_x, abs_y))
