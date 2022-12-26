import os
import pixpy as pix

screen = pix.open_display((1280, 720))

sprites: dict[str, list[pix.Image]] = {}
with os.scandir('data/knight') as it:
    for entry in it:
        if entry.name.endswith(".png") and entry.is_file():
            name = os.path.splitext(entry.name)[0].lower()
            sprites[name] = pix.load_png(entry.path).split(width=120, height=80)

WALKING = "run"
ATTACK = "attack"
JUMP = "jump"

state = WALKING
pos = pix.Int2(200,200)
frame = 0
sheet = sprites[WALKING]
start_frame = 0

dir = pix.Float2(2,2)

while pix.run_loop():
    screen.clear()
    if state == WALKING:
        if pix.is_pressed(pix.key.LEFT):
            dir = pix.Float2(-2, 2)
            pos -= (2,0)
        elif pix.is_pressed(pix.key.RIGHT):
            dir = pix.Float2(2, 2)
            pos += (2,0)
    if pix.was_pressed(pix.key.TAB):
        state = ATTACK
        start_frame = screen.frame_counter
    elif pix.was_pressed("z"):
        state = JUMP
        start_frame = screen.frame_counter

    if state != WALKING:
        frame = (screen.frame_counter - start_frame) // 10
        if frame == len(sheet):
            state = WALKING
    
    if state == JUMP:
        pos -= (0,1)

    if state == WALKING:
        frame = (pos.x // 10) % 10
    sheet = sprites[state]
    img = sheet[frame]
    screen.draw(image=img, center=pos.tof(), size=img.size*dir)
    screen.swap()
