import pixpy as pix
import math
from typing import Generator


def sine(low: float, high: float, steps: int) -> Generator[float, None, None] :
    d = high - low 
    for i in range(steps):
        yield (math.sin(i * 2 * math.pi / steps) * d + d) * 0.5 + low

class Color:
    def __init__(self, r: float, g: float, b: float, a: float):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @staticmethod
    def from_int(rgb: int):
        return Color(
            (rgb >> 24) / 255,
            ((rgb >> 16) & 0xFF) / 255,
            ((rgb >> 8) & 0xFF) / 255,
            (rgb & 0xFF) / 255,
        )

    def to_int(self):
        self.r = max(0, min(1.0, self.r))
        self.g = max(0, min(1.0, self.g))
        self.b = max(0, min(1.0, self.b))
        self.a = max(0, min(1.0, self.a))
        return (
            (int(self.r * 255) << 24)
            | (int(self.g * 255) << 16)
            | (int(self.b * 255) << 8)
            | (int(self.a) * 255)
        )

    def __mul__(self, f: float):
        return Color(self.r * f, self.g * f, self.b * f, self.a * f)

    def __add__(self, col: "Color"):
        return Color(self.r + col.r, self.g + col.g, self.b + col.b, self.a + col.a)

    def __sub__(self, col: "Color"):
        return Color(self.r - col.r, self.g + col.g, self.b - col.b, self.a - col.a)


screen = pix.open_display(size=(1280, 1024))

#image = pix.Font.UNSCII_FONT.make_image("SLAYERS", 128)
font = pix.load_font("data/Impact.ttf", 20)
image = font.make_image("LAIRFIGHT", 120)

scroll = pix.Font.UNSCII_FONT.make_image("THIS IS A SCROLLTEXT. WE ARE TAKING THE EASY WAY OUT AND JUST CREATING A SINGLE IMAGE FOR THE WHOLE THING!", 16)

ball = pix.Image(32, 32)
ball.draw_color = 0x000060ff
ball.filled_circle(center=(16,16), radius=16)
ball.draw_color = 0x000080ff
ball.filled_circle(center=(16,16), radius=10)
ball.draw_color = 0x0000e0ff
ball.filled_circle(center=(16,16), radius=6)

logo_center = pix.Float2(screen.size.x / 2, 160)

colors = [
    pix.blend_colors([pix.color.RED, pix.color.ORANGE, pix.color.YELLOW, pix.color.LIGHT_GREEN, pix.color.LIGHT_BLUE], t / 128)
    for t in range(128)
]
raster = pix.Image(1, colors)

image.blend_mode = pix.BLEND_MULTIPLY
image.draw(raster, top_left=(0, 0), size=image.size)
image.blend_mode = pix.BLEND_NORMAL

lines = image.split(width=1, height=int(image.size.y))

x = screen.size.x

sine_tab = [x for x in sine(100, 500, 200)]

x_tab = [x for x in sine(10, screen.size.x/2-10, 2000)]
y_tab = [x for x in sine(10, screen.size.y/2-10, 3000)]


tab2 = [x for x in sine(10, 50, 300)]


screen.fps = 0
j = 0
while pix.run_loop():
    screen.clear(0)
    #screen.draw_color = pix.color.RED
    #screen.draw(image, center=logo_center, size=image.size * 10)
    screen.draw_color = pix.color.WHITE
    screen.blend_mode = pix.BLEND_NORMAL
    screen.draw(image, center=logo_center, size=image.size * 2)

    pos = pix.Float2(240,20)
    xx = 240
    #for i,line in enumerate(lines):
    #    screen.draw(line, top_left=(xx, tab2[(i+j) % len(tab2)]), size=line.size*2)
    #    xx += 2
    #    i += 1

    #screen.draw(raster, top_left=(0, 220), size=(screen.size.x, raster.size.y * 8))
    #screen.draw(raster, top_left=(0, 240), size=(screen.size.x, raster.size.y * 8))
    fc = screen.frame_counter
    screen.draw(scroll, top_left=(x, sine_tab[fc % len(sine_tab)]), size=scroll.size * 8)
    x -= 1
    for i in range(14):
        screen.draw(ball, size=ball.size*4, center=(x_tab[(i*53+j) % len(x_tab)],y_tab[(i*15+j) % len(y_tab)]))
    j += 5
    screen.swap()
