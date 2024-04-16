import pixpy as pix

def main():
    screen = pix.open_display(width=1280, height=720)
    con = pix.Console(cols=1280//16, rows=720//32)

    con.write('What is your name?\n')
    con.read_line()
    while pix.run_loop():
        for e in pix.all_events():
            if isinstance(e, pix.event.Text):
                con.write(f"\nHello {e.text}")
                con.read_line()

        screen.draw(drawable=con, top_left=(0,0), size=screen.size)
        screen.swap()

main()

