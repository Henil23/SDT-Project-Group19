import pygame as pg  # Importing pygame library as pg
from GameSetting import *  # Importing constants from GameSetting module

class ObjectRenderer:
    def __init__(self, game):
        self.game = game  # Reference to the game instance
        self.screen = game.screen  # Reference to the game screen
        self.wall_textures = self.load_wall_textures()  # Load wall textures
        self.sky_image = self.get_texture('textures/sky.png', (SCREEN_WIDTH, HALF_SCREEN_HEIGHT))  # Load sky image
        self.sky_offset = 0  # Initialize sky offset
        self.blood_screen = self.get_texture('textures/blood_screen.png', SCREEN_RES)  # Load blood screen texture
        self.digit_size = 90  # Initialize digit size
        self.digit_images = [self.get_texture(f'textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]  # Load digit images
        self.digits = dict(zip(map(str, range(11)), self.digit_images))  # Create dictionary for digit images
        self.game_over_image = self.get_texture('textures/game_over.png', SCREEN_RES)  # Load game over image
        self.win_image = self.get_texture('textures/win.png', SCREEN_RES)  # Load win image

    def draw(self):
        self.draw_background()  # Draw background
        self.render_game_objects()  # Render game objects
        self.draw_player_health()  # Draw player health

    def win(self):
        self.screen.blit(self.win_image, (0, 0))  # Display win image

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))  # Display game over image

    def draw_player_health(self):
        health = str(self.game.player.health)  # Get player health as string
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))  # Draw digits for player health
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))  # Draw full heart for player health

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))  # Display blood screen texture

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % SCREEN_WIDTH  # Update sky offset
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))  # Display sky image
        self.screen.blit(self.sky_image, (-self.sky_offset + SCREEN_WIDTH, 0))  # Display sky image (repeated)
        # Draw floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)  # Render game objects

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()  # Load texture with transparency
        return pg.transform.scale(texture, res)  # Scale texture to specified resolution

    def load_wall_textures(self):
        return {
            1: self.get_texture('textures/1.png'),  # Load wall texture 1
            2: self.get_texture('textures/2.png'),  # Load wall texture 2
            3: self.get_texture('textures/3.png'),  # Load wall texture 3
            4: self.get_texture('textures/4.png'),  # Load wall texture 4
            5: self.get_texture('textures/5.png'),  # Load wall texture 5
        }
