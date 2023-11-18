from pathlib import Path
import subprocess
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("600x388")
window.configure(bg="#1B1B1B")

canvas = Canvas(
    window,
    bg="#1B1B1B",
    height=388,
    width=600,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    62.0,
    239.0,
    249.0,
    266.0,
    fill="#242424",
    outline="")

canvas.create_rectangle(
    62.0,
    173.0,
    249.0,
    200.0,
    fill="#242424",
    outline="")

canvas.create_rectangle(
    62.0,
    289.0,
    249.0,
    316.0,
    fill="#242424",
    outline="")

canvas.create_rectangle(
    0.0,
    77.0,
    600.0,
    79.0,
    fill="#2C2C2C",
    outline="")

canvas.create_text(
    28.0,
    26.0,
    anchor="nw",
    text="SOLARIS",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 25 * -1)
)

canvas.create_text(
    142.0,
    32.0,
    anchor="nw",
    text="| Credentials",
    fill="#696969",
    font=("Inter Regular", 16 * -1)
)

# Add the "Prefix" label above the second textbox
canvas.create_text(
    62.0,
    207.0,
    anchor="nw",
    text="Prefix",
    fill="#696969",
    font=("Inter Regular", 16 * -1)
)

# Add the "Bot Token" label above the first textbox
canvas.create_text(
    62.0,
    147.0,
    anchor="nw",
    text="Token",
    fill="#696969",
    font=("Inter Regular", 16 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    86.5,
    186.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#242424",
    fg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=70.0,
    y=177.0,
    width=179.0,
    height=17.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    159.5,
    252.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#242424",
    fg="#FFFFFF",
    highlightthickness=0
)
entry_2.place(
    x=70.0,
    y=239.0,
    width=179.0,
    height=25.0
)

def run_bot_command():
    entry_1_text = entry_1.get()
    entry_2_text = entry_2.get()
    
    command = f"sudo python3 bot.py {entry_2_text} {entry_1_text}"
    
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the command: {e}")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=run_bot_command,
    relief="flat",
    bg="#242424",
    activebackground="#242424",
    disabledforeground="#242424"
)
button_1.place(
    x=70.0,
    y=294.0,
    width=73.0,
    height=16.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    470.0,
    206.0,
    image=image_image_1
)

photo = PhotoImage(file=relative_to_assets("Icon.png"))
window.title("Orion Client")
window.iconphoto(False, photo)
window.resizable(False, False)

window.mainloop()
