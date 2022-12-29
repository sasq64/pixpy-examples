import pixpy as pix
import numpy as np


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
center = screen.size / 2
screen.line_width = 2

xa = 0.0
ya = 0.0
za = 0.0

vertices = np.array([[1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
                     [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]])

lines = [(0, 1), (1, 3), (3, 2), (2, 0), (4, 5), (5, 7),
         (7, 6), (6, 4), (0, 4), (1, 5), (2, 6), (3, 7)]

while pix.run_loop():

    screen.clear()

    mat = make_x_mat(xa) @ make_y_mat(ya) @ make_z_mat(za)

    points = [v @ mat for v in vertices]

    p = [pix.Float2(v[0], v[1]) * (4/(v[2] + 3))
         * 150 + center for v in points]

    for line in lines:
        screen.line(p[line[0]], p[line[1]])
    xa += 0.001
    ya += 0.002
    za += 0.0005
    screen.swap()
