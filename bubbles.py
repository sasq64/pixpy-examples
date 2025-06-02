import pixpy as pix
import math

class FrameGen:
    def __init__(self):
        self.i = 0
    def frame(self):
        self.i += 100
        for i in range(10):
            yield self.i + i


class BubbleGen:
    def __init__(self):
        self.v = 0
        self.x = 0
        self.t = 0

    def frame(self):
        v,x,t = self.v,self.x,self.t
        n = 300
        r = 2 * math.pi / 235
        for i in range(n):
            for _ in range(n):
                u = math.sin(i + v) + math.sin(r * i + x)
                v = math.cos(i + v) + math.cos(r * i + x)
                x = u + t
                yield pix.Float2(u, v)
        self.v = v
        self.x = x
        self.t += .005

screen = pix.open_display(size=(1280, 720))
screen.point_size = 3
bg = BubbleGen()

n = 200
colors = [pix.rgba(i / n, j / n, 99 / 200, 1.0) for i in range(n) for j in range(n)]

s = screen.height / 4
screen.scale = pix.Float2(s, s)
screen.offset = screen.size / 2
while pix.run_loop():
    screen.clear()
    for i, pos in enumerate(bg.frame()):
        screen.plot(pos, colors[i])
    screen.swap()
