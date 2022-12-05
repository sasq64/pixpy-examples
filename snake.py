import pixpy as pix
from pixpy import Int2

screen = pix.open_display(width=640, height=480)

con = pix.Console()
pos = Int2(10, 10)
add = [Int2(1, 0), Int2(0, 1), Int2(-1, 0), Int2(0, -1)]

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
        if con.get(pos) != 0x20:
            break
        con.put(pos, ord('█'))

    con.render(screen.context, size=screen.size)
    screen.swap()

