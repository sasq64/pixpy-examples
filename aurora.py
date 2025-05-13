import pixpy as pix
import musix
import pyaudio
import math
from typing import Iterator

def sine(low: float, high: float, steps: int) -> Iterator[float]:
    """Generate an array of `step` values forming a sin() curve from `low` to `high`"""
    d = high - low
    for i in range(steps):
        yield (math.sin(i * 2 * math.pi / steps) * d + d) * 0.5 + low


p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, channels=2, frames_per_buffer=1024, rate=44100, output=True
)

musix.init()
player = musix.load("data/aurora.mod")


screen = pix.open_display(size=(320 * 2, 240 * 2), full_screen=False)

logo = pix.load_png("data/quartex.png")
logo = logo.crop(size=(logo.size.x, 120))

font = pix.load_font("data/Impact.ttf", 20)
image = pix.Image(320, 64)
#font.make_image("AURORA", 64)
lines = image.split(width=1, height=int(image.size.y))
scroller = font.make_image("THIS IS A SCROLLTEXT, OR SOMETHING LIKE IT", 64)

raster = [
    pix.color.RED,
    pix.color.ORANGE,
    pix.color.YELLOW,
    pix.color.GREEN,
    pix.color.LIGHT_GREEN,
    pix.color.LIGHT_BLUE,
]
colors = [ pix.blend_colors(raster, t / 64,) for t in range(64) ]
raster = pix.Image(1, colors)

y = 100
tab2 = [x for x in sine(y, y + 50, 300)]
screen.fps = 0
j = 0
screen.draw_color = pix.color.WHITE

canvas = pix.Image(320, 240)
x : float = 0
while pix.run_loop():
    canvas.clear(pix.color.BLACK)
    canvas.draw(logo, size=logo.size)

    image.clear()
    image.copy_from(scroller.crop(top_left=(x,0), size = image.size))
    x += 0.5

    for i,line in enumerate(lines):
        canvas.draw(line, top_left=(i, tab2[(j+i) % len(tab2)]), size=line.size)
    j += 3

    canvas.blend_mode = pix.BLEND_MULTIPLY
    canvas.draw(raster, top_left=(0, y), size=(canvas.size.x, 120))
    canvas.blend_mode = pix.BLEND_NORMAL

    sz = stream.get_write_available()
    if sz > 0:
        samples = player.render(sz * 2)
        stream.write(samples)

    screen.draw(canvas, size=screen.size)
    screen.swap()
