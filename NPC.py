# Import necessary modules
from light_object import *
from random import randint, random

# Define the NPC class inheriting from AnimatedLight
class NPC(AnimatedLight):
    def __init__(self, game, path='npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        # Load images for different NPC animations
        self.AttackImages = self.load_images(self.directory_path + '/attack')
        self.DeathImages = self.load_images(self.directory_path + '/death')
        self.IdleImages = self.load_images(self.directory_path + '/idle')
        self.PainImages = self.load_images(self.directory_path + '/pain')
        self.WalkImages = self.load_images(self.directory_path + '/walk')
        # Set initial attributes for the NPC
        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 20
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False

    # Update method to update NPC state
    def Update(self):
        self.check_animation_time()
        self.GetLight()
        self.run_logic()

    # Method to check if NPC collides with a wall
    def CheckWall(self, x, y):
        return (x, y) not in self.game.map.world_map

    # Method to handle wall collisions
    def WallCollision(self, dx, dy):
        if self.CheckWall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.CheckWall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    # Method to handle NPC movement
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.WallCollision(dx, dy)

    # Method to handle NPC attacks
    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    # Method to animate NPC death
    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.DeathImages) - 1:
                self.DeathImages.rotate(-1)
                self.image = self.DeathImages[0]
                self.frame_counter += 1

    # Method to animate NPC pain
    def animate_pain(self):
        self.animate(self.PainImages)
        if self.animation_trigger:
            self.pain = False

    # Method to check if NPC is hit by the player
    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_SCREEN_WIDTH - self.sprite_half_width < self.screen_x < HALF_SCREEN_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    # Method to check NPC health
    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()

    # Method to define NPC logic during gameplay
    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()
            if self.pain:
                self.animate_pain()
            elif self.ray_cast_value:
                self.player_search_trigger = True
                if self.dist < self.attack_dist:
                    self.animate(self.AttackImages)
                    self.attack()
                else:
                    self.animate(self.WalkImages)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.WalkImages)
                self.movement()
            else:
                self.animate(self.IdleImages)
        else:
            self.animate_death()

    # Property to get NPC's position on the map
    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    # Method to perform raycasting to detect the player
    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

    # Method to visualize raycasting for debugging
    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)

# Specific NPC subclass for a soldier
class SoldierNPC(NPC):
    def __init__(self, game, path='npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

# Specific NPC subclass for a CacoDemon
class CacoDemonNPC(NPC):
    def __init__(self, game, path='npc/caco_demon/0.png', pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35

# Specific NPC subclass for a CyberDemon
class CyberDemonNPC(NPC):
    def __init__(self, game, path='npc/cyber_demon/0.png', pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25










































