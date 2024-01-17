
import pixpy as pix
from typing import Dict
import math
import os

from pixpy import Float2


screen = pix.open_display(size=(640, 480))

font_name = f"{os.path.dirname(__file__)}/data/Impact.ttf"
font = pix.load_font(font_name)

chess = pix.Image(width=32, pixels=[
                  ((i+i//32) & 1) * pix.rgba(0.2,0.1,i/32*8,1) for i in range(32*32)])

# Create a dictionary mapping letters to images
letters  : Dict[str, pix.Image] = {}
for letter in range(0x20, 0x7e):
    img = font.make_image(text=chr(letter), size=32)
    letters[chr(letter)] = img
letters['\n'] = letters[' ']

text = '''
HELLO FOLKS. THIS IS A CIRCLE SCROLLER.
IT'S JUST A SIMPLE EXAMPLE THAT CREATES IMAGES FROM LETTERS OF A FONT,
AND RENDERS THE IMAGES IN A CIRCLE
'''

radius = screen.size.y / 2 - 50
center = screen.size / 2
index = -50.0
cr : float = 0
while pix.run_loop():
    screen.clear()
    screen.draw_color = 0xffffffff
    screen.draw(image=chess, center=center, size=screen.size *
                (math.sin(cr) + 4.2), rot=cr)
    cr += 0.002
    r : float = index - int(index)
    a = r / 10.0 + 2 * math.pi
    for i in range(int(index), int(index) + 61):
        p = pix.Float2.from_angle(a) * Float2(radius, -radius) + center
        a -= 0.1
        c = a
        if c > 2 * math.pi - 1:
            c = 2 * math.pi - c
        if c > 1:
            c = 1
        if 0 <= i < len(text):
            l = letters[text[i]]
            screen.draw_color = pix.rgba(
                math.sin(a*2) * 0.5 + 0.5, math.sin(a*0.3) * 0.5 + 0.5, 1, c)
            screen.draw(image=l, center=p, rot=math.pi/2 - a)
    index += 0.1
    screen.swap()
    # exit()
