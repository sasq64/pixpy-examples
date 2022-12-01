import pixpy as pix

screen = pix.open_display(width=640, height=480)

pos = screen.size / 2

font = pix.load_font("data/Impact.ttf")
hello_image = font.make_image("Hallå Världen!", size=32, color=pix.color.ORANGE)

screen.draw_color = pix.color.YELLOW
screen.line_width = 5.0

while pix.run_loop():
    screen.clear()
    screen.draw(image=hello_image, center=pos, rot=pos.x/100)
    screen.circle(center=pos, radius=pos.x/4)
    pos += (1, 0)
    screen.swap()
