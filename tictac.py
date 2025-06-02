import pixpy as pix

Float2 = pix.Float2


def cross(context: pix.Canvas, xy: Float2, r: float):
    context.line(xy - (r, r), xy + (r, r))
    context.line(xy + (r, -r), xy + (-r, r))


def check_win(d: list[int]):
    p = d[4]
    if p != 0:
        if (
            (d[0] == p == d[8])
            or (d[1] == p == d[7])
            or (d[2] == p == d[6])
            or (d[3] == p == d[5])
        ):
            return p
    p = d[0]
    if p != 0:
        if (p == d[3] == d[6]) or (p == d[1] == d[2]):
            return p
    p = d[8]
    if p != 0:
        if (p == d[7] == d[6]) or (p == d[5] == d[2]):
            return p
    return 0


class Board:
    @property
    def won(self):
        return self.check() != 0

    def __init__(self, pos: Float2, size: Float2):
        self.pos = pos
        self.data: list[int] = [0] * 9
        self.context = screen.context
        self.size = size

    def click(self, pos: Float2, player: int):
        pos -= self.pos
        pos /= self.size / 3
        if pos.x < 0 or pos.y < 0:
            return -1
        x = int(pos.x)
        y = int(pos.y)
        if x < 3 and y < 3:
            i = x + 3 * y
            if self.data[i] == 0:
                self.data[i] = player + 1
                return i
        return -1

    def check(self):
        return check_win(self.data)

    def line(self, p0: Float2 | tuple[float, float], p1: Float2 | tuple[float, float]):
        self.context.line(self.pos + p0, self.pos + p1)

    def render(self):
        sz = self.size / 3
        self.context.draw_color = pix.color.GREEN
        self.line((sz.x, 0), (sz.x, self.size.y))
        self.line((sz.x * 2, 0), (sz.x * 2, self.size.y))
        self.line((0, sz.y), (self.size.x, sz.y))
        self.line((0, sz.y * 2), (self.size.x, sz.y * 2))
        for i, x in enumerate(self.data):
            xy = Float2(i % 3, i // 3) * sz + self.pos
            r = sz.x / 2 - 4
            if x == 2:
                self.context.circle(center=xy + sz / 2, radius=r)
            elif x == 1:
                cross(self.context, xy + sz / 2, r)


class TicTac:
    def __init__(self, context: pix.Canvas):
        self.context = context
        self.boards: list[Board] = []
        self.board_size = Float2(150, 150)
        self.m = Float2(50, 30)

        self.wins = [0] * 9
        self.winner = 0

        for i in range(9):
            xy = Float2(i % 3, i // 3) * (self.board_size + self.m) + (100, 100)
            self.boards.append(Board(xy, self.board_size))

        screen.line_width = 3

        self.player = 0
        self.font = pix.load_font("data/hyperspace_bold.ttf", 32)

        self.legal = -1

    def update(self):
        if pix.was_pressed(pix.key.LEFT_MOUSE):
            mp = pix.get_pointer()
            for i, board in enumerate(self.boards):
                p = board.check()
                if (self.legal == -1 or self.legal == i) and p == 0:
                    next = board.click(mp, self.player)
                    if next >= 0:
                        self.legal = next
                        if self.boards[next].won:
                            self.legal = -1
                        self.player ^= 1
                        self.wins[i] = board.check()
                        self.winner = check_win(self.wins)

    def render(self):
        ctx = self.context

        if self.winner != 0:
            mark = "X" if self.winner == 1 else "O"
            img = self.font.make_image(f"PLAYER {mark} HAS WON!", 32, pix.color.WHITE)
            ctx.draw_color = pix.color.LIGHT_BLUE
            ctx.draw(img, top_left=(10, 10))
            self.legal = -2
        else:
            mark = "X" if self.player == 0 else "O"
            img = self.font.make_image(f"PLAYER {mark}", 32, pix.color.WHITE)
            ctx.draw_color = pix.color.YELLOW
            ctx.draw(img, top_left=(10, 10))

        for i, board in enumerate(self.boards):
            ctx.draw_color = pix.color.GREEN
            board.render()
            xy = board.pos
            if self.legal == i:
                ctx.draw_color = pix.color.WHITE
                ctx.rect(top_left=xy - self.m / 2, size=self.board_size + self.m)
            p = board.check()
            if p == 1:
                ctx.draw_color = pix.color.LIGHT_RED
                ctx.line_width = 8
                cross(ctx, xy + self.board_size / 2, self.board_size.x / 2 - 5)
                ctx.line_width = 2
            elif p == 2:
                ctx.draw_color = pix.color.LIGHT_RED
                ctx.line_width = 8
                ctx.circle(xy + self.board_size / 2, self.board_size.x / 2 - 5)
                ctx.line_width = 2

        if self.legal == -1:
            ctx.draw_color = pix.color.WHITE
            ctx.rect(
                top_left=Float2(100, 100) - self.m / 2,
                size=(self.board_size + self.m) * 3,
            )


####

screen = pix.open_display(width=1280, height=720)
game = TicTac(screen.context)

while pix.run_loop():
    screen.clear()
    game.update()
    game.render()
    screen.swap()
