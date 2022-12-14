import pixpy as pix
from pixpy import event as evt


def main():
    screen = pix.open_display(width=1280, height=720)
    con = pix.Console(cols=80, rows=45)

    con.write('What is your name?\n')
    con.get_line()
    while pix.run_loop():
        match pix.get_event():
            case evt.Text(text):
                print(text)
                con.write(f"\nHello {text}")
                con.get_line()
            case _:
                pass

        screen.draw(drawable=con, top_left=(0,0), size=screen.size)
        screen.swap()

main()

