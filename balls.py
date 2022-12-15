import math
import random
import pixpy as pix
from dataclasses import dataclass
from pixpy import Float2


@dataclass
class Ball:
    pos: Float2
    vel: Float2
    color: int


rnd = random.random

screen = pix.open_display(size=(1280, 720))
img = pix.Image(64*2, 64*2  )
img.filled_circle(center=img.size/2, radius=img.size.x/2-1)

balls = [Ball(pos=screen.size/2,
              vel=Float2.from_angle(rnd() * math.pi * 2) * (rnd() + 0.01) * 3,
              color=pix.rgba(rnd(), rnd(), rnd(), 0.5)) for _ in range(1000)]

m = img.size
s = 0.0
while pix.run_loop():
    screen.clear()
    p = s
    s += 0.01
    for ball in balls:
        screen.draw_color = ball.color
        screen.draw(image=img, center=ball.pos, size=img.size * (math.sin(p) + 2.0) * 0.25)
        p += 0.1
        ball.pos += ball.vel
        d = ball.pos.clip(Float2.ZERO - m, screen.size + m)
        if d != Float2.ZERO:
            ball.pos -= (screen.size + m*2) * d.sign()
    screen.swap()
