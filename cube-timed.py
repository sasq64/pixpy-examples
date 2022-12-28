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

vertices = np.array([[1, 1, 1],     #0
                     [1, 1, -1],    #1
                     [1, -1, 1],    #2
                     [1, -1, -1],   #3
                     [-1, 1, 1],    #4
                     [-1, 1, -1],   #5
                     [-1, -1, 1],   #6    
                     [-1, -1, -1]]) #7

normals = np.array([[1, 0, 0],
                     [-1, 0, 0],
                     [0, 1, 0],
                     [0, -1, 0],
                     [0, 0, 1],
                     [0, 0, -1]])

quads = np.array([[0, 1, 3, 2],
                  [4, 5, 7, 6],
                  [0, 1, 5, 4],
                  [2, 3, 7, 6],
                  [0, 2, 6, 4],
                  [1, 3, 7, 5]])

center = screen.size / 2
screen.line_width = 2
screen.fps = 0
screen.draw_color = 0xffffff80
while pix.run_loop():

    screen.clear()

    mat = make_x_mat(xa) @ make_y_mat(ya) @ make_z_mat(za)

    points = [v @ mat for v in vertices]
    norms = [v @ mat for v in normals]

    d = 4
    z = 3

    p = [pix.Float2(v[0], v[1]) * 150 + center for v in points]

    for i,q in enumerate(quads):
        c = -norms[i][2]
        if c < 0:
            continue
        screen.draw_color = pix.rgba(0,0,c, 1)
        screen.polygon([p[x] for x in q])

    # screen.line(p[0], p[1])
    # screen.line(p[3])
    # screen.line(p[2])
    # screen.line(p[0])

    # screen.line(p[4], p[5])
    # screen.line(p[7])
    # screen.line(p[6])
    # screen.line(p[4])

    # screen.line(p[0], p[4])
    # screen.line(p[1], p[5])
    # screen.line(p[2], p[6])
    # screen.line(p[3], p[7])



    t = screen.seconds
    xa = t * 0.8
    ya = t * 0.2
    za = t * 0.05
    screen.swap()