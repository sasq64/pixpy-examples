import pixpy as pix
import math
from typing import Tuple, cast

screen = pix.open_display(size=(1280, 720))

n = 255
r = 2 * math.pi / 235
x, y, v, t = 0, 0, 0, 0
points = [0.0] * n * n * 2
colors = [0] * n * n

screen.point_size = 2.0
font = pix.load_font("data/hyperspace_bold.ttf")
logo = font.make_image("65000 plots", 60)

while pix.run_loop():
    (cx, cy) = cast(Tuple[int, int], screen.size / 2)
    s = screen.size.y / 5
    screen.clear()
    screen.point_size = screen.size.y / 540

    for i in range(n):
        col = pix.rgba(i / n, 0, 99 / 200, 1.0)
        for j in range(i*n,(i+1)*n):
            u = math.sin(i + v) + math.sin(r * i + x)
            v = math.cos(i + v) + math.cos(r * i + x)
            x = u + t
            colors[j] = col
            points[j*2] = u * s + cx
            points[j*2+1] = v * s + cy
            col += 0x00010000
            
    t += .005
    screen.plot(points, colors)
    screen.draw(image=logo, top_left=(50,50))
    screen.swap()
