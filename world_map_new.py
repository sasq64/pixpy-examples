from dataclasses import dataclass
import sys
from typing import Literal, TypedDict
import pixpy as pix
import json
import random

@dataclass
class BBox:
    min: pix.Float2
    max: pix.Float2

    def __add__(self, p: pix.Float2) -> "BBox":
        return BBox(self.min + p, self.max + p)

    def __mul__(self, p: pix.Float2):
        pass



class Country:
    def __init__(self):
        self.polygons = []
        self.highlight = 0

    polygons: list[list[pix.Float2]]
    bbox: tuple[pix.Float2, pix.Float2]
    pos: pix.Float2
    name: str
    iso2: str
    highlight: int


def bbox(points: list[pix.Float2]) -> tuple[pix.Float2, pix.Float2]:
    """Create a bounding box from `points`"""

    max_x, max_y = sys.float_info.min, sys.float_info.min
    min_x, min_y = sys.float_info.max, sys.float_info.max
    for p in points:
        if p.x < min_x:
            min_x = p.x
        if p.y < min_y:
            min_y = p.y
        if p.x > max_x:
            max_x = p.x
        if p.y > max_y:
            max_y = p.y
    return (pix.Float2(min_x, min_y), pix.Float2(max_x, max_y))

class Property(TypedDict):
    name: str
    name_long: str
    iso_a2_eh: str
    label_x: float
    label_y: float


Point = list[float] # Always size 2

LinearRing = list[Point]


class Geometry(TypedDict):
    type : Literal['Polygon']
    coordinates: list[LinearRing]

class MutliGeometry(TypedDict):
    type : Literal['MultiPolygon']
    coordinates: list[list[LinearRing]]

class Feature(TypedDict):
    properties: Property
    geometry: Geometry | MutliGeometry

class GeoData(TypedDict):
    features: list[Feature]

def read_geo() -> list[Country]:
    countries: list[Country] = []
    with open("data/geo.json") as f:
        data : GeoData = json.load(f)
        for f in data['features']:
            geo = f['geometry']
            polys: list[list[pix.Float2]] = []
            box: list[pix.Float2] = []
            if geo['type'] == 'Polygon':
                for ring in geo['coordinates']:
                    points = [pix.Float2(v[0], -v[1]) for v in ring]
                    box += bbox(points)
                    polys.append(points)
            else:
                for multi in geo['coordinates']:
                    for coords in multi:
                        points = [pix.Float2(v[0], -v[1]) for v in coords]
                        box += bbox(points)
                        polys.append(points)
            country = Country()
            country.bbox = bbox(box)
            country.polygons = polys
            props = f['properties']
            country.name = props['name_long']
            country.iso2 = props['iso_a2_eh']
            country.pos = pix.Float2(props['label_x'], props['label_y'])

            countries.append(country)
    return countries


screen = pix.open_display(width=1920, height=1080)
canvas = pix.Image(size=screen.size)

font = pix.load_font("data/hyperspace_bold.ttf")
countries = read_geo()

scale = pix.Float2(5.3, 6.7)
canvas.scale = scale
offset = pix.Float2(960, 550)
canvas.offset = offset

def draw_world():
    canvas.draw_color = 0x000050FF
    canvas.clear()
    for country in countries:
        for points in country.polygons:
            canvas.draw_color = 0x000050FF
            canvas.polygon(points)


guess = random.randrange(len(countries))
gc = countries[guess]

inside = None
last_result = "Take a guess!"
score = 0

COUNT = 30

questions = COUNT

hilight = None
hilight_time = 0

draw_world()

while pix.run_loop():
    screen.clear()
    screen.draw_color = pix.color.WHITE
    screen.draw(canvas, size = canvas.size)

    img = font.make_image(f"#{COUNT-questions+1} {gc.name}", 40, 0x8080E0FF)
    screen.draw(img, top_left=(10, 10))

    img = font.make_image(last_result, 48, pix.color.WHITE)
    screen.draw(img, top_left=(screen.width - 400, 10))

    img = font.make_image(f"SCORE: {score}", 54, 0x80ff80FF)
    screen.draw(img, top_left=(10, screen.height - 90))

    if questions == 0:
        last_result = "GAME OVER"

    if hilight:
        if hilight_time == 0:
            hilight = None
        hilight_time -= 1

    xy = canvas.get_pointer()
    for country in countries:
        screen.line_width = 2
        min = country.bbox[0]
        max = country.bbox[1]
        if xy.x > min.x and xy.x < max.x and xy.y > min.y and xy.y < max.y:
            for points in country.polygons:
                screen.draw_color = pix.color.BLACK
                if xy.inside_polygon(points):
                    inside = country

    screen.scale = canvas.scale
    screen.offset = canvas.offset
    if inside:
        screen.draw_color = pix.color.WHITE
        for poly in inside.polygons:
            screen.lines(poly)
        screen.draw_color = pix.color.LIGHT_BLUE
        screen.complex_polygon(inside.polygons)

    if hilight:
        screen.draw_color = pix.color.WHITE
        for poly in hilight.polygons:
            screen.lines(poly)
        screen.draw_color = pix.color.LIGHT_GREEN
        screen.complex_polygon(hilight.polygons)

    screen.scale = pix.Float2.ONE
    screen.offset = pix.Float2.ZERO

    if questions > 0:
        if pix.was_pressed(pix.key.LEFT_MOUSE):
            if inside is not None and inside.name == gc.name:
                last_result = "Correct"
                questions -= 1
                score += 3
                guess = random.randrange(len(countries))
                gc = countries[guess]
                #img = font.make_image(inside.name, 48, 0x8080E0FF)
                #screen.draw(img, top_left=(10, 10))
            else:
                score -= 2
                last_result = "Incorrect"

    if pix.was_pressed('z'):
        canvas.scale *= 2
        canvas.offset = offset - pix.get_pointer()
        draw_world()
    elif pix.was_pressed('x'):
        canvas.scale = scale
        canvas.offset = offset
        draw_world()

    if pix.was_pressed(pix.key.SPACE):
        last_result = "Pass"
        hilight = gc
        hilight_time = 100
        score -= 1
        questions -= 1
        if questions < 0:
            questions = COUNT
            score = 0
            last_result = "Take a guess!"
        guess = random.randrange(len(countries))
        gc = countries[guess]
    if score < 0:
        score = 0

    screen.swap()
