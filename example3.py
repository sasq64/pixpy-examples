import pixpy as pix

screen = pix.open_display(width=1280, height=720)

canvas = pix.Image(1280, 720)

face = pix.load_png('data/face.png')

while pix.run_loop():
    pos = pix.get_pointer()

    canvas.filled_circle(center=pos, radius=4)
    canvas.line(end=pos)

    screen.blit(image=face, size=(1280, 720))
    screen.blit(canvas)

    screen.swap()
