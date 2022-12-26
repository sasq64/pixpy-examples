import pixpy as pix

screen = pix.open_display(width=1280, height=720)
canvas = pix.Image(size=screen.size)

zoom = 1.0
canvas.point_size = 1
last = pix.Float2.ZERO
while pix.run_loop():
    screen.clear()
    for e in pix.all_events():
        if isinstance(e, pix.event.Click):
            last = e.pos
            canvas.line(start=last / zoom + 0.5, end=last / zoom + 0.5)
        elif isinstance(e, pix.event.Move):
            if e.buttons:
                canvas.line(start=last / zoom + 0.5, end=e.pos  / zoom + 0.5)
                last = e.pos
        elif isinstance(e, pix.event.Text):
            if e.text == '+':
                zoom *= 2
    screen.draw(image=canvas, size=canvas.size*zoom)
    screen.swap()

