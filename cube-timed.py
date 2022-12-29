import pixpy as pix
import numpy as np
import random


def make_x_mat(a: float):
    return np.array([[1, 0, 0],
                    [0, np.cos(a), -np.sin(a)],
                    [0, np.sin(a), np.cos(a)]])


def make_y_mat(a: float):
    return np.array([[np.cos(a), 0, np.sin(a)],
                     [0, 1, 0],
                     [-np.sin(a), 0, np.cos(a)]])


def make_z_mat(a: float):
    return np.array([[np.cos(a), -np.sin(a), 0],
                     [np.sin(a), np.cos(a), 0],
                     [0, 0, 1]])


screen = pix.open_display(size=(1280, 720))
#screen = pix.open_display(full_screen=True)

vertices = np.array([[1, 1, 1],
                     [1, 1, -1],
                     [1, -1, 1],
                     [1, -1, -1],
                     [-1, 1, 1],
                     [-1, 1, -1],
                     [-1, -1, 1],
                     [-1, -1, -1]])

normals = np.array([[1, 0, 0],
                    [-1, 0, 0],
                    [0, 1, 0],
                    [0, -1, 0],
                    [0, 0, 1],
                    [0, 0, -1]])

quads = np.array([
    [1, 0, 2, 3],
    [4, 5, 7, 6],
    [0, 1, 5, 4],
    [2, 6, 7, 3],
    [0, 4, 6, 2],
    [1, 3, 7, 5]
])

screen.line_width = 2
screen.fps = 0

font = pix.load_font("data/Hack.ttf")
text = font.make_image("THIS IS A CUBE. IT IS BLUE", 50)
print(text.width)

sz = screen.size / 2
planes = [pix.Image(size=sz) for _ in range(3)]
c = 0xffffffff
for i,plane in enumerate(planes):
    v = (i+1) / 3;
    c = pix.rgba(v, v, v, 1)
    print(f"{c:x}")
    plane.draw_color = 0xffffffff
    plane.point_size = 1
    for y in range(plane.size.toi().y//3):
        #plane.plot(center=pix.Float2(random.randint(0,screen.size.toi().x), y*3+i), color=c)
        plane.set_pixel((random.randint(0,screen.size.toi().x), y*3+i), c)


while pix.run_loop():

    screen.clear()
    fc = screen.frame_counter
    center = screen.size / 2
    screen.draw_color = 0xffffffff
    t = screen.seconds
    for i,plane in enumerate(planes):
        x = (fc * (i + 1)) % screen.size.toi().x
        screen.draw(image=plane, top_left=pix.Float2(x, 0), size=screen.size)
        screen.draw(image=plane, top_left=pix.Float2(x - screen.size.x, 0), size=screen.size)

    xa = t * 0.8
    ya = t * 0.2
    za = t * 0.05

    mat = make_x_mat(xa) @ make_y_mat(ya) @ make_z_mat(za)

    points = [v @ mat for v in vertices]
    norms = [v @ mat for v in normals]
    p = [pix.Float2(v[0], v[1]) * (5/(v[2] + 4))
         * center.y/3 + center for v in points]

    for i, q in enumerate(quads):
        c = -norms[i][2]
        screen.draw_color = pix.rgba(0, 0, c, 1)
        screen.polygon([p[x] for x in q])

    screen.draw_color = 0xffffffff
    screen.draw(image=text, top_left=screen.size - (fc, 70))
    screen.swap()
