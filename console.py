import pixpy as pix
screen = pix.open_display(width=60*16, height=20*32)

con = pix.Console(font_file = 'data/Hack.ttf', font_size=16, rows=60, cols=60)
con.write('Hello\nThis is the Hack font instead\nof the normal font.')
screen.draw(con)

