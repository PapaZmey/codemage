# Base class for the UI elements
class UIElement:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.parent = None

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_absolute_position(self):
        # Calculate position considering parent windows (if any)
        if self.parent:
            parent_x, parent_y = self.parent.get_absolute_position()
            return parent_x + self.x, parent_y + self.y
        return self.x, self.y

    def contains_point(self, point):
        abs_x, abs_y = self.get_absolute_position()
        return (
            abs_x <= point[0] <= abs_x + self.width
            and abs_y <= point[1] <= abs_y + self.height
        )

    def update(self, dt):
        pass

    def handle_event(self, event):
        return False  # Return true if event is handled

    def draw(self, screen):
        pass
