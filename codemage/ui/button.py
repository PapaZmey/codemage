import pygame

from codemage import config
from codemage.ui import UIElement


class Button(UIElement):
    def __init__(self, x, y, width, height, text, callback=None):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.font = pygame.font.Font(config.UI_FONT, config.UI_FONT_SIZE)

    def handle_event(self, event):
        if not self.visible:
            return False

        # Only handle MOUSE events!
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.contains_point(event.pos)
            return self.hovered

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.callback:
                self.callback()
                return True

        return False

    def draw(self, screen):
        if not self.visible:
            return

        abs_x, abs_y = self.get_absolute_position()
        color = config.UI_BUTTON_HOVER_COLOR if self.hovered else config.UI_BUTTON_COLOR

        # Draw button background
        pygame.draw.rect(screen, color, (abs_x, abs_y, self.width, self.height))
        pygame.draw.rect(
            screen, config.UI_BORDER_COLOR, (abs_x, abs_y, self.width, self.height), 1
        )

        # Draw button text
        text_surface = self.font.render(self.text, True, config.UI_TEXT_COLOR)
        text_rect = text_surface.get_rect(
            center=(abs_x + self.width / 2, abs_y + self.height / 2)
        )
        screen.blit(text_surface, text_rect)
