import pixpy as pix
Float2 = pix.Float2
 
""" HELP
 First thing: we open a display so we have somwhere to draw. Notice that
 all 2D points are single arguments, we avoid splitting them up into
 `x` and `y` or `width` and `height`
"""
screen = pix.open_display(size=(800,600))

""" HELP
Here we load an image to be used as background.
"""
bg = pix.load_png("data/background.png") 

""" HELP
Here we load another image. The image contains a set of
'sprites' layed out from left to right. You can click on the
image (in the data/ folder) to see what it looks like.
"""
img = pix.load_png("data/invaders.png")

"""HELP
Here we "split" the image into parts. We know that the image
contains 8 by 2 "tiles" where each tile contains the image of
a single sprite. So after this operation, we will end up with
a list of images, where each image is 32x32 pixels in size.

Note that nothing happens to the original image. In fact, all
the images in the `sprites` list are views into the orignal image.
"""
sprites = img.split(cols=8, rows=2)

"""HELP
The "sprite sheet" contains more sprites than we need at the moment,
we will use the first 6 sprites as enemies, and sprite number 14 as
the player sprite.
"""
enemies = sprites[0:6]
player = sprites[13]

pos = Float2(400, 552)
enemy_offset = Float2(100,100)
while pix.run_loop():
    screen.draw(image=bg)
    for e in enemies:
        screen.draw(image=e, center=e.pos * 2 + enemy_offset, size=e.size * 2)
    screen.draw(image=player, top_left=pos, size=player.size*2)
    if pix.is_pressed(pix.key.LEFT):
        pos -= (2, 0)
    elif pix.is_pressed(pix.key.RIGHT):
        pos += (2, 0)
    screen.swap()