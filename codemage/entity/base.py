# Game entity base class
class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def collides_with(self, other):
        return (
            abs(self.x - other.x) < (self.width + other.width) / 2
            and abs(self.y - other.y) < (self.height + other.height) / 2
        )

    def on_collision(self, other):
        pass
