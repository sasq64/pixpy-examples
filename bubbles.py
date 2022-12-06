import pixpy as pix
import math
from typing import Tuple, cast

screen = pix.open_display(size=(1280, 720))

n = 200
r = 2 * math.pi / 235
x, y, v, t = 0, 0, 0, 0

while pix.run_loop():
    (cx, cy) = cast(Tuple[int, int], screen.size / 2)
    
    s = screen.size.y / 5
    screen.clear()
    for i in range(n):
        for j in range(n):
            u = math.sin(i + v) + math.sin(r * i + x)
            v = math.cos(i + v) + math.cos(r * i + x)
            x = u + t
            col = pix.rgba(i / n, j / n, 99 / 200, 1.0)
            screen.plot(pix.Float2(u * s + cx, v * s + cy), col)
    t += .005
    screen.swap()
