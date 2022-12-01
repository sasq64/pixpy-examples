import pixpy as pix
Vec2 = pix.Vec2

screen = pix.open_display(width=640, height=480)

con = pix.Console()
pos = Vec2(10, 10)
add = [Vec2(1, 0), Vec2(0, 1), Vec2(-1, 0), Vec2(0, -1)]
direction = 0

while pix.run_loop():
    for e in pix.all_events():
        match e:
            case pix.event.Key(key):
                match key:
                    case pix.key.RIGHT:
                        direction = (direction + 1) % 4
                    case pix.key.LEFT:
                        direction = (direction + 3) % 4

    if screen.frame_counter % 10 == 0:
        pos += add[direction]
        if con.get(pos) != ' ':
            break
        con.put(pos, '█')

    con.render(screen.context, size=screen.size)
    screen.swap()

