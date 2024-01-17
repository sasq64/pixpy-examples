
import os
import struct
from dataclasses import dataclass, field
import pixpy as pix

BOX = 9
PLAYER = 13*4
GOAL = 13*7+11
FLOOR = 13*6+11
WALL = 6*13+9
GOAL_BOX = 9+4*13

ZERO = pix.Float2.ZERO
@dataclass
class Sprite:
    pos: pix.Float2
    img: pix.Image
    vel: pix.Float2 = field(default_factory=pix.Float2) 
    count: int = 0

class Sokoban:
    def load_levels(self, fn):

        block_map = {
            '#': [WALL,0],
            ' ': [FLOOR,0],
            '$': [FLOOR, BOX],
            '.': [GOAL,0],
            '*': [GOAL,BOX],
            '@': [FLOOR,PLAYER],
            '+': [GOAL,PLAYER]
        }

        self.levels = []

        level = []
        with open(fn, "r") as f:
            for line in f.readlines():
                if line[0] == ';':
                    self.levels.append(level)
                    level = []
                    continue
                t = [block_map[i] for i in line.rstrip()]
                level.append(t)

    def __init__(self):
        self.screen = pix.open_display(width=1280, height=860)
        self.tile_size = pix.Float2(64, 64)

        self.con = pix.Console(cols=20, rows=20, tile_size=self.tile_size)
        tiles = pix.load_png("data/sokoban_tilesheet.png").split(size=self.tile_size)
        for i, tile in enumerate(tiles):
            self.con.get_image_for(256 + i).copy_from(tile)

        self.load_levels("data/sokoban_levels.txt")
        level = self.levels[0]
        pos = pix.Int2(0,0)
        sprites : list[Sprite] = []
        for line in level:
            pos = pix.Int2(0, pos.y + 1)
            for (tile,item) in line:
                if item != 0:
                    sprite = Sprite(pos.tof(), self.con.get_image_for(256+item))
                    sprites.append(sprite)
                    if item == PLAYER:
                        self.player = sprite
                self.con.put(pos, tile + 256)
                pos += (1, 0)
        self.sprites = sprites

    def run(self):
        while pix.run_loop():
            self.screen.draw(self.con)
            for sprite in self.sprites:

                self.screen.draw(sprite.img, sprite.pos * self.tile_size)
                if sprite.count > 0:
                    sprite.pos += sprite.vel
                    sprite.count -= 1
                    if sprite.count == 0:
                        sprite.pos = sprite.pos.round()

            target = pix.Float2.ZERO
            if pix.was_pressed(pix.key.LEFT):
                target = self.player.pos + (-1, 0)
            if pix.was_pressed(pix.key.UP):
                target = self.player.pos + (0, -1)

            if target != pix.Float2.ZERO:
                tile = self.con.get(target.toi()) 
                if tile == BOX + 256:
                    pass

                if tile != WALL + 256:
                    self.player.vel = (target - self.player.pos) / 8 
                    self.player.count = 8
            self.screen.swap()
        

game = Sokoban()
game.run()

