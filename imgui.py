import pixpy as pix
from typing import TypeVar, Generic, Optional, Type
from types import TracebackType
from collections.abc import Callable

Float2 = pix.Float2
Int2 = pix.Int2

T = TypeVar('T')

class Cache(Generic[T]):
    """Object cache; Dictionary with creator function."""

    def __init__(self, fn: Callable[[], T] | None = None):
        self.data : dict[str, T] = {}
        self.constructor = fn

    def put(self, id: str, data: T):
        """Put value into cache."""
        self.data[id] = data

    def get_default(self, id: str, fn: Callable[[], T]) -> T:
        """Get cached object if contained in cache, otherwise call `fn()` to create it."""
        try:
            return self.data[id]
        except KeyError:
            self.data[id] = d = fn()
            return d

    def get(self, id: str) -> T:
        """Get cached object, create if it doesn't exist."""
        try:
            return self.data[id]
        except KeyError:
            if self.constructor != None:
                self.data[id] = d = self.constructor()
                return d
            raise


class UIContext:
    """A context for placing imgui components."""

    def __init__(self, offset: Float2, edge: Float2, target: pix.Context):
        self.offset = offset
        """Where to place the next component."""

        self.edge = edge
        """Position of right and bottom border."""

        self.target = target
        self.max_width: float = 0
        self.max_height: float = 0

    def layout_next(self, size: Float2):
        if self.offset.x + size.x > self.edge.x:
            self.offset = Float2(0, self.offset.y + self.max_height)
            self.max_height = 0

        if size.y > self.max_height:
            self.max_height = size.y
        self.offset += (size.x, 0)
    
    def layout_size(self, size: Float2):
        return size

    def inside(self, xy: Float2):
        return xy > self.offset and xy < self.edge


class Font:

    def __init__(self, file_name: str, size: int):
        self.font = pix.load_font(file_name)
        self.size = size
        self.texts = Cache[pix.Image]()

    def make_image(self, text: str):
        return self.font.make_image(text, self.size)


default_font = Font("data/Impact.ttf", 16)
large_font = Font("data/Impact.ttf", 24)

stack : list[UIContext] = []
"""The UI context stack. The top value is will be used by any UI creation functions."""

def push_context():
    s = stack[-1]
    stack.append(UIContext(s.offset, s.edge, s.target.copy()))
    return stack[-1]

def pop_context():
    stack.pop()

def button(text: str, size : Float2 = Float2.ZERO): 
    top = stack[-1]
    pos = top.offset
    img = default_font.make_image(text)

    size = top.layout_size(size)

    xy = pix.get_pointer()
    margin = Float2(5,5)
    if size == Float2.ZERO:
        size = img.size + margin * 2
    top.layout_next(size)
    inside = xy > pos and xy < (size + pos)
    
    ctx = top.target
    ctx.draw_color = pix.color.GREY
    if pix.is_pressed(pix.key.LEFT_MOUSE) and inside:
        ctx.draw_color = pix.color.LIGHT_GREY
    ctx.filled_rect(top_left=pos, size=size)
    ctx.draw_color = pix.color.WHITE
    ctx.draw(img, top_left=pos + margin)
    return inside and pix.was_released(pix.key.LEFT_MOUSE)



class TileGrid:
    """A component displaying a grid of images using a `pix.Console`."""

    def __init__(self, images: list[pix.Image], size: Int2):
        self.con = pix.Console(cols = size.x, rows = size.y, tile_size=images[0].size)
        self.selected : int = 0
        self.saved: int = 0
        self.dragging : Float2 | None = None
        self.offset = Float2.ZERO

        for i,tile in enumerate(images):
            self.con.get_image_for(i).copy_from(tile)
        pos = Int2.ZERO
        for i in range(len(images)):
            self.con.put(pos, i)
            pos += (1,0)
            if pos.x >= self.con.grid_size.x:
                pos = (pos + (0,1)).with_x0

    def draw_cursor(self, target: pix.Context, pos: Float2):
        y = self.selected // self.con.grid_size.x
        x = self.selected % self.con.grid_size.x
        rec_pos = Float2(x, y) * self.con.tile_size + pos
        target.line_width = 2
        target.draw_color = pix.color.LIGHT_RED
        target.rect(rec_pos - (4,4), self.con.tile_size + (8,8))
        target.draw_color = pix.color.WHITE
        target.rect(rec_pos - (2,2), self.con.tile_size + (4,4))

grids = Cache[TileGrid]()

