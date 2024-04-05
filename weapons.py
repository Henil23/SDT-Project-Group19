from light_object import *  # Importing from light_object module
from GameSetting import *  # Importing constants from GameSetting module

class Weapon(AnimatedLight):
    def __init__(self, game_instance, image_path='weapon/shotgun/0.png', scale=0.4, animation_duration=90):
        super().__init__(game_instance, image_path, animation_time=animation_duration)  # Initialize AnimatedLight superclass
        # Scale weapon images
        self.images = deque(
            [pg.transform.smoothscale(image, (self.image.get_width() * scale, self.image.get_height() * scale))
             for image in self.images])
        # Set initial weapon position
        self.weapon_position = (HALF_SCREEN_WIDTH - self.images[0].get_width() // 2, SCREEN_HEIGHT - self.images[0].get_height())
        self.reloading = False  # Initialize reloading status
        self.num_images = len(self.images)  # Get number of weapon images
        self.frame_counter = 0  # Initialize frame counter
        self.damage = 50  # Set weapon damage

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)  # Rotate weapon images
                self.image = self.images[0]  # Set current weapon image
                self.frame_counter += 1  # Increment frame counter
                if self.frame_counter == self.num_images:
                    self.reloading = False  # Stop reloading animation
                    self.frame_counter = 0  # Reset frame counter

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_position)  # Draw current weapon image

    def update(self):
        self.check_animation_time()  # Check animation time
        self.animate_shot()  # Animate weapon shot
