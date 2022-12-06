import pixpy as pix

screen = pix.open_display(size=(1280, 720))
canvas = pix.Image(size=screen.size)

while pix.run_loop():
    if pix.is_pressed(pix.key.LEFT_MOUSE):
        canvas.filled_circle(center=pix.get_pointer(), radius=10)
    screen.draw(canvas)
    screen.swap()