def grid(id: str, images: list[pix.Image], size: Int2):
    """Create a TileGrid component."""

    g = grids.get_default(id, lambda : TileGrid(images, size))
    pixel_size = g.con.grid_size * g.con.tile_size
    top = stack[-1]
    pos = top.offset + g.offset
    target = top.target
    target.draw(g.con, top_left=pos, size=pixel_size)

    g.draw_cursor(target, pos)

    xy = pix.get_pointer()
    if g.dragging and pix.is_pressed(pix.key.LEFT_MOUSE):
        delta = xy - g.dragging
        g.dragging = xy
        g.offset += delta
    else:
        g.dragging = None

    inside = top.inside(xy) 
    if inside:
        g.saved = g.selected
        if pix.was_pressed(pix.key.LEFT_MOUSE):
            g.dragging = xy
            p = ((xy-pos) / g.con.tile_size).toi()
            g.selected = p.y * g.con.grid_size.x + p.x
        if pix.was_pressed(pix.key.RIGHT):
            g.selected += 1
        elif pix.was_pressed(pix.key.LEFT):
            g.selected -= 1
        elif pix.was_pressed(pix.key.UP):
            g.selected -= g.con.grid_size.x
        elif pix.was_pressed(pix.key.DOWN):
            g.selected += g.con.grid_size.y
        if g.selected < 0:
            g.selected = g.saved


class Selectable:
    index = 0

state = Cache[Selectable](Selectable) 


def text_list(id: str, lines: list[str] ):

    pos = stack[-1].offset
    target = stack[-1].target
    
    s = state.get(id)
    xy = pix.get_pointer()
    max_len = Float2.ZERO
    for i,line in enumerate(lines):
        img = large_font.make_image(line)
        if img.size.x > max_len.x:
            max_len = Float2(img.size.x, max_len.y)
        if img.size.y > max_len.y:
            max_len = Float2(max_len.x, img.size.y)
        target.draw_color = pix.color.WHITE if s.index == i else pix.color.GREY
        target.draw(img, top_left=pos)
        if pix.was_pressed(pix.key.LEFT_MOUSE) and xy > pos and xy < (pos + img.size):
            s.index = i
        pos += (0, img.size.y)
    stack[-1].layout_next(max_len)


class Window:
    def __init__(self, text: str, pos: Float2 = Float2.ZERO):
        self.pos = pos 
        self.size = Float2(320, 240)
        self.move_pos = Float2.ZERO
        self.moving = False
        self.title_img = default_font.make_image(text)

    def __enter__(self):
        pass

    def __exit__(self, et: Optional[Type[BaseException]], ei: Optional[BaseException],
                 ett: Optional[TracebackType]) -> bool:
        target = stack[-1].target
        target.draw_color = pix.color.BLUE
        target.filled_rect(self.pos, size=(self.size.x, 32))
        target.draw_color = pix.color.WHITE
        target.draw(self.title_img, top_left=self.pos + (8,8))
        target.line_width = 1
        target.rect(self.pos, size=self.size)
        pop_context()
        return True

def begin(width: int = -1):
    c = push_context()
    if width > 0:
        c.edge = Float2(c.offset.x + width, c.edge.y)


def end():
    #offset = stack[-1].offset
    max_w = stack[-1].max_width
    pop_context()
    stack[-1].offset += (max_w, 0)

windows = Cache[Window]()

def begin_window(text : str) -> Window:
    win = windows.get_default(text, lambda: Window(text, stack[-1].offset))
    stack[-1].layout_next(win.size)

    c = push_context()
    c.offset = win.pos + (2, 34)
    c.edge = win.pos + win.size
    c.target.clip_top_left = win.pos.toi()
    c.target.clip_size = win.size.toi()

    xy = pix.get_pointer()
    m = Float2(10,10)
    md = get_mouse_delta()
    inside_titlebar = xy > win.pos and xy < (win.pos + (win.size.x, 32))
    if inside_titlebar:
        if pix.was_pressed(pix.key.LEFT_MOUSE):
            win.move_pos = win.pos - xy
            win.moving = True
    xy -= md
    in_resize = xy > c.edge - m and xy < c.edge + m
    if in_resize:
        if pix.is_pressed(pix.key.LEFT_MOUSE):
            win.size += md

    if win.moving and pix.is_pressed(pix.key.LEFT_MOUSE):
        win.pos = win.move_pos + xy
    else:
        win.moving = False
    return win

def end_window():
    pop_context()

mouse_xy = Float2.ZERO
mouse_delta = Float2.ZERO

def start(context: pix.Context):
    global stack, mouse_xy, mouse_delta
    xy = pix.get_pointer()
    mouse_delta = xy - mouse_xy
    mouse_xy = xy
    stack = [UIContext(Float2.ZERO, Float2.ZERO, context)]

def get_mouse_delta():
    return mouse_delta