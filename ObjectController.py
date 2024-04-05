from light_object import *
from NPC import *
from random import choices, randrange


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'npc/'
        self.static_sprite_path = 'skullCandle/' #changed
        self.anim_sprite_path = 'Animated/' #changed
        add_sprite = self.AddLight
        add_npc = self.newNPC
        self.npc_positions = {}

        # spawn npc
        self.enemies = 20  # npc count
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.Spawn()

        # sprite map
        add_sprite(AnimatedLight(game))
        add_sprite(AnimatedLight(game, position=(1.5, 1.5)))
        add_sprite(AnimatedLight(game, position=(1.5, 7.5)))
        add_sprite(AnimatedLight(game, position=(5.5, 3.25)))
        add_sprite(AnimatedLight(game, position=(5.5, 4.75)))
        add_sprite(AnimatedLight(game, position=(7.5, 2.5)))
        add_sprite(AnimatedLight(game, position=(7.5, 5.5)))
        add_sprite(AnimatedLight(game, position=(14.5, 1.5)))
        add_sprite(AnimatedLight(game, position=(14.5, 4.5)))
        add_sprite(AnimatedLight(game, image_path=self.anim_sprite_path + 'redLight/0.png', position=(14.5, 5.5)))
        add_sprite(AnimatedLight(game, image_path=self.anim_sprite_path + 'redLight/0.png', position=(14.5, 7.5)))
        add_sprite(AnimatedLight(game, image_path=self.anim_sprite_path + 'redLight/0.png', position=(12.5, 7.5)))
        add_sprite(AnimatedLight(game, image_path=self.anim_sprite_path + 'redLight/0.png', position=(9.5, 7.5)))
        add_sprite(AnimatedLight(game, image_path=self.anim_sprite_path + 'redLight/0.png', position=(14.5, 12.5)))
        add_sprite(AnimatedLight(game, image_path=self.anim_sprite_path + 'redLight/0.png', position=(9.5, 20.5)))
        add_sprite(AnimatedLight(game, image_path=self.anim_sprite_path + 'redLight/0.png', position=(10.5, 20.5)))
        add_sprite(AnimatedLight(game, image_path=self.anim_sprite_path + 'redLight/0.png', position=(3.5, 14.5)))
        add_sprite(AnimatedLight(game, image_path=self.anim_sprite_path + 'redLight/0.png', position=(3.5, 18.5)))
        add_sprite(AnimatedLight(game, position=(14.5, 24.5)))
        add_sprite(AnimatedLight(game, position=(14.5, 30.5)))
        add_sprite(AnimatedLight(game, position=(1.5, 30.5)))
        add_sprite(AnimatedLight(game, position=(1.5, 24.5)))


    def Spawn(self):
        for i in range(self.enemies):
                npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.newNPC(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def Win(self):
        if not len(self.npc_positions):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.Win()

    def newNPC(self, npc):
        self.npc_list.append(npc)

    def AddLight(self, sprite):
        self.sprite_list.append(sprite)