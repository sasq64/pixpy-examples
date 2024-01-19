import pixpy as pix
import math

def raster(colors: list[int], y: int, h: int, a: int, b: int):
    for i in range(h):
        col = pix.blend_color(a, b, (math.cos(math.pi * 2 * i / h) + 1) / 2) 
        if i + y > 0 and i + y < len(colors):
            colors[i+y] = pix.add_color(colors[i+y], col) 


screen = pix.open_display(width=1280, height=720)
rcolors = [ pix.color.RED, pix.color.BLUE, pix.color.GREEN, pix.color.YELLOW]

while pix.run_loop():
    screen.clear()
    pos = pix.get_pointer()

    colors = [0] * 256
    s = screen.frame_counter / 100
    for i in range(10):
        y = int((math.sin(s) + 1) * 120 - 10)
        raster(colors, y, 48, pix.color.BLACK, rcolors[i&3])
        s += 0.3
    tex = pix.Image(1, colors)

    screen.draw(tex, center=screen.size/2, size=screen.size*2, rot=screen.frame_counter/500)
    screen.swap()
