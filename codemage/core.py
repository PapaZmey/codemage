import time
import pygame
import sys

from codemage import config
from codemage.entity import Player
from codemage.ui import Button, Label, UIManager, Window


# Main game class
class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(config.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Game objects
        self.entities = []
        self.player = Player(400, 300)
        self.entities.append(self.player)

        # UI setup
        self.ui_manager = UIManager()
        self.setup_ui()

        # Input handling - store key binding functions
        self.key_bindings = {
            pygame.K_i: lambda: self.toggle_window("inventory"),
            pygame.K_c: lambda: self.toggle_window("character"),
            pygame.K_m: lambda: self.toggle_window("map"),
            pygame.K_o: lambda: self.toggle_window("options"),
        }

    def toggle_window(self, window_name):
        window = self.windows.get(window_name)
        if window:
            window.toggle()
            if window.visible:
                self.ui_manager.bring_window_to_front(window)

    def setup_ui(self):
        # Store references to windows for easy access
        self.windows = {}

        # Create inventory window
        inventory_window = Window(50, 50, 300, 400, "Inventory", draggable=True)

        # Example items
        for i in range(5):
            item_btn = Button(
                20,
                40 + i * 40,
                260,
                30,
                f"Item {i + 1}",
                lambda i=i: print(f"Used item {i+1}"),
            )
            inventory_window.add_child(item_btn)

        self.ui_manager.add_window(inventory_window)
        self.windows["inventory"] = inventory_window

        # Create character window
        character_window = Window(400, 50, 300, 400, "Character", draggable=True)
        character_window.add_child(Label(20, 40, "Health: 100/100"))
        character_window.add_child(Label(20, 70, "Strength: 15"))
        character_window.add_child(Label(20, 100, "Agility: 12"))
        character_window.add_child(Label(20, 130, "Intelligence: 10"))
        self.ui_manager.add_window(character_window)
        self.windows["character"] = character_window

        # Create map window
        map_window = Window(150, 100, 400, 300, "Map", draggable=True)
        map_window.add_child(Label(150, 140, "Map goes here"))
        self.ui_manager.add_window(map_window)
        self.windows["map"] = map_window

        # Create options window
        options_window = Window(200, 150, 350, 250, "Options", draggable=True)
        options_window.add_child(Label(20, 40, "Game Settings"))
        options_window.add_child(
            Button(20, 70, 120, 30, "Sound: On", lambda: print("Toggle sound"))
        )
        options_window.add_child(
            Button(20, 110, 120, 30, "Music: On", lambda: print("Toggle music"))
        )
        options_window.add_child(
            Button(20, 150, 120, 30, "Fullscreen", lambda: print("Toggle fullscreen"))
        )
        self.ui_manager.add_window(options_window)
        self.windows["options"] = options_window

        for window in self.windows.values():
            window.visible = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # handle window toggle hotkeys
                elif event.key in self.key_bindings:
                    self.key_bindings[event.key]()

            # Try to handle the event with the UI system first
            if not self.ui_manager.handle_event(event):
                # If UI didn't handle it, the event might be relevant for gameplay
                self.handle_gameplay_event(event)

    def handle_gameplay_event(self, event):
        # Handle events specifically for gameplay (not UI)
        # For example, mouse clicks on entities, etc.
        pass

    def update(self, dt):
        # update game entities
        for entity in self.entities:
            entity.update(dt)

        # update UI
        self.ui_manager.update(dt)

        # Update DYNAMIC UI elements
        char_window = self.windows.get("character")
        if char_window and char_window.visible:
            # update player stats in char. window
            for child in char_window.children:
                if isinstance(child, Label) and child.text.startswith("Health"):
                    child.set_text(f"Health: {self.player.hp}/{self.player.max_hp}")

    def render(self):
        # Clear screen
        self.screen.fill(config.UI_BG_COLOR)

        # Dram game entities
        for entity in self.entities:
            entity.draw(self.screen)

        # Draw UI on top
        self.ui_manager.draw(self.screen)

        # Update display
        pygame.display.flip()

    def run(self):
        previous_time = time.time()

        while self.running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - previous_time
            previous_time = current_time

            # process input
            self.handle_events()

            # update game state
            self.update(dt)

            # render
            self.render()

            # Cap the frame rate
            self.clock.tick(config.FPS)

        pygame.quit()
        sys.exit()
