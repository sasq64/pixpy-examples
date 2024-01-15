#!/usr/bin/env python3

import pixpy as pix
import musix
import pyaudio
import sys

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                frames_per_buffer=1024,
                rate=44100,
                output=True)

musix.init()

name = "data/propaganda.sid"
if len(sys.argv) > 1:
    name = sys.argv[1]

player = musix.load(name)
screen = pix.open_display(width=50*8, height=10*16)
con = pix.Console(rows=10, cols=50)

positions = {
    "title": (12,1),
    "game": (12,1),
    "composer": (12,2),
    "copyright": (12,3),
    "length": (12,5),
    "song": (26,5),
    "songs": (29,5),
    "format": (35,5),
}

song = 0
songs = 0
info_text = None
info_pos = 0
con.set_color(fg = pix.color.YELLOW, bg = pix.color.BLACK)
con.write("\n TITLE:\n COMPOSER:\n COPYRIGHT:\n\n TIME:00:00/00:00 -- SONG:00/00 -- ")
con.set_color(fg = pix.color.GREEN, bg = pix.color.BLACK)
def handle_meta(meta_list: list[str]):
    global song, songs, info_text, info_pos
    con.cursor_pos = (0,0)
    for meta in meta_list:
        val = player.get_meta(meta)
        print(f"{meta} = {val}")
        if meta == "sub_title" or meta == "comment" or meta == "message":
            msg = str(val).replace('\n', ' ')
            info_text = pix.Font.UNSCII_FONT.make_image(text=msg, size=16)
            info_pos = screen.width
        if meta in positions:
            pos = positions[meta]
            con.cursor_pos = pos
            if meta == "length": 
                len = int(val)
                con.write(f"{(len//60):02}:{(len%60):02}") 
            elif meta == "song":
                song = int(val)
                con.write(f"{(song+1):02}") 
            elif meta == "songs":
                songs = int(val)
                con.write(f"{songs:02}") 
            else:
                con.write(f"{val}") 
player.on_meta(handle_meta)

seconds = 0
print(f"{song} / {songs}")
while pix.run_loop():
    if pix.was_pressed(pix.key.LEFT) and song > 0:
        song -= 1
        player.seek(song)
    elif pix.was_pressed(pix.key.RIGHT) and song < songs:
        song += 1
        player.seek(song)
    sz = stream.get_write_available()
    if sz > 0:
        samples = player.render(sz * 2)
        seconds += (len(samples) / (44100*4))
        con.cursor_pos = (6,5)
        secs = int(seconds)
        con.write(f"{(secs//60):02}:{(secs%60):02}")
        stream.write(samples)

    screen.draw(con, size = screen.size)
    if info_text:
        screen.draw_color = pix.color.GREY
        screen.draw(image=info_text, top_left=(info_pos * 3.2 / 3 - 10, 99), size=info_text.size * 3.2)
        screen.draw_color = pix.color.WHITE
        screen.draw(image=info_text, top_left=(info_pos, 100), size=info_text.size * 3)
        info_pos -= 4
    screen.swap()

