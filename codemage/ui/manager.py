import pygame


class UIManager:
    def __init__(self):

        self.windows = []
        self.active_window = None
        self.next_z_index = 0

    def add_window(self, window):
        window.z_index = self.next_z_index
        self.next_z_index += 1
        self.windows.append(window)

    def remove_window(self, window):
        if window in self.windows:
            self.windows.remove(window)

    def bring_window_to_front(self, window):
        if window in self.windows:
            self.windows.remove(window)
            window.z_index = self.next_z_index
            self.next_z_index += 1
            self.windows.append(window)
            self.active_window = window

    def handle_event(self, event):
        # Special handling for kb events - the don't involve window pos.
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            # Let active window handle KB events if it exits
            if self.active_window and self.active_window.visible:
                return self.active_window.handle_event(event)
            return False

        # For mouse events, process window in reverse order (front to back)
        if hasattr(event, "pos"):  # check if it's a mouse event
            for window in reversed(self.windows):
                if window.handle_event(event):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.bring_window_to_front(window)
                    return True
        return False

    def update(self, dt):
        for window in self.windows:
            window.update(dt)

    def draw(self, screen):
        # Sort windows by Z-index before drawing
        sorted_windows = sorted(self.windows, key=lambda w: w.z_index)

        for window in sorted_windows:
            window.draw(screen)
