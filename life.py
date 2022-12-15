import random
import pixpy as pix


def main():
    screen = pix.open_display(width=1280, height=720)
    con = pix.Console(cols=160, rows=90)
    cols = con.grid_size.x
    rows = con.grid_size.y
    con.set_color(pix.color.YELLOW, pix.color.BLACK)

    counts = [0] * (cols * rows + cols + 1)
    board = [0] * (cols * rows + cols + 1)

    def reset():
        for y in range(rows):
            for x in range(cols):
                board[x + y * cols] = random.randrange(0, 2) == 0
                con.put((x, y), ord('●' if board[x + y * cols] else ' '))

    def step():
        for i in range(cols * rows):
            counts[i] = board[i-1] + board[i+1] + board[i + cols - 1] + \
                board[i + cols] + board[i + cols + 1] + board[i - cols - 1] + \
                board[i - cols] + board[i - cols + 1]
        for y in range(rows):
            for x in range(cols):
                i = x + y * cols
                count = counts[i]
                if not board[i] and count == 3:
                    con.put((x, y), ord('●'))
                    board[i] = 1
                elif board[i] and (count < 2 or count > 3):
                    con.put((x, y), ord(' '))
                    board[i] = 0

    reset()
    while pix.run_loop():
        for e in pix.all_events():
            if isinstance(e, pix.event.Text):
                reset()
        step()
        screen.draw(drawable=con, size=screen.size)
        screen.swap()


main()

