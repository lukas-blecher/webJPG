# pyinstaller
import os
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames, askdirectory
from pathlib import Path
import subprocess

_version = 0.1

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def get_last_path() -> Path:
    history = OUTPUT_PATH / ".hist"
    if history.exists():
        path = Path(history.open().read())
        if path.exists() and path.is_dir():
            return path
    return OUTPUT_PATH


def set_last_path(path: Path):
    history = OUTPUT_PATH / ".hist"
    with history.open("w") as f:
        f.write(str(path.resolve()))


NAMES = []


def open_file():
    names = askopenfilenames(
        initialdir=get_last_path(),
        filetypes=(("Bilder", ["*.png", "*.jpeg", "*.jpg"]), ("Alle Dateien", "*.*")),
        title="Bilder auswählen",
    )
    if len(names) > 0:
        set_last_path(Path(names[0]).parent)
    global NAMES
    NAMES.extend(list(names))

    entry_1.delete("1.0", END)
    entry_1.insert(END, "\n".join(NAMES))
    return names


OUTPUT_DIR = None


def dest_dir():
    global OUTPUT_DIR
    OUTPUT_DIR = Path(
        askdirectory(initialdir=get_last_path(), title="Speicherort auswählen")
    ).resolve()


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
        resp = messagebox.askokcancel("Speicherort", "Kein Speicherordner ausgewählt.\nIn '%s' speichern" % str(pos_dir))
        if resp:
            OUTPUT_DIR = pos_dir
        else:
            return
    args = "-strip -interlace Plane -gaussian-blur 0.05 -quality 85% -sampling-factor 4:2:0 -adaptive-resize 448 -colorspace sRGB".split(
        " "
    )
    os.chdir(OUTPUT_PATH)
    if len(files) == 0:
        messagebox.showinfo("Info", "Kein Bild ausgewählt")
        return

    for i, f in enumerate(set(files)):
        out = OUTPUT_DIR / Path(f).name
        if out.exists():
            out = out.parent / (out.stem + "_web" + out.suffix)
        out = out.parent / (out.stem + ".jpg")
        subp = subprocess.Popen(["convert", f, *args, str(out)])
        subp.communicate()

        progress["value"] = int((i + 1) / len(files) * 100)
        window.update_idletasks()
    NAMES = []
    entry_1.delete("1.0", END)


window = Tk()
window.wm_iconbitmap('logo.ico')
window.title("Bilder konvertieren")
window.geometry("475x320")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=284,
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
button_1.place(x=26.0, y=75.0, width=107.0, height=25.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=dest_dir,
    relief="flat",
)
button_2.place(x=341.0, y=75.0, width=107.0, height=25.0)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(238.0, 170.5, image=entry_image_1)
entry_1 = Text(bd=0, bg="#D9D9D9", highlightthickness=0)
entry_1.place(x=28.0, y=111.0, width=420.0, height=117.0)

canvas.create_text(
    28.0,
    15.0,
    anchor="nw",
    text="Bilder auswählen\nSpeicherort (Ordner) auswählen\nAuf 'Konvertieren' drücken",
    fill="#000",
    font=("None", int(10.0)),
)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=convert,
    relief="flat",
)
button_3.place(x=153.0, y=241.0, width=171.0, height=35.0)
progress = ttk.Progressbar(window, orient=HORIZONTAL, length=420, mode="determinate")
progress.pack(side="bottom", pady=10)
window.resizable(False, False)
window.mainloop()
