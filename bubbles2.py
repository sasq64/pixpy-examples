import pixpy as pix
import math

screen = pix.open_display(size=(1280, 720))

n = 350
r = 2 * math.pi / 235
x, y, v, t = 0.0, 0.0, 0.0, 0.0
points = [0.0] * n * n * 2
colors = [0] * n * n

screen.point_size = 4.0
font = pix.load_font("data/hyperspace_bold.ttf")
logo = font.make_image(f"{n*n} plots", 60)
while pix.run_loop():
    screen.clear()
    s = screen.size.y / 4.1
    screen.point_size = screen.size.y / 200
    screen.scale = pix.Float2(s, s)
    screen.offset = screen.size / 2

    for i in range(n):
        col = pix.rgba(i / n, 0, 99 / 200, 0.5)
        ri = r * i
        for j in range(i*n,(i+1)*n):
            u = math.sin(i + v) + math.sin(ri + x)
            v = math.cos(i + v) + math.cos(ri + x)
            x = u + t
            colors[j] = col
            points[j*2] = u
            points[j*2+1] = v
            col += 0x00010000
    t += .005
    screen.plot(points, colors)
    screen.scale = pix.Float2.ONE
    screen.offset = pix.Float2.ZERO
    screen.draw(image=logo, top_left=(50,50))
    screen.swap()
