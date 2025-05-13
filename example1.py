import pixpy as pix

display = pix.open_display((1280,720))

display.filled_circle(center=(640,360), radius=100)

display.filled_rect(top_left=(10,10), size=(100,100))