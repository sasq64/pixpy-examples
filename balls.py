import math
import random
import pixpy as pix
from dataclasses import dataclass
from pixpy import Float2

@dataclass
class Ball:
    """Represents a ball on the screen"""

    pos: Float2
    """Current position of this ball on screen"""

    vel: Float2
    """Current velocity of this ball"""

    color: int
    """Color of this ball"""


rnd = random.random

screen = pix.open_display(size=(1280, 720))

# Create the ball image
img = pix.Image(size=(64 * 2, 64 * 2))
img.filled_circle(center=img.size / 2, radius=img.size.x / 2 - 1)

# Generate initial position, velocity and color for all balls.
# Velocity and color are randomized, but position is always center of screen.
balls = [
    Ball(
        pos=screen.size / 2,
        vel=Float2.from_angle(rnd() * math.pi * 2) * (rnd() + 0.025) * 3,
        color=pix.rgba(rnd(), rnd(), rnd(), 0.5),
    )
    for _ in range(1000)
]

margin = img.size

while pix.run_loop():
    screen.clear()
    z = screen.frame_counter / 100
    for ball in balls:
        screen.draw_color = ball.color
        screen.draw(
            image=img, center=ball.pos, size=img.size * (math.sin(z) + 2.0) * 0.25
        )
        z += 0.1
        ball.pos += ball.vel

        # Check if the center of the ball is outside of screen (plus a margin)
        d = ball.pos.clip(Float2.ZERO - margin, screen.size + margin)
        if d != Float2.ZERO:
            # Move it to the opposite side of the screen
            ball.pos -= (screen.size + margin * 2) * d.sign()

    screen.swap()
