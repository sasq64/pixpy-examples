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


xa = 0
ya = 0
za = 0

vertices = np.array([[1, 1, 1],
                     [1, 1, -1],
                     [1, -1, 1],
                     [1, -1, -1],
                     [-1, 1, 1],
                     [-1, 1, -1],
                     [-1, -1, 1],
                     [-1, -1, -1]])

indexes = np.array([[0, 1, 2],
                       [1, 2, 3],
                       [4, 5, 6],
                       [5, 6, 7],
                       [0, 1, 4],
                       [1, 4, 5],
                       [2, 3, 6],
                       [3, 6, 7],
                       [0, 2, 4],
                       [2, 4, 6],
                       [1, 3, 5],
                       [3, 5, 7]])

center = screen.size / 2
screen.line_width = 2
screen.fps = 0
while pix.run_loop():

    screen.clear()

    mat = make_x_mat(xa) @ make_y_mat(ya) @ make_z_mat(za)

    points = [v @ mat for v in vertices]

    d = 4
    z = 3

    p = [pix.Float2(v[0], v[1]) * (d/(v[2] + z)) * 150 + center for v in points]

    screen.line(p[0], p[1])
    screen.line(p[3])
    screen.line(p[2])
    screen.line(p[0])

    screen.line(p[4], p[5])
    screen.line(p[7])
    screen.line(p[6])
    screen.line(p[4])

    screen.line(p[0], p[4])
    screen.line(p[1], p[5])
    screen.line(p[2], p[6])
    screen.line(p[3], p[7])



    t = screen.seconds
    xa = t * 0.1
    ya = t * 0.2
    za = t * 0.05
    print(1.0 / screen.delta)
    screen.swap()