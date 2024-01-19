import os
import struct
import pixpy as pix

screen = pix.open_display(width=1280, height=860)
tile_size = pix.Float2(16,16)

con = pix.Console(cols=256, rows=48, tile_size=tile_size)
tiles = pix.load_png("data/mono_tiles.png").split(size=tile_size)
for i, tile in enumerate(tiles):
    con.get_image_for(1024 + i).copy_from(tile)

if os.path.exists("data/tiles.dat"):
    with open("data/tiles.dat", "rb") as f:
        data = f.read()
        unpacked = list(struct.unpack(f'{len(data) // 4}I', data))
        con.set_tiles(unpacked)

con.put((10,10), 1025)
offset = pix.Float2(0,0)

while pix.run_loop():
    screen.clear(pix.color.BLUE)
    con.render(screen.context, offset, con.grid_size * tile_size * 2)
    offset -= (1,0)
    screen.swap()
