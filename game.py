import pixpy as pix
import dungen
from pixpy import Int2,Float2


class Game:
    MOVE_LOOKUP = {pix.key.LEFT: Int2(-1, 0), pix.key.RIGHT: Int2(1, 0),
                   pix.key.DOWN: Int2(0, 1), pix.key.UP: Int2(0, -1)}

    def __init__(self, con, screen):
        self.screen = screen
        self.con = con
        self.offset = Float2(0, 0)
        self.zoom = 2
        self.tile_size = con.tile_size
        self.tiles = pix.load_png('data/mono_tiles.png').split(self.tile_size)
        for i, tile in enumerate(self.tiles):
            con.get_image_for(1024 + i).copy_from(tile)

        self.map = []
        gen = dungen.MessyBSPTree()
        level = gen.generateLevel(64, 64)
        self.con.set_color(pix.color.LIGHT_GREY, pix.color.BLACK)
        for y in range(len(level)):
            for x in range(len(level[0])):
                self.con.put((x, y), 1024 + level[x][y])

        self.player = self.tiles[26 * 16]
        self.player_pos = Int2(10, 10)

    def to_screen(self, tile_pos):
        return tile_pos * self.tile_size * self.zoom + self.offset

    def update(self):
        for event in pix.all_events():
            match event:
                case pix.event.Key(k):
                    diff = Game.MOVE_LOOKUP[k]
                    if diff:
                        new_pos = self.player_pos + diff
                        if self.con.get(new_pos) == 1024:
                            self.player_pos = new_pos

        border = self.zoom * 100
        screen_pos = self.to_screen(self.player_pos)
        clip = screen_pos.clip(Float2(border, border), self.screen.size - border)
        self.offset -= (clip / self.zoom)

    def render(self):
        self.screen.clear(pix.color.BLUE)
        self.con.render(self.screen.context, self.offset,
                        self.con.grid_size * self.tile_size * self.zoom)
        self.screen.draw(image=self.player,
                         top_left=self.to_screen(self.player_pos),
                         size=self.player.size * self.zoom)


def main():
    screen = pix.open_display(width=1280, height=860)
    con = pix.Console(cols=256, rows=256, tile_size=(16, 16))

    game = Game(con, screen)

    while pix.run_loop():
        game.update()
        game.render()
        screen.swap()


main()
