import pygame as pg  # Importing pygame library as pg
import math  # Importing math module for mathematical operations
from GameSetting import *  # Importing constants from GameSetting module

class RayCastingEngine:
    def __init__(self, game_instance):
        self.game_instance = game_instance  # Reference to the game instance
        self.ray_casting_result = []  # List to store ray casting results
        self.objects_to_render = []  # List to store objects to render
        self.textures = self.game_instance.object_renderer.wall_textures  # Reference to wall textures

    def prepare_objects_to_render(self):
        self.objects_to_render = []  # Resetting objects to render list
        for ray_index, ray_values in enumerate(self.ray_casting_result):
            depth, proj_height, texture_index, texture_offset = ray_values

            # Rendering wall column based on projection height and texture offset
            if proj_height < SCREEN_HEIGHT:
                wall_column = self.textures[texture_index].subsurface(
                    texture_offset * (TEXTURE_SIZE - RAYCASTING_SCALE), 0, RAYCASTING_SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (RAYCASTING_SCALE, proj_height))
                wall_position = (ray_index * RAYCASTING_SCALE, HALF_SCREEN_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * SCREEN_HEIGHT / proj_height
                wall_column = self.textures[texture_index].subsurface(
                    texture_offset * (TEXTURE_SIZE - RAYCASTING_SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    RAYCASTING_SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (RAYCASTING_SCALE, SCREEN_HEIGHT))
                wall_position = (ray_index * RAYCASTING_SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_position))  # Adding object to render

    def cast_rays(self):
        self.ray_casting_result = []  # Resetting ray casting result list
        texture_vert, texture_hor = 1, 1  # Initialize texture indices
        player_pos_x, player_pos_y = self.game_instance.player.pos  # Get player position
        player_map_x, player_map_y = self.game_instance.player.map_pos  # Get player map position

        ray_angle = self.game_instance.player.angle - HALF_FIELD_OF_VIEW + 0.0001  # Initialize ray angle
        for ray_index in range(NUMBER_OF_RAYS):
            sin_ray_angle = math.sin(ray_angle)  # Calculate sine of ray angle
            cos_ray_angle = math.cos(ray_angle)  # Calculate cosine of ray angle

            # Horizontal intersections
            y_hor, dy = (player_map_y + 1, 1) if sin_ray_angle > 0 else (player_map_y - 1e-6, -1)

            depth_hor = (y_hor - player_pos_y) / sin_ray_angle
            x_hor = player_pos_x + depth_hor * cos_ray_angle

            delta_depth = dy / sin_ray_angle
            dx = delta_depth * cos_ray_angle

            for _ in range(MAX_RENDER_DISTANCE):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game_instance.map.world_map:
                    texture_hor = self.game_instance.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # Vertical intersections
            x_vert, dx = (player_map_x + 1, 1) if cos_ray_angle > 0 else (player_map_x - 1e-6, -1)

            depth_vert = (x_vert - player_pos_x) / cos_ray_angle
            y_vert = player_pos_y + depth_vert * sin_ray_angle

            delta_depth = dx / cos_ray_angle
            dy = delta_depth * sin_ray_angle

            for _ in range(MAX_RENDER_DISTANCE):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game_instance.map.world_map:
                    texture_vert = self.game_instance.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Determine which intersection is closer
            if depth_vert < depth_hor:
                depth, texture_index = depth_vert, texture_vert
                y_vert %= 1
                texture_offset = y_vert if cos_ray_angle > 0 else (1 - y_vert)
            else:
                depth, texture_index = depth_hor, texture_hor
                x_hor %= 1
                texture_offset = (1 - x_hor) if sin_ray_angle > 0 else x_hor

            # Remove fishbowl effect
            depth *= math.cos(self.game_instance.player.angle - ray_angle)

            # Projection
            proj_height = SCREEN_DISTANCE / (depth + 0.0001)

            # Store ray casting result
            self.ray_casting_result.append((depth, proj_height, texture_index, texture_offset))

            ray_angle += DELTA_ANGLE  # Increment ray angle

    def update(self):
        self.cast_rays()  # Cast rays to generate ray casting result
        self.prepare_objects_to_render()  # Prepare objects to render based on ray casting result
