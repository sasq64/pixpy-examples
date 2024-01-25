import pixpy as pix
import imgui

Float2 = pix.Float2
Int2 = pix.Int2

screen = pix.open_display(width=1280, height=720)


tiles = pix.load_png('data/sokoban_tilesheet.png').split((64,64))

while pix.run_loop():
    screen.clear()
    imgui.start(screen.context)
    
    with imgui.begin_window("Buttons"):
        if imgui.button("Click me"):
            print("CLICKED")
            pass

    imgui.text_list("x", [ "Hello", "Good bye", "Get away!"])

    with imgui.begin_window("Grid"):
        # A grid is a console displaying images that you can select.
        # You can pass all images in or use it as a scope w
        imgui.grid("g", tiles, Int2(10, 10))

    screen.swap()
