import pixpy as pix

import math
from typing import Iterator

def sine(low: float, high: float, steps: int) -> Iterator[float] :
    """
    Generate sine values between `low` and `high`, completing a full
    cycle (2 * PI) in `steps` steps.
    """
    d = high - low 
    for i in range(steps):
        yield (math.sin(i * 2 * math.pi / steps) * d + d) * 0.5 + low

screen = pix.open_display(size=(1280, 1024))

font = pix.load_font("data/Hack.ttf", 32)
tile_set = pix.TileSet(font, tile_size=(16,32))
pix.save_png(tile_set.get_tileset_image(), "tile_set.png")

image = pix.Image(size=(screen.size.x, 80))

text = "This is the scrolltext that we want to show"

pos = pix.Float2(0,0)
for t in text:
    c = tile_set.get_image_for(t)
    image.draw(c, top_left=pos)
    pos += (16,0)


lines = image.split(width=1, height=int(image.size.y))



rainbow = [pix.color.RED, pix.color.ORANGE, pix.color.YELLOW, pix.color.GREEN, pix.color.LIGHT_GREEN, pix.color.LIGHT_BLUE]

colors = [ pix.blend_colors(rainbow, t / 64) for t in range(64) ]
raster = pix.Image(1, colors)

y = 450
tab2 = [x for x in sine(y, y+150, 300)]
screen.fps = 0
j = 0
screen.draw_color = pix.color.WHITE

while pix.run_loop():
    screen.clear(0)
    xx = 180
    i = j
    for line in lines:
        screen.draw(line, top_left=(xx, tab2[i % len(tab2)]), size=line.size*2)
        xx += 2
        i += 1
    j += 1
    screen.blend_mode = pix.BLEND_MULTIPLY
    screen.draw(raster, top_left=(0, y), size=(screen.size.x, 440))
    screen.blend_mode = pix.BLEND_NORMAL

    screen.swap()