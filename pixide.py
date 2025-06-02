import os.path
#import traceback
from pathlib import Path
import pixpy as pix
from editor import TextEdit
import jedi # type: ignore
from jedi.api import Completion # type: ignore

class ListBox:
    def __init__(self):
        self.con = pix.Console(20, 10, font_file="data/Hack.ttf", font_size=32)
        self.xy = pix.Int2(0,0)
        self.selected = 0
        self.selected_name = ""

    def set_lines(self, lines: list[str]):
        self.lines = lines
        self.update()

    def set_pos(self, xy: pix.Int2):
        self.xy = xy

    def update(self):
        self.con.clear()
        pos = pix.Int2(0,0)
        self.con.set_color(pix.color.WHITE, pix.color.BLACK)
        for i,line in enumerate(self.lines):
            self.con.cursor_pos = pos
            if line == self.selected_name:
                self.selected = i
                self.con.set_color(pix.color.WHITE, pix.color.BLUE)
            else:
                self.con.set_color(pix.color.WHITE, pix.color.BLACK)
            self.con.write(line)
            pos += (0,1)
    
    def move(self, dy: int):
        self.selected += dy
        if self.selected < 0:
            self.selected = 0
        if self.selected >= len(self.lines):
            self.selected = len(self.lines)-1
        self.selected_name = self.lines[self.selected]
        self.update()

    def render(self, screen: pix.Screen):
        screen.context.draw_color = 0xffffffff
        screen.filled_rect(top_left=self.xy, size=self.con.size + (8,8))
        screen.draw(self.con, top_left = self.xy + (4,4))
    
    def get_selection(self) -> str:
        return self.selected_name


def info_box(text: str):

    lines = text.split("\n")
    maxl = len(max(lines, key=lambda i: len(i)))

    sz = pix.Int2(maxl, len(lines))
    con = pix.Console(cols = sz.x, rows = sz.y + 1)
    con.write(text)
    psz = sz * (8,16) + (8,8)
    xy = screen.size - psz 
    screen.context.draw_color = 0x000040ff
    screen.filled_rect(top_left=xy, size=psz)
    screen.draw(con, top_left = xy + (4,4))

def run(source: str):
    screen.clear(0x2020a0ff)
    screen.swap()
    try:
        exec(source)
        info_box("[PRESS ANY KEY]")
    except SyntaxError as se:
        screen.swap()
        info_box(f"Syntax error in line {se.lineno}")
    except Exception as e:
        screen.swap()
        info_box(str(e))

    screen.swap()
    leave = False
    while pix.run_loop() and not leave:
        events = pix.all_events()
        for e in events:
            if isinstance(e, pix.event.Key):
                leave = True

def main():
    global screen
    screen = pix.open_display(width=80 * 8 * 2, height=25 * 16 * 2)
    con = pix.Console(80, 25, font_file="data/Hack.ttf", font_size=28)

    title = pix.Console(80, 1, font_file="data/Hack.ttf", font_size=28)
    title.set_color(pix.color.DARK_GREY, pix.color.LIGHT_BLUE)
    title.clear()
    title.write("example.py")

    comp =  ListBox()
    comp_enabled = False

    edit = TextEdit(con)
    edit.set_color(0xffffffff, 0x4040e0ff)
    workFile = Path.home() / '.pixwork.py'
    if os.path.isfile(workFile):
        with open(workFile) as f:
            if f.readable() :
                text = f.read()
                edit.set_text(text)

    result: list[Completion] = []
    while pix.run_loop():
        events = pix.all_events()
        keep : list[pix.event.AnyEvent] = []
        for e in events:
            print(e)
            if isinstance(e, pix.event.Key):
                if e.key == pix.key.TAB:
                    x,y = edit.get_location()
                    if x > 0 and edit.get_char(x-1) != ' ':
                        script = jedi.Script(edit.get_text(), path=workFile)
                        result = script.complete(line=y+1, column=x) # type: ignore
                        comp.set_lines(list([str(res.name) for res in result]))
                        comp_enabled = True
                    else:
                        keep.append(e)
                elif e.key == pix.key.F5:
                    text = edit.get_text()
                    with open(Path.home() / '.pixwork.py', 'w') as f:
                        f.write(text)
                    run(edit.get_text())
                elif (e.key == pix.key.UP or e.key == pix.key.DOWN) and comp_enabled:
                    comp.move(-1 if e.key == pix.key.UP else 1)
                elif e.key == pix.key.ENTER and comp_enabled:
                    comp_enabled = False
                    res = result[comp.selected]
                    i = res.get_completion_prefix_length()
                    edit.insert(res.name[i:])
                else:
                    keep.append(e)
            elif comp_enabled and isinstance(e, pix.event.Text):
                x,y = edit.get_location()
                if x > 0 and edit.get_char(x-1) != ' ':
                    script = jedi.Script(edit.get_text(), path=workFile)
                    result = script.complete(line=y+1, column=x) # type: ignore
                    comp.set_lines(list([str(res.name) for res in result]))
                    comp_enabled = True
                keep.append(e)
            else:
                keep.append(e)
        comp.set_pos(con.cursor_pos * con.tile_size)
        edit.update(keep)
        edit.render()
        screen.clear(pix.color.DARK_GREY)
        screen.draw(con, top_left=(0, con.tile_size.y), size=con.size)
        screen.draw(title, size=title.size)
        if comp_enabled:
            comp.render(screen)

        screen.swap()

if __name__ == "__main__":
    main()
