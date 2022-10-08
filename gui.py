'''
   Copyright 2022 Lukas Blecher

   Licensed under the ImageMagick License (the "License"); you may not use
   this file except in compliance with the License.  You may obtain a copy
   of the License at

     https://imagemagick.org/script/license.php

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
   License for the specific language governing permissions and limitations
   under the License.
'''

import json
import os
import re
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames, askdirectory
from pathlib import Path
import subprocess

_version = 0.4
MIN_SIZE = 448
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
history = Path(os.getenv("APPDATA")) / "webjpg" / ".hist"
if not history.exists():
    history.parent.mkdir(exist_ok=True)


def get_last_path(key: str) -> Path:
    if history.exists():
        try:
            hist = json.load(history.open())
            if key in hist:
                path = Path(hist[key])
            elif len(hist) > 0:
                path = Path(next(iter(hist.values())))
            else:
                path = Path.home()
            if path.exists() and path.is_dir():
                return path
        except json.decoder.JSONDecodeError:
            pass
    return Path.home()


def set_last_path(key: str, path: Path):
    print(key, path)
    try:
        hist = json.load(history.open())
    except json.decoder.JSONDecodeError:
        hist = {}
    with history.open("w") as f:
        hist[key] = str(path.resolve())
        f.write(json.dumps(hist))


NAMES = []


def open_file():
    names = askopenfilenames(
        initialdir=get_last_path("img"),
        filetypes=(("Bilder", ["*.png", "*.jpeg", "*.jpg"]), ("Alle Dateien", "*.*")),
        title="Bilder auswählen",
    )
    if len(names) > 0:
        set_last_path("img", Path(names[0]).parent)
    global NAMES
    NAMES.extend(list(names))

    entry_1.delete("1.0", END)
    entry_1.insert(END, "\n".join(NAMES))
    return names


OUTPUT_DIR = None


def dest_dir():
    global OUTPUT_DIR
    out = askdirectory(initialdir=get_last_path("save"), title="Speicherort auswählen")
    if out:
        OUTPUT_DIR = Path(out).resolve()
        set_last_path("save", OUTPUT_DIR)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def convert(files=None):
    global NAMES, OUTPUT_DIR
    if files is None:
        files = NAMES
    if isinstance(files, Path):
        files = Path(files)
    if OUTPUT_DIR is None:
        pos_dir = Path(files[0]).resolve().parent
        resp = messagebox.askokcancel(
            "Speicherort",
            "Kein Speicherordner ausgewählt.\nIn '%s' speichern" % str(pos_dir),
        )
        if resp:
            OUTPUT_DIR = pos_dir
        else:
            return
    args = "-strip -interlace Plane -gaussian-blur 0.05 -quality 85% -sampling-factor 4:2:0 -adaptive-resize {MIN_SIZE} -colorspace sRGB".format(
        MIN_SIZE=MIN_SIZE
    ).split(
        " "
    )
    os.chdir(str(OUTPUT_PATH))
    if len(files) == 0:
        messagebox.showinfo("Info", "Kein Bild ausgewählt")
        return
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    for i, f in enumerate(set(files)):
        out = OUTPUT_DIR / Path(f).name
        if out.exists():
            out = out.parent / (out.stem + "_web" + out.suffix)
        out = out.parent / (out.stem + ".jpg")
        subp = subprocess.Popen(
            ["convert", f, *args, str(out)], shell=False, startupinfo=startupinfo
        )
        subp.communicate()

        progress["value"] = int((i + 1) / len(files) * 100)
        window.update_idletasks()
    NAMES = []
    entry_1.delete("1.0", END)


window = Tk()
window.wm_iconbitmap("assets/logo.ico")
window.title("Bilder konvertieren - webJPG v" + str(_version))
window.geometry("475x300")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=265,
    width=475,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_file,
    relief="flat",
)
button_1.place(x=26.0, y=57.0, width=107.0, height=25.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=dest_dir,
    relief="flat",
)
button_2.place(x=341.0, y=57.0, width=107.0, height=25.0)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(238.0, 152.5, image=entry_image_1)
entry_1 = Text(bd=0, bg="#D9D9D9", highlightthickness=0)
entry_1.place(x=28.0, y=93.0, width=420.0, height=117.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=convert,
    relief="flat",
)
button_3.place(x=153.0, y=223.0, width=171.0, height=35.0)

canvas.create_text(
    177.0,
    22.0,
    anchor="nw",
    text="Maximale Bildgröße (px)",
    fill="#000",
    font=("None", int(10.0)),
)


var = StringVar(value=str(MIN_SIZE))


def is_type_int(*args):
    item = var.get()
    var.set(re.sub(r"\D", "", item))
    item = var.get()
    if item:
        global MIN_SIZE
        MIN_SIZE = int(item)


entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(394.5, 34.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#D9D9D9", highlightthickness=0, textvariable=var)

var.trace("w", is_type_int)
entry_2.place(x=341.0, y=22.0, width=107.0, height=22.0)
progress = ttk.Progressbar(window, orient=HORIZONTAL, length=420, mode="determinate")
progress.pack(side="bottom", pady=10)
window.resizable(False, False)
window.mainloop()
