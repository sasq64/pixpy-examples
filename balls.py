import math
import random
import pixpy as pix
from dataclasses import dataclass
from pixpy import Float2

import utils.tween as tween

@dataclass
class Ball:
    pos: Float2
    vel: Float2
    color: int


rnd = random.random

screen = pix.open_display(size=(1280, 720))
img = pix.Image(size=(64 * 2, 64 * 2))
img.filled_circle(center=img.size / 2, radius=img.size.x / 2 - 1)

balls = [
    Ball(
        pos=screen.size / 2,
        vel=Float2.from_angle(rnd() * math.pi * 2) * (rnd() + 0.025) * 3,
        color=pix.rgba(rnd(), rnd(), rnd(), 0.5),
    )
    for _ in range(1000)
]

font = pix.load_font("data/Impact.ttf")
text = font.make_image("circles", 32)
text.set_texture_filter(False, False)
y = screen.size.y - text.size.y * 4 - 20
xpos_iter = tween.tween(Float2(-200, y), Float2(20, y), 50, tween.Ease.out_sine)

margin = img.size
s = 0.0

while pix.run_loop():
    screen.clear()
    p = s
    s += 0.01
    for ball in balls:
        screen.draw_color = ball.color
        screen.draw(
            image=img, center=ball.pos, size=img.size * (math.sin(p) + 2.0) * 0.25
        )
        p += 0.1
        ball.pos += ball.vel
        d = ball.pos.clip(Float2.ZERO - margin, screen.size + margin)
        if d != Float2.ZERO:
            ball.pos -= (screen.size + margin * 2) * d.sign()
    screen.draw_color = pix.color.WHITE
    screen.draw(text, top_left=next(xpos_iter), size=text.size * 4)
    screen.swap()
