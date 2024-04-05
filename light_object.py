import pygame as pg
from GameSetting import *
import os
from collections import deque


class LightObject:
    def __init__(self, game, image_path='skullCandle/candlebra.png', #changed
                 position=(10.5, 3.5), scale_factor=0.7, height_shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = position
        self.image = pg.image.load(image_path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale_factor
        self.SPRITE_HEIGHT_SHIFT = height_shift

    def light_projection(self):
        projection = SCREEN_DISTANCE / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = projection * self.IMAGE_RATIO, projection

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        position = self.screen_x - self.sprite_half_width, HALF_SCREEN_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, position))

    def GetLight(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUMBER_OF_RAYS + delta_rays) * RAYCASTING_SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (SCREEN_WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.light_projection()

    def update(self):
        self.GetLight()


class AnimatedLight(LightObject):
    def __init__(self, game, image_path='Animated/greenLight/0.png', #changed
                 position=(11.5, 3.5), scale_factor=0.8, height_shift=0.16, animation_time=120):
        super().__init__(game, image_path, position, scale_factor, height_shift)
        self.animation_time = animation_time
        self.directory_path = image_path.rsplit('/', 1)[0]
        self.images = self.load_images(self.directory_path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def load_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
