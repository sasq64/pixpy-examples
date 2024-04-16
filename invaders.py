import pixpy as pix
Float2 = pix.Float2

screen = pix.open_display(width=800, height=600)

img = pix.load_png("data/invaders.png")
bg = pix.load_png("data/background.png")
sprites = img.split(cols=8, rows=2)
enemies = sprites[0:6]
player = sprites[13]
pos = Float2(400, 552)

while pix.run_loop():
    screen.draw(image=bg)
    for e in enemies:
        screen.draw(image=e, center=e.pos * 2 + (pos.x/2, 200), size=e.size * 2)
    screen.draw(image=player, top_left=pos, size=player.size*2)
    if pix.is_pressed(pix.key.LEFT):
        pos -= (2, 0)
    elif pix.is_pressed(pix.key.RIGHT):
        pos += (2, 0)
    screen.swap()