import pixpy as pix
import math
from dataclasses import dataclass, field
from typing import Union, Any, Optional, TYPE_CHECKING, cast

Float2 = pix.Float2

@dataclass
class Hex:
    tiles: list[int] 

def cartesian_to_axial(x: float, y: float, r: float) -> tuple[int, int]:
    # Convert Cartesian coordinates to floating-point axial coordinates for flat-top hexagons
    q_prime = (2 / 3 * x) / r
    r_prime = (-1 / 3 * x + math.sqrt(3) / 3 * y) / r

    # Round to nearest hexagonal grid point
    q = round(q_prime)
    r = round(r_prime)
    s = round(-q_prime - r_prime)

    # Ensure q + r + s = 0 by correcting the largest rounding error
    if q + r + s != 0:
        dq = abs(q - q_prime)
        dr = abs(r - r_prime)
        ds = abs(s - (-q_prime - r_prime))

        if dq > dr and dq > ds:
            q = -r - s
        elif dr > ds:
            r = -q - s
        else:
            s = -q - r

    return (q, r)


def cartesian_to_axial2(x: float, y: float, r: float) -> tuple[int, int]:
    # Convert Cartesian coordinates to floating-point axial coordinates
    q_prime = (math.sqrt(3)/3 * x - 1/3 * y) / r
    r_prime = (2/3 * y) / r

    # Round to nearest hexagonal grid point
    q = round(q_prime)
    r = round(r_prime)
    s = round(-q_prime - r_prime)

    # Ensure q + r + s = 0 by correcting the largest rounding error
    if q + r + s != 0:
        dq = abs(q - q_prime)
        dr = abs(r - r_prime)
        ds = abs(s - (-q_prime - r_prime))

        if dq > dr and dq > ds:
            q = -r - s
        elif dr > ds:
            r = -q - s
        else:
            s = -q - r

    return (q, r)


hexes: list[Hex] = [Hex([]) for _ in range(100)]


def cross(context: pix.Context, xy: Float2, r: float):
    context.line(xy - (r, r), xy + (r, r))
    context.line(xy + (r, -r), xy + (-r, r))


def draw_hex_old(context: pix.Context, xy: Float2, size: Float2):
    size *= (2/3, math.sqrt(3)/3)
    points = [xy + size * Float2.from_angle(a*math.pi/3) for a in range(7)]
    context.lines(points)

def draw_hex(context: pix.Context, xy: Float2, r: float):
    points = [xy + Float2.from_angle(a*math.pi/3) * r for a in range(7)]
    context.lines(points)

def draw_hex_map(context: pix.Context):
    sz = Float2(40, 40)

    pos = Float2(0,0)
    for x in range(0, 10):
        xy = pos + (0, (x & 1) * sz.y / 2)
        for y in range(0, 10):
            draw_hex(context, xy, 30)
            xy += (0, math.sqrt(3) * 30)
            hex = hexes[x + y * 10]
            if len(hex.tiles) > 0:
                context.filled_circle(xy, sz.x/2)
        pos += (3 * 30 / 2, 0)


col = pix.color            

colors = [
    col.BLUE, col.RED, col.BROWN, col.CYAN, col.DARK_GREY, col.GREEN, col.LIGHT_RED,
    col.YELLOW, col.GREY, col.PURPLE, col.ORANGE, col.WHITE, 0x204060, 0xff8070, 0x0076e0, 0xff2070, 0x304080
]




def draw_water(context: pix.Context, xy: Float2):
    context.draw_color = pix.color.BLUE
    context.filled_circle(xy, 30)
    context.draw_color = pix.color.LIGHT_BLUE
    context.lines([])


screen = pix.open_display(width=1280, height=720)

print(hexes[0])
hexes[7] = Hex([1])
hexes[37] = Hex([1])
print(hexes[0])
canvas = pix.Image(size=screen.size)
while pix.run_loop():
    screen.clear()
    screen.draw(canvas)
    #draw_hex(screen.context, Float2(100, 100), Float2(30, 30))
    draw_hex_map(screen.context)
    xy = pix.get_pointer()
    q,r = cartesian_to_axial(xy.x, xy.y, 30)
    print(q, r)
    color = colors[(q + r * 4) & 0xf]
    canvas.plot(xy, color)

    screen.swap()
