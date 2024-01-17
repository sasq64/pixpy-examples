import pixpy as pix
import json

def read_geo():
    countries = {}
    with open('data/geo.json') as f:
        data = json.load(f)
        for f in data['features']:
            iso = f['properties']['name']
            t = f['geometry']['type']
            multi = t != "Polygon"
            coords = f['geometry']['coordinates']
            points = []
            for c in coords:
                if multi:
                    c2 = c[0]
                else:
                    c2 = c
                points.append([pix.Float2(v[0], v[1]) for v in c2])
            if iso in countries:
                countries[iso] = countries[iso] + points
            else:
                countries[iso] = points
    return countries


screen = pix.open_display(width=1920, height=1080, full_screen=True)
canvas = pix.Image(size = screen.size)

countries = read_geo()

scale = pix.Float2(5.3, -6.7)
offset = pix.Float2(960, 600)

canvas.draw_color = 0x000050ff
for (iso,all) in countries.items():
    for points in all: 
        points2 = [p * scale + offset for p in points]
        canvas.polygon(points2)

while pix.run_loop():
    screen.clear()
    screen.draw_color = pix.color.WHITE
    screen.draw(canvas)
    xy = pix.get_pointer()
    for (iso,all) in countries.items():
        screen.line_width = 2
        for points in all: 
            screen.draw_color = pix.color.BLACK
            points2 = [p * scale + offset for p in points]
            if pix.inside_polygon(points2, xy):
                screen.draw_color = pix.color.LIGHT_BLUE
                screen.polygon(points2)
                screen.draw_color = pix.color.WHITE
                screen.lines(points2)
                img = pix.Font.UNSCII_FONT.make_image(iso, 32)
                screen.draw(img)

    screen.swap()
