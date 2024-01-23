import pixpy as pix
from typing import Any, TypeVar, Generic
from collections.abc import Callable

Float2 = pix.Float2
Int2 = pix.Int2

T = TypeVar('T')

class Cache(Generic[T]):
    def __init__(self, fn: Callable[[], T] | None = None):
        self.data : dict[str, T] = {}
        self.constructor = fn

    def get_default(self, id: str, fn: Callable[[], T]) -> T:
        try:
            return self.data[id]
        except KeyError:
            self.data[id] = d = fn()
            return d

    def get(self, id: str) -> T:
        try:
            return self.data[id]
        except KeyError:
            if self.constructor != None:
                self.data[id] = d = self.constructor()
                return d
            raise
    pass

class UIContext:
    def __init__(self, offset: Float2, size: Float2, target: pix.Context):
        self.offset = offset
        self.target = target
        self.size = size

stack : list[UIContext] = []

texts = Cache[pix.Image]()

def push_context():
    s = stack[-1]
    stack.append(UIContext(s.offset, s.size, s.target.copy()))
    return stack[-1]

def pop_context():
    stack.pop()

def button(text, size : Float2 = Float2.ZERO): 
    top = stack[-1]
    pos = top.offset

    xy = pix.get_pointer()
    margin = Float2(5,5)
    img = texts.get_default(text, lambda: font.make_image(text, size=24))
    if size == Float2.ZERO:
        size = img.size + margin * 2
    print(size)
    top.offset += (size.x, 0)
    inside = xy > pos and xy < (size + pos)
    
    top.target.draw_color = pix.color.GREY
    if pix.is_pressed(pix.key.LEFT_MOUSE) and inside:
        top.target.draw_color = pix.color.LIGHT_GREY
    top.target.filled_rect(top_left=pos, size=size)
    top.target.draw_color = pix.color.WHITE
    top.target.draw(img, top_left=pos + margin)
    return inside and pix.was_released(pix.key.LEFT_MOUSE)



class TileGrid:
    con : pix.Console
    selected: int
    def __init__(self, images: list[pix.Image], size: Int2):
        self.con = pix.Console(cols = size.x, rows = size.y, tile_size=images[0].size)
        for i,tile in enumerate(images):
            self.con.get_image_for(i).copy_from(tile)
        pos = Int2.ZERO
        self.selected = 0
        for i in range(len(images)):
            self.con.put(pos, i)
            pos += (1,0)
            if pos.x >= self.con.grid_size.x:
                pos = (pos + (0,1)).with_x0

grids = Cache[TileGrid]()

def grid(id: str, images: list[pix.Image], pos: Float2, size: Int2):
    g = grids.get_default(id, lambda : TileGrid(images, size))
    pixel_size = g.con.grid_size * g.con.tile_size
    pos += stack[-1].offset
    target = stack[-1].target
    target.draw(g.con, top_left=pos, size=pixel_size)
    y = g.selected // g.con.grid_size.x
    x = g.selected % g.con.grid_size.x
    rpos = Float2(x, y) * g.con.tile_size + pos
    target.line_width = 2
    target.draw_color = pix.color.LIGHT_RED
    target.rect(rpos - (4,4), g.con.tile_size + (8,8))
    target.draw_color = pix.color.WHITE
    target.rect(rpos - (2,2), g.con.tile_size + (4,4))
    if pix.was_pressed(pix.key.LEFT_MOUSE):
        xy = pix.get_pointer()
        if xy > pos and xy < (pixel_size + pos):
            p = ((xy -pos) / g.con.tile_size).toi()
            g.selected = p.y * g.con.grid_size.x + p.x
    if pix.was_pressed(pix.key.RIGHT):
        xy = pix.get_pointer()
        if xy > pos and xy < (pixel_size + pos):
            g.selected += 1






class Selectable:
    index = 0

state = Cache[Selectable](Selectable) 

def text_list(id: str, lines: list[str] ):

    pos = stack[-1].offset
    target = stack[-1].target
    
    s = state.get(id)
    xy = pix.get_pointer()
    maxl = 0
    for i,line in enumerate(lines):
        img = font.make_image(line, size=24)
        if img.size.x > maxl:
            maxl = img.size.x
        target.draw_color = pix.color.WHITE if s.index == i else pix.color.GREY
        target.draw(img, top_left=pos)
        if pix.was_pressed(pix.key.LEFT_MOUSE) and xy > pos and xy < (pos + img.size):
            s.index = i
        pos += (0, img.size.y)
    stack[-1].offset += (maxl, 0)


class Window:
    def __init__(self, pos = Float2.ZERO):
        self.pos = pos 
        self.size = Float2(320, 240)
        self.move_pos = Float2.ZERO
        self.moving = False


windows = Cache[Window](Window)

def begin_window(id : str):
    win = windows.get_default(id, lambda: Window(stack[-1].offset))
    stack[-1].offset += (win.size.x, 0)
    stack[-1].target.draw_color = pix.color.WHITE
    stack[-1].target.rect(win.pos, size=win.size)
    stack[-1].target.draw_color = pix.color.BLUE
    stack[-1].target.filled_rect(win.pos, size=(win.size.x, 32))

    c = push_context()

    c.offset = win.pos
    c.target.clip_top_left = win.pos.toi()
    c.target.clip_size = win.size.toi()

    xy = pix.get_pointer()
    inside = xy > win.pos and xy < (win.pos + (win.size.x, 32))
    if inside:
        if pix.was_pressed(pix.key.LEFT_MOUSE):
            win.move_pos = win.pos - xy
            win.moving = True

    if win.moving and pix.is_pressed(pix.key.LEFT_MOUSE):
        win.pos = win.move_pos + xy
    else:
        win.moving = False

def end_window():
    pop_context()


screen = pix.open_display(width=1280, height=720)

font = pix.load_font("data/Impact.ttf")

tiles = pix.load_png('data/sokoban_tilesheet.png').split((64,64))

while pix.run_loop():
    stack = [UIContext(Float2.ZERO, Float2.ZERO, screen.context)]
    screen.clear()
    begin_window("Buttons")
    if button("Click me"):
        print("CLICKED")
        pass
    end_window()

    text_list("x", [ "Hello", "Good bye", "Get away!"])

    begin_window("Grid")
    grid("g", tiles, Float2.ZERO, Int2(10, 10))
    end_window()

    screen.swap()
