import pixpy as pix

def frame_fn():
    print("HEY")
    return True

screen = pix.open_display(width=60 * 16, height=20 * 32)

pix.run_every_frame(frame_fn)

con = pix.Console(font_file="data/Hack.ttf", font_size=16, rows=60, cols=60)
con.write("Hello\nThis is the Hack font instead\nof the normal font.")
screen.draw(con)
