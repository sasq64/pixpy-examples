import pixpy as pix
from pixpy import Int2
from typing import List

class SnakeGame:

    ADD = [Int2(1, 0), Int2(0, 1), Int2(-1, 0), Int2(0, -1)]
    APPLE = 0x2b24
    BODY = ord('█')


    def draw_box(self, pos: Int2, size: Int2):
        "Draw an outline box using box characters"
        for i in range(size.x):
            self.con.put(pos + (i,0), ord('━'))
            self.con.put(pos + (i,size.y),ord('━'))
        for i in range(size.y):
            self.con.put(pos + (0,i), ord('│'))
            self.con.put(pos + (size.x,i),ord('│'))
        self.con.put(pos,ord('┍'))
        self.con.put(pos + (size.x,0),ord('┑'))
        self.con.put(pos + (0,size.y),ord('┕'))
        self.con.put(pos + size, ord('┙'))

    def __init__(self):
        self.screen = pix.open_display(width=640*2, height=480*2)
        self.score = 0
        self.length = 10
        sz = self.screen.size.toi()
        self.con = pix.Console(cols = sz.x//(8*4), rows = sz.y//(8*4))
        self.draw_box(Int2(0,0), self.con.grid_size - (1,1))
        self.pos = Int2(10, 10)
        self.direction = 0
        self.snake : List[Int2] = []

        self.make_apple()

        while pix.run_loop():
            self.screen.clear()
            for e in pix.all_events():
                if isinstance(e, pix.event.Key):
                    if e.key == pix.key.RIGHT:
                        self.direction = (self.direction + 1) % 4
                    elif e.key == pix.key.LEFT:
                        self.direction = (self.direction + 3) % 4

            if self.screen.frame_counter % 10 == 0:
                self.snake.append(self.pos)
                self.pos += SnakeGame.ADD[self.direction]
                c = self.con.get(self.pos)
                if c == 0x20:
                    pass
                elif c == SnakeGame.APPLE:
                    self.score += 1
                    self.length += 4
                    self.make_apple()
                else:
                    break
                self.con.put(self.pos, SnakeGame.BODY)

                if len(self.snake) > self.length:
                    tail = self.snake.pop(0)
                    self.con.put(tail, ord(' '))

            self.con.cursor_pos = (2,0)
            self.con.write(f"SCORE {self.score}")
            self.screen.draw(self.con, size=self.screen.size)
            self.screen.swap()

    def make_apple(self):
        while True:
            gs = self.con.grid_size - (2,2)
            pos = gs.random() + (1,1)
            if self.con.get(pos) == 0x20:
                self.con.put(pos, SnakeGame.APPLE, fg = pix.color.RED)
                break




game = SnakeGame()
