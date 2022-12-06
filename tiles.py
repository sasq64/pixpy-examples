import pixpy as pix
import struct
import os
from pixpy import Float2
from typing import List


class Panel:

    def __init___(self, pos: Float2, size: Float2):
        self.pos = pos
        self.size = size

    def on_click(self, pos: Float2):
        return False

    def render(self, screen: Float2):
        pass

class TileEditor:

    def __init__(self, con: pix.Console, screen: pix.Screen):
        self.screen = screen
        self.tile_size = con.tile_size
        self.con = con
        self.offset = Float2.ZERO
        
        self.panel_size = Float2(16, 40)

        self.tiles = pix.load_png('data/mono_tiles.png'). \
            split(self.tile_size * (1,1))

        for i in range(len(self.tiles)):
            con.get_image_for(1024 + i).copy_from(self.tiles[i])

        self.colors = [
            pix.color.BLACK,
            pix.color.WHITE,
            pix.color.RED,
            pix.color.CYAN,
            pix.color.PURPLE,
            pix.color.GREEN,
            pix.color.BLUE,
            pix.color.YELLOW,
            pix.color.ORANGE,
            pix.color.BROWN,
            pix.color.LIGHT_RED,
            pix.color.DARK_GREY,
            pix.color.GREY,
            pix.color.LIGHT_GREEN,
            pix.color.LIGHT_BLUE,
            pix.color.LIGHT_GREY,
        ]

        self.offset = Float2.ZERO
        self.tile = 1
        self.tpos = Float2.ZERO
        self.epos = Float2.ZERO
        self.scroll_step = 8 * 16
        self.filling = False
        self.bank = 0
        self.zoom = 2.0
        self.current_color = 1
        self.dialog = None
        self.saved : List[int] = []

        self.info = pix.Console(cols=20, rows=10)
        self.info.write("Tile:00")

        # self.saved = self.con.get_tiles()
        # data = struct.pack(f'{len(self.saved)}I', *self.saved)
        if os.path.exists("tiles.dat"):
            with open("tiles.dat", "rb") as f:
                data = f.read()
                self.saved = list(struct.unpack(f'{len(data) // 4}I', data))
                con.set_tiles(self.saved)

    def ask_line(self):
        self.dialog = pix.Console(cols=40, rows=1)
        self.dialog.get_line()

    def update(self):
        for event in pix.all_events():
            match event:
                case pix.event.Text(text):
                    if self.dialog:
                        self.dialog = None
                        continue
                    match text:
                        case '/':
                            self.ask_line()
                        case 'k':
                            self.saved = self.con.get_tiles()
                            data = struct.pack(f'{len(self.saved)}I',
                                               *self.saved)
                            f = open("tiles.dat", "wb")
                            f.write(data)
                            f.close()
                        case 'l':
                            self.con.set_tiles(self.saved)
                        case '[':
                            self.bank -= 1
                        case ']':
                            self.bank += 1
                        case '=' | '+':
                            self.zoom *= 2.0
                        case '-':
                            self.zoom /= 2.0
                        case 'w':
                            self.offset += Float2(0, self.scroll_step)
                        case 's':
                            self.offset -= Float2(0, self.scroll_step)
                        case 'a':
                            self.offset += Float2(self.scroll_step, 0)
                        case 'd':
                            self.offset -= Float2(self.scroll_step, 0)
                        case _:
                            pass
                    t = ord(text[0]) - 0x30
                    if 0 <= t <= 9:
                        if t == 0:
                            t = 10
                        self.tile = (t - 1) + 10 * self.bank
                case pix.event.Key(_):
                    pass
                case pix.event.Click(pos):
                    if self.select_tile(pos):
                        continue
                    if self.select_color(pos):
                        continue
                    self.tpos = (pos - self.offset) // (
                                self.tile_size * self.zoom)
                    self.epos = self.tpos + Float2.ONE
                    self.filling = True
                case _:
                    pass

    def select_tile(self, pos: Float2):
        ps = self.panel_size
        xy = (pos - (32.0, 32.0)) // self.tile_size
        if 0 <= xy.y < ps.y and 0 <= xy.x <= ps.x:
            self.tile = int(self.bank * 10 + xy.x + xy.y * ps.x)
            self.info.cursor_pos = (5,0)
            self.info.write(f"{self.tile:03}")
            return True
        return False

    def select_color(self, pos: Float2):
        if pos.x > self.screen.width - 32:
            no = pos.y // 30
            if 0 <= no < len(self.colors):
                self.current_color = int(no)
                return True
        return False

    def render_tile_panel(self, screen: pix.Screen):
        screen.draw_color = pix.color.DARK_GREY
        pos = Float2(32, 32)
        screen.filled_rect(top_left=pos - 4,
                           size=self.panel_size * self.tile_size + 8)
        screen.draw_color = pix.color.WHITE
        for y in range(int(self.panel_size.y)):
            for x in range(int(self.panel_size.x)):
                i = x + int(self.panel_size.x) * y
                if i + self.bank * 10 >= len(self.tiles):
                    break
                screen.draw(self.tiles[i + self.bank * 10],
                            Float2(x, y) * self.tile_size + pos)
        screen.draw_color = pix.color.GREEN
        b = self.bank * 10
        x = (self.tile - b) % self.panel_size.x
        y = (self.tile - b) / self.panel_size.x
        p = Float2(int(x), int(y))
        screen.rect(
            top_left=p * self.tile_size + pos, size=self.tile_size.tof())

    def render_colors(self, screen: pix.Screen):
        size = Float2(30, 30)
        pos = Float2(screen.width - size.x - 2, 2)
        for col in self.colors:
            screen.draw_color = col
            screen.filled_rect(top_left=pos, size=size - 2)
            pos += (0, size.y)

    def render(self):
        self.screen.clear(pix.color.BLUE)
        self.con.render(self.screen.context, self.offset, self.tile_size *
                        self.con.grid_size * self.zoom)
        self.render_tile_panel(self.screen)
        self.render_colors(self.screen)

        self.info.render(self.screen.context, (0, self.screen.height - 11 * 16))

        if self.dialog:
            self.screen.draw_color = pix.color.RED
            pos = Float2(0, self.screen.size.y - self.dialog.tile_size.y)
            self.screen.filled_rect(top_left=pos - (2, 2),
                                    size=(self.dialog.grid_size *
                                          self.dialog.tile_size) + 4)
            self.dialog.render(self.screen.context, pos=pos)

        if not self.filling:
            return
        # Handle filling
        if pix.is_pressed(pix.key.LEFT_MOUSE):
            mouse = pix.get_pointer()
            self.epos = (mouse - self.offset) // (self.tile_size * self.zoom)
            self.screen.rect(
                self.tpos * self.tile_size * self.zoom + self.offset,
                (self.epos - self.tpos + Float2.ONE) *
                self.tile_size * self.zoom)
        else:
            self.filling = False
            self.con.set_color(self.colors[self.current_color], pix.color.BLACK)
            for y in range(int(self.tpos.y), int(self.epos.y + 1)):
                for x in range(int(self.tpos.x), int(self.epos.x + 1)):
                    self.con.put((x, y), 1024 + self.tile)


def main():
    screen = pix.open_display(width=1280, height=860)
    con = pix.Console(cols=256, rows=256, tile_size=(16, 16))

    tile_editor = TileEditor(con, screen)

    while pix.run_loop():
        tile_editor.update()
        tile_editor.render()
        screen.swap()


main()
