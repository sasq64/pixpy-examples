import os
import math
import struct
import pixpy as pix
from pixpy import Float2

WALKING = "Run"
ATTACK = "Attack"
JUMP = "Jump"

class Platformer:

    def to_screen(self, pos: Float2):
        "Convert 2D world position to screen position"
        return pos * self.zoom + self.scroll

    def scroll_to(self, pos: Float2):
        "Scroll play area so that `pos` is visible"
        border = 150
        clip = self.to_screen(pos).clip(pix.Float2(border, border), self.screen.size - border)
        self.scroll -= (clip / self.zoom).toi() 

    def __init__(self):
        screen = pix.open_display((1280, 720))
        self.con = pix.Console(cols=256,rows=24, tile_size=(16,16))

        self.font = pix.load_font('data/Hack.ttf')

        tiles = pix.load_png('data/mono_tiles.png').split(size=self.con.tile_size.tof())
        for i, tile in enumerate(tiles):
            self.con.get_image_for(1024 + i).copy_from(tile)
        if os.path.exists("tiles.dat"):
            with open("tiles.dat", "rb") as f:
                data = f.read()
                saved = list(struct.unpack(f'{len(data) // 4}I', data))
                self.con.set_tiles(saved)

        self.sprites: dict[str, list[pix.Image]] = {}
        with os.scandir('data/knight') as it:
            for entry in it:
                if entry.name.endswith(".png") and entry.is_file():
                    name = os.path.splitext(entry.name)[0]
                    self.sprites[name] = pix.load_png(
                        entry.path).split(width=120, height=80)

        self.speed = {WALKING: 18, ATTACK: 5, JUMP: 20}
        self.state = WALKING
        self.pos = Float2(200, 380) / 4
        self.sheet = self.sprites[WALKING]
        self.start_frame = 0
        self.screen = screen
        self.zoom = 2.5
        self.frame = 0
        self.feet_collide = False
        self.head_collide = False

        self.colliders : list[Float2] = []

        self.dir = pix.Float2(2, 2)
        self.scroll = pix.Float2(0,0)

    def collides(self, pos: Float2):
        self.colliders.append(pos)
        tpos = pos / self.con.tile_size
        return self.con.get(tpos.toi()) != 0x20

    def update_player(self):
        in_anim = True
        self.colliders.clear()
        self.feet_collide = self.collides(self.pos + (0,40))
        self.head_collide = self.collides(self.pos - (0,0))
        self.left_collide = self.collides(self.pos + (-10,10)) or self.collides(self.pos + (-10,30))
        self.right_collide = self.collides(self.pos + (10,10)) or self.collides(self.pos + (10,30))
        if self.state == WALKING or self.state == JUMP:
            in_anim = False
            if pix.is_pressed(pix.key.LEFT):
                self.dir = pix.Float2(-2, 2)
                if not self.left_collide:
                    self.pos -= (0.8, 0)
            elif pix.is_pressed(pix.key.RIGHT):
                self.dir = pix.Float2(2, 2)
                if not self.right_collide:
                    self.pos += (0.8, 0)
        if pix.was_pressed(pix.key.TAB) and not in_anim:
            self.state = ATTACK
            self.start_frame = self.screen.frame_counter
        elif pix.was_pressed("z") and not in_anim and self.feet_collide and not self.head_collide:
            self.state = JUMP
            self.start_frame = self.screen.frame_counter
            self.velocity = self.dir

        self.frame = 0
        if self.state != WALKING:
            self.frame = (self.screen.frame_counter - self.start_frame) // self.speed[self.state]
            if self.frame == len(self.sprites[self.state]):
                self.state = WALKING

        if self.state == WALKING:
            self.frame = int(self.dir.x * self.pos.x * 2 // self.speed[WALKING]) % 10

        # 0 -> 1
        #t = (self.screen.frame_counter - self.start_frame) / \
        #    len(self.sprites[self.state]) / self.speed[self.state]
        if self.state == JUMP:
            if not self.head_collide: 
                self.pos += Float2(0, -1)
            else:
                self.state = WALKING
        else:
            if not self.feet_collide:
                self.pos += (0,1)

    def render(self):

        self.update_player()
        self.scroll_to(self.pos)

        img = self.sprites[self.state][self.frame]
        self.screen.draw_color = pix.color.WHITE
        self.screen.draw(self.con, top_left=self.scroll, size=self.con.tile_size*self.con.grid_size*self.zoom)
        self.screen.draw(image=img, center=self.to_screen(self.pos), size=img.size*self.dir * self.zoom / 2)
        for p in self.colliders:
            self.screen.circle(center=self.to_screen(p), radius=5)
        self.screen.draw(image=self.font.make_image(f"{self.head_collide} {self.feet_collide} L:{self.left_collide} R:{self.right_collide}", 24))

    def run(self):
        while pix.run_loop():
            self.screen.clear()
            self.render()
            self.screen.swap()


p = Platformer()
p.run()