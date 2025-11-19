from tkinter import *
from PIL import Image, ImageTk


# This are the descriptions for the games
descriptions = {
    "Hollow Knight: Silksong": "A fast-paced action platformer starring Hornet.\nExplore Pharloom, master new abilities, and uncover the kingdom’s mysteries.",
    "HADES II": "A rogue-like dungeon crawler. Battle through the Underworld as Melinoë on a quest to defeat Chronos.",
    "DONKEY KONG BANANZA": "A jungle adventure with classic Donkey Kong platforming.\nCollect bananas, dodge enemies, and save your friends.",
    "KINGDOM COME DELIVERANCE II": "A historically accurate medieval RPG.\nFollow Henry’s story, make choices, and survive realistic combat.",
    "DEATH STRANDING 2: ON THE BEACH": "A cinematic narrative adventure by Hideo Kojima.\nReconnect a fractured world and uncover new mysteries.",
    "CLAIR OBSCUR: EXPEDITION 33": "A turn-based RPG with breathtaking painterly visuals.\nDefy fate in the world of Clair Obscur.",
}

# Other slide with the game stuff
def open_game_scene(image_path, game_title):
    scene = Toplevel(root)
    scene.title(game_title)
    scene.geometry("1500x1000")
    scene.configure(bg="#2b2b2b")

    # Loads the image
    original = Image.open(image_path)
    resized = original.resize((650, 450))
    img = ImageTk.PhotoImage(resized)

    # Image on the left
    img_label = Label(scene, image=img, bg="#2b2b2b")
    img_label.image = img
    img_label.pack(side=LEFT, padx=20, pady=20)

    # This thing get's the spesific game description. if no description  presents dev text
    game_desc = descriptions.get(game_title, "No description or not a game selected.")

    # Description text placed on the right
    info = Label(
        scene,
        text=f"{game_title}\n\n{game_desc}",
        justify=LEFT,
        font=("Arial", 14),
        bg="#2b2b2b",
        fg="white"
    )
    info.pack(side=LEFT, padx=20)

# The main seen
root = Tk()
root.title("Game Selector")
root.geometry("1500x1000")
root.configure(bg="#2b2b2b")

# The setting button on the top left of the thing
settings_button = Menubutton(root, text="Settings", relief=RAISED)
settings_button.menu = Menu(settings_button, tearoff=0)

settings_button["menu"] = settings_button.menu

settings_button.menu.add_command(label="Help")
settings_button.menu.add_command(label="Credits")
settings_button.menu.add_command(label="More")
settings_button.menu.add_command(label="Dance")
settings_button.menu.add_separator()
settings_button.menu.add_command(label="Exit", command=root.quit)

settings_button.place(x=10, y=10)

# Big text / titel
title_label = Label(root, text="GAMES", font=("Arial", 32), bg="#2b2b2b", fg="white")
title_label.pack(pady=20)

# Sides for buttond
button_frame = Frame(root, bg="#2b2b2b")
button_frame.pack(pady=20)

# List of games
games = [
    ("silksong.jpg", "Hollow Knight: Silksong"),
    ("Hades_2.JPEG", "HADES II"),
    ("donkey-kong-bananza.jpg", "DONKEY KONG BANANZA"),
    ("kingdom-come-deliverance-ii.jpg", "KINGDOM COME DELIVERANCE II"),
    ("DEATH_STRANDING_2_image.jpg", "DEATH STRANDING 2: ON THE BEACH"),
    ("CO-EXP33-mobile-header.jpg", "CLAIR OBSCUR: EXPEDITION 33"),
]

# Big buttons for games be like
for img_path, title in games:

    try:
        original = Image.open(img_path)
        resized = original.resize((150, 150))
        button_img = ImageTk.PhotoImage(resized)
    except:
        placeholder = Image.new("RGB", (150,150), color="gray")
        button_img = ImageTk.PhotoImage(placeholder)

    btn = Button(
        button_frame,
        image=button_img,
        command=lambda p=img_path, t=title: open_game_scene(p, t),
        bg="#2b2b2b",
        borderwidth=2,
        highlightthickness=0
    )

    btn.image = button_img
    btn.pack(side=LEFT, padx=10)

root.mainloop()

