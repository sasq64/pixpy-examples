from dataclasses import dataclass
import sys
from typing import Literal, TypedDict
import pixpy as pix
import json
import random

F2 = tuple[float, float]

def bbox(points: list[F2] | list[pix.Float2]) -> tuple[pix.Float2, pix.Float2]:
    """Create a bounding box from `points`"""

    max_x, max_y = sys.float_info.min, sys.float_info.min
    min_x, min_y = sys.float_info.max, sys.float_info.max
    for x,y in points:
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    return (pix.Float2(min_x, min_y), pix.Float2(max_x, max_y))

@dataclass
class BBox:
    min: pix.Float2
    max: pix.Float2

    def __init__(self, min: pix.Float2, max: pix.Float2):
        self.min, self.max = min,max

    @staticmethod
    def from_points(points: list[F2] | list[pix.Float2]) -> "BBox":
        x,y = bbox(points)
        return BBox(x, y)

    def __add__(self, p: pix.Float2) -> "BBox":
        return BBox(self.min + p, self.max + p)

    def __mul__(self, p: pix.Float2):
        if p.x < 0 or p.y < 0:
            return BBox.from_points([self.min * p, self.max * p])
        return BBox(self.min * p, self.max * p)



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


class Property(TypedDict):
    name: str
    name_long: str
    iso_a2_eh: str
    label_x: float
    label_y: float

PointList = list[list[float]]

class Geometry(TypedDict):
    type : Literal['Polygon']
    coordinates: list[PointList]

class MutliGeometry(TypedDict):
    type : Literal['MultiPolygon']
    coordinates: list[list[PointList]]

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
            if geo['type'] == 'Polygon':
                coords = geo['coordinates'][0]
                points = [pix.Float2(v[0], v[1]) for v in coords]
                box = BBox.from_points(points)
                polys.append(points)
            else:
                
                for multi in geo['coordinates']:
                    coords = multi[0] 
                    points = [pix.Float2(v[0], v[1]) for v in coords]
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

scale = pix.Float2(5.3, -6.7) * 0.80
offset = pix.Float2(960 - 250, 500)

canvas.draw_color = 0x000050FF
for country in countries:
    #if country.name == "Lesotho":
    #    les = country
    for points in country.polygons:
        canvas.draw_color = 0x000050FF
        canvas.polygon([p * scale + offset for p in points])


guess = random.randrange(len(countries))
gc = countries[guess]

inside = None
last_result = "Take a guess!"
score = 0

COUNT = 30

questions = COUNT

hilight = None
hilight_time = 0

zoom = 2

while pix.run_loop():
    screen.clear()
    screen.draw_color = pix.color.WHITE
    screen.draw(canvas, size = canvas.size*zoom)

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

    xy = (pix.get_pointer() / zoom - offset) / scale 
    for country in countries:
        screen.line_width = 2
        #min = country.bbox[0] * scale #+ offset
        #max = country.bbox[1] * scale #+ offset
        #if xy.x > min.x and xy.x < max.x and xy.y > max.y and xy.y < min.y:
        for points in country.polygons:
            screen.draw_color = pix.color.BLACK
            if xy.inside_polygon(points):
                points2 = [(p * scale + offset) * zoom for p in points]
                screen.draw_color = pix.color.LIGHT_BLUE
                screen.polygon(points2)
                screen.draw_color = pix.color.WHITE
                screen.lines(points2)
                inside = country
            if hilight is not None and hilight.name == country.name:
                points2 = [p * scale * zoom + offset for p in points]
                screen.draw_color = pix.color.LIGHT_GREEN
                screen.polygon(points2)
                screen.draw_color = pix.color.WHITE
                screen.lines(points2)
                inside = country



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
