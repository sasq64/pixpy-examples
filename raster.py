import pixpy as pix
import math
#from typing import List

def raster(colors: list[int], y: int, h: int, a: int, b: int):
    for i in range(h):
        col = pix.blend_color(a, b, (math.cos(math.pi * 2 * i / h) + 1) / 2) 
        colors[i+y] = pix.add_color(colors[i+y], col) 


screen = pix.open_display(width=1280, height=720)

canvas = pix.Image(size=(1280, 720))

face = pix.load_png('data/face.png')

a0 = pix.color.BLUE
b0 = pix.color.GREEN

a1 = pix.color.BLACK
b1 = pix.color.YELLOW

#colors = [ b ] * 100

d = 0
z = 3
while pix.run_loop():
    screen.clear()
    pos = pix.get_pointer()

    colors = [0] * 256
    raster(colors, 45, 32, pix.color.BLACK, pix.color.RED)
    raster(colors, 55, 32, pix.color.BLACK, pix.color.BLUE)
    tex = pix.Image(1, colors)
    z += 0.001





    canvas.filled_circle(center=pos, radius=4)
    canvas.line(end=pos)

    #screen.draw(image=face, size=screen.size)
    #screen.draw(canvas)
    screen.draw(tex, top_left=(0,0), size=screen.size)

    screen.swap()
