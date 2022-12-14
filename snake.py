import pixpy as pix
from pixpy import Int2

class SnakeGame:

    ADD = [Int2(1, 0), Int2(0, 1), Int2(-1, 0), Int2(0, -1)]
    APPLE = ord('$')

    def make_apple(self):
        while True:
            pos = self.con.grid_size.random()
            if self.con.get(pos) == 0x20:
                self.con.put(pos, SnakeGame.APPLE)
                break


    def __init__(self):
        self.screen = pix.open_display(width=640, height=480)
        self.score = 0
        self.con = pix.Console()
        self.pos = Int2(10, 10)
        self.direction = 0

        self.make_apple()

        while pix.run_loop():
            self.screen.clear()
            for e in pix.all_events():
                if isinstance(e, pix.event.Key):
                    match e.key:
                        case pix.key.RIGHT:
                            self.direction = (self.direction + 1) % 4
                        case pix.key.LEFT:
                            self.direction = (self.direction + 3) % 4
                        case _:
                            pass

            if self.screen.frame_counter % 10 == 0:
                self.pos += SnakeGame.ADD[self.direction]
                c = self.con.get(self.pos)
                if c == 0x20:
                    pass
                elif c == SnakeGame.APPLE:
                    self.score += 1
                    self.make_apple()
                else:
                    break
                self.con.put(self.pos, ord('█'))

            self.con.cursor_pos = (0,0)
            self.con.write(f"SCORE {self.score}")
            self.con.render(self.screen.context, size=self.screen.size)
            self.screen.swap()


game = SnakeGame()