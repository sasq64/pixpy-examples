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

font = pix.load_font('data/hyperspace_bold.ttf')
countries = read_geo()

scale = pix.Float2(5.3, -6.7)
offset = pix.Float2(960, 600)

canvas.draw_color = 0x000050ff
boxes = {}
for (iso,all) in countries.items():
    max_x,max_y = -10000, -10000
    min_x,min_y = 10000, 10000
    for points in all:
        for p in points:
            if p.x < min_x : min_x = p.x
            if p.y < min_y : min_y = p.y
            if p.x > max_x : max_x = p.x
            if p.y > max_y : max_y = p.y
        points2 = [p * scale + offset for p in points]
        canvas.draw_color = 0x000050ff
        canvas.polygon(points2)
    min,max = pix.Float2(min_x, min_y), pix.Float2(max_x, max_y)
    boxes[iso] = [min, max]

while pix.run_loop():
    screen.clear()
    screen.draw_color = pix.color.WHITE
    screen.draw(canvas)
    xy = pix.get_pointer()
    for (iso,all) in countries.items():
        screen.line_width = 2
        box = boxes[iso]
        for points in all: 
            min = box[0] * scale + offset
            max = box[1] * scale + offset
            if xy.x > min.x and xy.x < max.x and xy.y > max.y and xy.y < min.y: 
                screen.draw_color = pix.color.BLACK
                points2 = [p * scale + offset for p in points]
                if xy.inside_polygon(points2):
                    screen.draw_color = pix.color.LIGHT_BLUE
                    screen.polygon(points2)
                    screen.draw_color = pix.color.WHITE
                    screen.lines(points2)
                    img = font.make_image(iso, 48, 0x8080e0ff)
                    screen.draw(img, top_left=(10,10))

    screen.swap()
