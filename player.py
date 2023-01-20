import pixpy as pix
import musix
import pyaudio
import sys

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                output=True)

musix.init()
player = musix.load(sys.argv[1])
screen = pix.open_display(width=60*16, height=20*32)

con = pix.Console(font_file = 'data/Hack.ttf', font_size=16, rows=60, cols=60)
title = player.get_meta("title")
con.write(f"PLAYING: {title}")

while pix.run_loop():
    sz = stream.get_write_available()
    if sz > 0:
        samples = player.render(sz * 2)
        stream.write(samples)

    screen.draw(con)
    screen.swap()

