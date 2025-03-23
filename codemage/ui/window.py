import pygame

from codemage import config
from codemage.ui import UIElement, Button


class Window(UIElement):
    def __init__(
        self, x, y, width, height, title="Window", draggable=True, closable=True
    ):
        super().__init__(x, y, width, height)
        self.title = title
        self.draggable = draggable
        self.closable = closable
        self.dragging = False
        self.drag_offset = (0, 0)
        self.children = []
        self.font = pygame.font.Font(config.UI_FONT, config.UI_FONT_SIZE)
        self.header_height = 30
        self.z_index = 0  # For determining draw order

        # Add close button if window is closable
        if self.closable:
            close_btn = Button(width - 25, 5, 20, 20, "X", self.close)
            self.add_child(close_btn)

    def close(self):
        self.visible = False

    def show(self):
        self.visible = True

    def toggle(self):
        self.visible = not self.visible

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def bring_to_front(self):
        # This will be used by the UI Manager to change z-index
        pass

    def handle_event(self, event):
        if not self.visible:
            return False

        # handle events for child elements first (in reverse, to respect z-index)
        for child in reversed(self.children):
            if child.handle_event(event):
                return True

        # Only process mouse-related events for window dragging and activation
        if hasattr(event, "pos"):
            # handle dragging
            if self.draggable:
                header_rect = pygame.Rect(
                    self.x, self.y, self.width, self.header_height
                )

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if header_rect.collidepoint(event.pos[0], event.pos[1]):
                        self.dragging = True
                        self.drag_offset = (
                            event.pos[0] - self.x,
                            event.pos[1] - self.y,
                        )
                        return True
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.dragging:
                        self.dragging = False
                        return True
                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    self.x = event.pos[0] - self.drag_offset[0]
                    self.y = event.pos[1] - self.drag_offset[1]

                    # Keep window within screen bounds
                    self.x = max(0, min(self.x, config.SCREEN_WIDTH - self.width))
                    self.y = max(0, min(self.y, config.SCREEN_HEIGHT - self.height))
                    return True

            # Return true if mouse is over window (for clicking to bring to front)
            if event.type in (
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEMOTION,
            ):
                return self.contains_point(event.pos)
        return False  # Event not handled

    def update(self, dt):
        if not self.visible:
            return

        for child in self.children:
            child.update(dt)

    def draw(self, screen):
        if not self.visible:
            return

        # Draw window bg
        pygame.draw.rect(
            screen, config.UI_BG_COLOR, (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            screen,
            config.UI_BORDER_COLOR,
            (self.x, self.y, self.width, self.height),
            2,
        )

        # Draw header
        pygame.draw.rect(
            screen,
            config.UI_HIGHLIGHT_COLOR,
            (self.x, self.y, self.width, self.header_height),
        )

        # Draw title
        title_surface = self.font.render(self.title, True, config.UI_TEXT_COLOR)
        title_rect = title_surface.get_rect(
            midleft=(self.x + 10, self.y + self.header_height / 2)
        )
        screen.blit(title_surface, title_rect)

        # Draw children
        for child in self.children:
            child.draw(screen)
