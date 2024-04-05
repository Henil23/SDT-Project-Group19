import pygame as pg  # Import the pygame library
import sys  # Import the sys module for system-related functions
from GameSetting import *  # Import settings for the game
from GameMap import *  # Import the GameMap module
from GamePlayer import *  # Import the GamePlayer module
from raycaste import *  # Import the raycaste module
from RenderObject import *  # Import the RenderObject module
from light_object import *  # Import the light_object module
from ObjectController import *  # Import the ObjectController module
from weapons import *  # Import the weapons module
from GameSounds import *  # Import the GameSounds module
from PathFinder import *  # Import the PathFinder module


class Game:
    def __init__(self):
        # Initialize the game
        pg.init()  # Initialize pygame
        pg.mouse.set_visible(False)  # Hide the mouse cursor
        self.screen = pg.display.set_mode(SCREEN_RES)  # Set the screen resolution
        pg.event.set_grab(True)  # Grab the mouse input
        self.clock = pg.time.Clock()  # Create a clock object to control the frame rate
        self.delta_time = 1  # Initialize delta time
        self.global_trigger = False  # Initialize global trigger flag
        self.global_event = pg.USEREVENT + 0  # Define a custom event
        pg.time.set_timer(self.global_event, 40)  # Set a timer for the custom event
        self.new_game()  # Start a new game

    def new_game(self):
        # Start a new game
        self.map = Map(self)  # Create a new map object
        self.player = Player(self)  # Create a new player object
        self.object_renderer = ObjectRenderer(self)  # Create an object renderer
        self.raycasting = RayCastingEngine(self)  # Create a raycasting engine
        self.object_handler = ObjectHandler(self)  # Create an object handler
        self.weapon = Weapon(self)  # Create a weapon object
        self.sound = Sound(self)  # Create a sound object
        self.pathfinding = PathFinding(self)  # Create a pathfinding object
        pg.mixer.music.play(-1)  # Start playing background music

    def update(self):
        # Update game state
        self.player.Update()  # Update player state
        self.raycasting.update()  # Update raycasting engine
        self.object_handler.update()  # Update object handler
        self.weapon.update()  # Update weapon state
        pg.display.flip()  # Update the display
        self.delta_time = self.clock.tick(FPS)  # Update delta time
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  # Update window title with FPS

    def draw(self):
        # Draw game elements
        self.object_renderer.draw()  # Draw objects
        self.weapon.draw()  # Draw weapon

    def check_events(self):
        # Check for and handle events
        self.global_trigger = False  # Reset global trigger flag
        for event in pg.event.get():  # Iterate over all events
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()  # Quit pygame
                sys.exit()  # Exit the program
            elif event.type == self.global_event:  # Check for custom event
                self.global_trigger = True  # Set global trigger flag
            self.player.single_fire_event(event)  # Handle single fire event

    def run(self):
        # Main game loop
        while True:
            self.check_events()  # Check for events
            self.update()  # Update game state
            self.draw()  # Draw game elements


if __name__ == '__main__':
    # Create and run the game
    game = Game()  # Create a new game object
    game.run()  # Run the game loop
