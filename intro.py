
import webbrowser
import urllib.request
import zipfile
from pathlib import Path
home = str(Path.home())

import pixpy as pix

def download_and_unzip(url: str):
    global con,screen
    con.write(f"Fetching:\n`{url}`...\n")
    screen.draw(con, top_left = m, size=screen.size - m * 2)
    screen.swap()
    fh, _ = urllib.request.urlretrieve(url)
    zf = zipfile.ZipFile(fh, 'r')
    #first_file = zip_file_object.namelist()[0]
    home = Path.home()
    con.write(f"Extracting to {home / 'pix'}\n")
    screen.draw(con, top_left = m, size=screen.size - m * 2)
    screen.swap()
    zf.extractall(home / "pix")
    con.write(f"Done!")
    screen.draw(con, top_left = m, size=screen.size - m * 2)
    screen.swap()
    #file = zip_file_object.open(first_file)
    #content = file.read()


vscode = 'https://code.visualstudio.com/download'
readme = 'https://github.com/sasq64/pix/blob/main/README.md'

screen = pix.open_display(size=(1280, 720))
canvas = pix.Image(size=screen.size)

m = pix.Float2(20,20)
con = pix.Console(60, 35)
con.write("[1] Getting started\n[2] Watch demo\n[3] Download examples\n[4] Start editor\n")
while pix.run_loop():
    if pix.was_pressed('1'):
        webbrowser.open(readme)
    if pix.was_pressed('2'):
        webbrowser.open(vscode)
    if pix.was_pressed('3'):
        download_and_unzip('https://github.com/sasq64/pixpy-examples/archive/refs/tags/release-1.zip')
    #screen.draw(canvas)
    screen.clear(pix.color.LIGHT_GREEN)
    screen.draw(con, top_left = m, size=screen.size - m * 2)
    screen.swap()
