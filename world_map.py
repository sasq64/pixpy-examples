import sys
import pixpy as pix
import json
from collections.abc import Iterable
from dataclasses import dataclass

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

def bbox(points):
    max_x,max_y = sys.float_info.min, sys.float_info.min
    min_x,min_y = sys.float_info.max, sys.float_info.max 
    for p in points:
        if p.x < min_x : min_x = p.x
        if p.y < min_y : min_y = p.y
        if p.x > max_x : max_x = p.x
        if p.y > max_y : max_y = p.y
    return (pix.Float2(min_x, min_y), pix.Float2(max_x, max_y))

def read_geo() -> list[Country]:
    countries : list[Country] = []
    with open('data/geo.json') as f:
        data = json.load(f)
        for f in data['features']:
            t = f['geometry']['type']
            multi = t != "Polygon"
            coords = f['geometry']['coordinates']
            polys = []
            box = []
            for c in coords:
                if multi:
                    c2 = c[0]
                else:
                    c2 = c
                points = [pix.Float2(v[0], v[1]) for v in c2]
                box += bbox(points)
                polys.append(points)
            country = Country()
            country.bbox = bbox(box)
            country.polygons = polys
            props = f['properties']
            country.name = props['name']
            country.iso2 = props['iso_a2_eh']
            country.pos = pix.Float2(props['label_x'], props['label_y'])

            countries.append(country)
    return countries

screen = pix.open_display(width=1920, height=1080, full_screen=True)
canvas = pix.Image(size = screen.size)

font = pix.load_font('data/hyperspace_bold.ttf')
countries = read_geo()

scale = pix.Float2(5.3, -6.7)
offset = pix.Float2(960, 600)

canvas.draw_color = 0x000050ff
for country in countries:
    for points in country.polygons:
        canvas.draw_color = 0x000050ff
        canvas.polygon([p * scale + offset for p in points])
    #img = pix.Font.UNSCII_FONT.make_image(country.iso2, 16)
    #canvas.draw_color = 0xffa0a0ff
    #canvas.draw(img, country.pos * scale + offset)

while pix.run_loop():
    screen.clear()
    screen.draw_color = pix.color.WHITE
    screen.draw(canvas)
    xy = pix.get_pointer()
    for country in countries:
        screen.line_width = 2

        for points in country.polygons: 
            min = country.bbox[0] * scale + offset
            max = country.bbox[1] * scale + offset
            if xy.x > min.x and xy.x < max.x and xy.y > max.y and xy.y < min.y: 
                screen.draw_color = pix.color.BLACK
                points2 = [p * scale + offset for p in points]
                if xy.inside_polygon(points2):
                    screen.draw_color = pix.color.LIGHT_BLUE
                    screen.polygon(points2)
                    screen.draw_color = pix.color.WHITE
                    screen.lines(points2)
                    img = font.make_image(country.name, 48, 0x8080e0ff)
                    screen.draw(img, top_left=(10,10))

    screen.swap()
