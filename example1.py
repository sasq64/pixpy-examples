import pixpy as pix

screen = pix.open_display(width=1280, height=720)
screen.filled_circle(center=(640,360), radius=100)
