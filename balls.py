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

screen = pix.open_display(width=800, height=600)
img = pix.Image(32, 32)
img.filled_circle(center=img.size/2, radius=img.size.x/2-1)

balls = [Ball(screen.size.random(),
              Float2.from_angle(rnd() * math.pi * 2) * rnd() * 3 + 1,
              pix.rgba(rnd(), rnd(), rnd(), 1.0)) for _ in range(1000)]

s = 0.0
while pix.run_loop():
    screen.clear()
    p = s
    s += 0.001
    for ball in balls:
        screen.draw_color = ball.color
        screen.draw(image=img, center=ball.pos, size=img.size * math.sin(p))
        p += 0.01
        ball.pos = ball.pos + ball.vel
        d = ball.pos.clip(Float2.ZERO, screen.size)
        if d != Float2.ZERO:
            ball.pos -= screen.size * d.sign()
    screen.swap()
