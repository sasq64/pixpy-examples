import pixpy as pix

screen = pix.open_display((640, 480))

tiles = pix.load_png("data/ANTOR1.png").split((32, 32))

tile_map = pix.TileSet(tile_size=tiles[0].size)
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.:,?! "

for (img, c) in zip(tiles, chars):
    tile_map.get_image_for(c).copy_from(img)

pos = screen.size - (0, 40)
screen.fps = 0
while pix.run_loop():
    screen.clear()
    tile_map.render_text(screen, "HELLO OLD SCHOOL DEMO SCROLLER WORLD!", pos)
    pos -= (screen.delta * 120, 0)
    screen.swap()
