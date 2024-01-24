from dataclasses import dataclass, field
import pixpy as pix

BOX = 9
PLAYER = 13*4
GOAL = 13*7+11
FLOOR = 13*6+11
WALL = 6*13+9
GOAL_BOX = 9+4*13

@dataclass
class Sprite:
    pos: pix.Float2
    screen_pos: pix.Float2
    img: pix.Image
    vel: pix.Float2 = field(default_factory=pix.Float2) 
    count: int = 0
    
    def move_to(self, target: pix.Float2):
        self.pos = target
        self.vel = (target - self.screen_pos) / 8 
        self.count = 8

    def update(self):
        if self.count > 0:
            self.screen_pos += self.vel
            self.count -= 1
            if self.count == 0:
                self.screen_pos = self.pos


Tile = tuple[int, int]

class Sokoban:
    def load_levels(self, fn: str):

        block_map  : dict[str, Tile]= {
            '#': (WALL,0),
            ' ': (FLOOR,0),
            '$': (FLOOR, BOX),
            '.': (GOAL,0),
            '*': (GOAL,BOX),
            '@': (FLOOR,PLAYER),
            '+': (GOAL,PLAYER)
        }

        self.levels : list[list[list[Tile]]] = []

        level : list[list[Tile]] = []
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
        self.con.set_color(pix.color.WHITE, 0x779699ff)
        tiles = pix.load_png("data/sokoban_tilesheet.png").split(size=self.tile_size)
        for i, tile in enumerate(tiles):
            self.con.get_image_for(256 + i).copy_from(tile)

        self.load_levels("data/sokoban_levels.txt")
        self.level = self.levels[2]
        self.set_level()

    def set_level(self):
        self.con.clear()
        level = self.level
        self.correct = 0
        pos = pix.Int2(0,0)
        sprites : list[Sprite] = []
        self.boxes : list[Sprite] = []
        for line in level:
            pos = pix.Int2(0, pos.y + 1)
            for (tile,item) in line:
                if item != 0:
                    sprite = Sprite(pos.tof(), pos.tof(), self.con.get_image_for(256+item))
                    sprites.append(sprite)
                    if item == PLAYER:
                        self.player = sprite
                    elif item == BOX:
                        self.boxes.append(sprite)
                self.con.put(pos, tile + 256)
                pos += (1, 0)
        self.sprites = sprites


    def run(self):
        while pix.run_loop():
            self.screen.draw(self.con)
            for sprite in self.sprites:
                sprite.update()
                self.screen.draw(sprite.img, sprite.screen_pos * self.tile_size)

            delta = pix.Float2.ZERO
            if pix.was_pressed(pix.key.RIGHT):
                delta = pix.Float2(1, 0)
            if pix.was_pressed(pix.key.DOWN):
                delta = pix.Float2(0, 1)
            if pix.was_pressed(pix.key.LEFT):
                delta = pix.Float2(-1, 0)
            if pix.was_pressed(pix.key.UP):
                delta = pix.Float2(0, -1)
            if pix.was_pressed(pix.key.F1):
                self.set_level()

            if delta != pix.Float2.ZERO:
                target = self.player.pos + delta
                tile = self.con.get(target.toi()) 
                move = True
                self.correct = 0
                if tile != WALL + 256:
                    for box in self.boxes:
                        if self.con.get(box.pos.toi()) == GOAL + 256:
                            self.correct += 1
                        if box.pos == target:
                            box_target = box.pos + delta
                            for box2 in self.boxes:
                                if box2.pos == box_target:
                                    move = False
                                    break
                            box_tile = self.con.get(box_target.toi())
                            if box_tile == WALL + 256:
                                move = False
                            if move:
                                box.move_to(box.pos + delta)
                                if self.con.get(box.pos.toi()) == GOAL + 256:
                                    self.correct += 1
                    if move:
                        self.player.move_to(target)
            img = pix.Font.UNSCII_FONT.make_image(f"{self.correct}/{len(self.boxes)}", 16*4)
            self.screen.draw(img)

            self.screen.swap()
        

game = Sokoban()
game.run()

