import os
import pixpy as pix

screen = pix.open_display((1280, 720))

sprites: dict[str, list[pix.Image]] = {}
with os.scandir('data/knight') as it:
    for entry in it:
        if entry.name.endswith(".png") and entry.is_file():
            name = os.path.splitext(entry.name)[0]
            sprites[name] = pix.load_png(entry.path).split(width=120, height=80)

sheet = sprites["Run"]
pos = pix.Int2(200,200)
dir = pix.Float2(2,2)

while pix.run_loop():
    screen.clear()
    if pix.is_pressed(pix.key.LEFT):
        dir = pix.Float2(-2, 2)
        pos -= (2,0)
    elif pix.is_pressed(pix.key.RIGHT):
        dir = pix.Float2(2, 2)
        pos += (2,0)

    frame = (pos.x // 10) % 10
    img = sheet[frame]
    screen.draw(image=img, center=pos.tof(), size=img.size*dir)
    screen.swap()
