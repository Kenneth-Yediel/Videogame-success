from tkinter import *
from PIL import Image, ImageTk

# This are the descriptions for the games
descriptions = {
    "Dragon Age: Inquisition": "A massive fantasy RPG where you lead the Inquisition\nand seal the Breach across Thedas.",
    "Middle-earth: Shadow of Mordor": "A combat-focused open-world adventure set in Middle-earth\nwith the iconic Nemesis system.",
    "Bayonetta 2": "A stylish, fast-paced action game starring the witch Bayonetta\nfighting angelic and demonic threats.",
    "The Witcher 3: Wild Hunt": "A giant open-world RPG following Geralt of Rivia\nthrough monster hunts and political intrigue.",
    "Bloodborne": "A gothic horror action RPG set in Yharnam.\nFast combat, nightmarish enemies, deep lore.",
    "Fallout 4": "A post-apocalyptic RPG with base building,\nopen-world exploration, and story-driven quests.",
    "Overwatch": "A team-based hero shooter featuring unique abilities,\ncooperative strategies, and fast-paced matches.",
    "Uncharted 4: A Thief's End": "A cinematic action adventure with Nathan Drake\non a treasure hunt full of danger and secrets.",
    "Doom": "A brutal, fast first-person shooter\nfocused on demon slaying and heavy metal energy.",
    "The Legend of Zelda: Breath of the Wild": "An open-world Zelda game with exploration, physics,\nand total freedom in a massive kingdom.",
    "Horizon Zero Dawn": "A post-post-apocalyptic world filled with robot creatures\nand a mystery surrounding Aloy's past.",
    "Persona 5": "A stylish JRPG about teenagers living double lives\nas Phantom Thieves who reform corrupted adults.",
    "God of War": "A reimagining of the series where Kratos journeys\nthrough Norse mythology with his son Atreus.",
    "Red Dead Redemption 2": "A cinematic Western open-world story about Arthur Morgan\nand the fading age of outlaws.",
    "Marvel's Spider-Man": "A fast and fluid open-world superhero game\nfeaturing Peter Parker’s battles across New York City.",
    "Sekiro: Shadows Die Twice": "A precise, challenging action game set in Sengoku-era Japan\nfocused on sword combat and stealth.",
    "Death Stranding": "A unique strand-type game where you reconnect America\nwhile avoiding supernatural threats.",
    "Control": "A supernatural action-adventure about Jesse Faden\nexploring the strange and shifting Oldest House.",
    "The Last of Us Part II": "A story-driven survival experience about revenge,\npain, and the consequences of violence.",
    "Ghost of Tsushima": "A samurai open-world game set during the Mongol invasion,\nfilled with beautiful landscapes and duels.",
    "Hades": "A rogue-like action game where Zagreus tries to escape the Underworld\nwith fast-paced combat and great storytelling.",
    "It Takes Two": "A co-op adventure built entirely around cooperation\nwith creative level design and humor.",
    "Ratchet & Clank: Rift Apart": "A dimension-shifting action platformer\nwith impressive visuals and chaotic weaponry.",
    "Resident Evil Village": "A first-person survival horror adventure\nfacing mutated creatures in an isolated village.",
    "Elden Ring": "An open-world Souls-like designed with George R.R. Martin,\nfeaturing challenging bosses and deep lore.",
    "God of War Ragnarok": "Kratos and Atreus travel across the realms\nas Ragnarok approaches in Norse mythology.",
    "Horizon Forbidden West": "Aloy explores new lands and fights advanced machines\nin a beautiful open-world world.",
    "Baldur's Gate 3": "A massive D&D party-based RPG\nwith choices, companions, and reactive storytelling.",
    "The Legend of Zelda: Tears of the Kingdom": "A sequel expanding the world of Hyrule\nwith sky islands, new abilities, and deep creativity.",
    "Alan Wake 2": "A psychological survival horror story\nmixing dual narratives, mystery, and atmosphere."
}

# Other slide with the game stuff
def open_game_scene(image_path, game_title):
    scene = Toplevel(root)
    scene.title(game_title)
    scene.geometry("1500x1000")
    scene.configure(bg="#555555")

    # This is a return button to go back to the main menu
    return_button = Button(scene, text="Return to Main Menu", font=("Arial", 14), command=open_start_screen)
    return_button.pack(pady=10)

    # Loads the image
    original = Image.open(image_path)
    resized = original.copy()
    resized.thumbnail((650, 450))
    img = ImageTk.PhotoImage(resized)

    # Image on the left
    img_label = Label(scene, image=img, bg="#555555")
    img_label.image = img
    img_label.pack(side=LEFT, padx=20, pady=20)

    # This thing get's the spesific game description. if no description  presents dev text
    game_desc = descriptions.get(game_title, "No description or not a game selected\n or something went wrong.")

    # Description text placed on the right
    info = Label(
        scene,
        text=f"{game_title}\n\n{game_desc}",
        justify=LEFT,
        font=("Arial", 14),
        bg="#555555",
        fg="white"
    )
    info.pack(side=LEFT, padx=20)


# This opens the main game selection screen
def open_videogames_screen():
    for widget in root.winfo_children():
        widget.destroy()

    # Background image added
    bg = PhotoImage(file="video_gamesbackground.png")
    background_label = Label(root, image=bg)
    background_label.image = bg
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # The setting button on the top left
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

    # This is a return button to go back to the main menu
    return_button = Button(root, text="Return to Main Menu", font=("Arial", 14), command=open_start_screen)
    return_button.pack(pady=10)

    # Big text / title
    title_label = Label(root, text="GAMES", font=("Arial", 32), bg="#555555", fg="white")
    title_label.pack(pady=20)

    # Scroll container
    scroll_container = Frame(root, bg="#555555")
    scroll_container.pack()

    canvas = Canvas(scroll_container, width=1000, height=600, bg="#555555", highlightthickness=0)
    canvas.pack(side=LEFT)

    scroll_slider = Scale(
        scroll_container,
        from_=0,
        to=500,
        orient=VERTICAL,
        bg="#222222",
        fg="white",
        length=600
    )
    scroll_slider.pack(side=RIGHT, padx=10)

    button_frame = Frame(canvas, bg="#555555")
    canvas.create_window((0, 0), window=button_frame, anchor="nw")

    def update_scroll(pos):
        canvas.yview_moveto(int(pos) / 1000)

    scroll_slider.config(command=update_scroll)

    # List of games
    games = [
        ("Dragon_Age.jpg", "Dragon Age: Inquisition"),
        ("Middle-earth.jpg", "Middle-earth: Shadow of Mordor"),
        ("Bayonetta2.jpg", "Bayonetta 2"),
        ("TheWitcher3.png", "The Witcher 3: Wild Hunt"),
        ("Bloodborne.jpg", "Bloodborne"),
        ("Fallout 4.jpg", "Fallout 4"),
        ("Overwatch.jpg", "Overwatch"),
        ("Uncharted 4.jpg", "Uncharted 4: A Thief's End"),
        ("Doom.png", "Doom"),
        ("The Legen.jpeg", "The Legend of Zelda: Breath of the Wild"),
        ("Horizon.jpg", "Horizon Zero Dawn"),
        ("Persona 5.jpg", "Persona 5"),
        ("God of War.jpg", "God of War"),
        ("Red Dead Redemption 2.jpg", "Red Dead Redemption 2"),
        ("Marvel's Spider-Man.jpg", "Marvel's Spider-Man"),
        ("SekiroShadows Die Twice.jpg", "Sekiro: Shadows Die Twice"),
        ("Death Stranding.jpg", "Death Stranding"),
        ("Control.jpg", "Control"),
        ("The Last of Us Part II.jpg", "The Last of Us Part II"),
        ("Ghost of Tsushima.jpg", "Ghost of Tsushima"),
        ("Hades.jpg", "Hades"),
        ("It Takes Two.jpg", "It Takes Two"),
        ("Ratchet & Clank.jpeg", "Ratchet & Clank: Rift Apart"),
        ("Resident Evil Village.jpg", "Resident Evil Village"),
        ("Elden Ring.jpg", "Elden Ring"),
        ("God of War Ragnarok.jpg", "God of War Ragnarok"),
        ("Horizon Forbidden West.jpg", "Horizon Forbidden West"),
        ("Baldur's Gate 3.jpg", "Baldur's Gate 3"),
        ("The Legend of Zelda Tears.jpg", "The Legend of Zelda: Tears of the Kingdom"),
        ("Alan Wake 2.jpeg", "Alan Wake 2")
    ]

    # Control of the games presented
    columns = 5
    row = 0
    col = 0

    # Big buttons for games
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
            bg="#555555",
            borderwidth=2,
            highlightthickness=0
        )
        btn.image = button_img
        btn.grid(row=row, column=col, padx=20, pady=20)

        col += 1
        if col >= columns:
            col = 0
            row += 1

    # Update scroll region
    button_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# This is the starting area (the first screen)
def open_start_screen():
    for widget in root.winfo_children():
        widget.destroy()

    # Background image added
    bg = PhotoImage(file="YES.png")
    background_label = Label(root, image=bg)
    background_label.image = bg
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # The setting button on the top left
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

    # Big text / title
    start_title = Label(root, text="Videogame success", font=("Arial", 40), bg="#555555", fg="white")
    start_title.pack(pady=80)

    # The 3 starting buttons
    start_frame = Frame(root, bg="#555555")
    start_frame.pack(pady=20)

    # First button: Videogames
    btn_games = Button(
        start_frame,
        text="Videogames",
        font=("Arial", 20),
        width=20,
        command=open_videogames_screen
    )
    btn_games.pack(pady=10)

    # Second button: videogame predictor
    btn_predictor = Button(
        start_frame,
        text="Videogame Predictor",
        font=("Arial", 20),
        width=20
        # Coming soon
    )
    btn_predictor.pack(pady=10)

    # The third button: exit
    btn_exit = Button(
        start_frame,
        text="Exit",
        font=("Arial", 20),
        width=20,
        command=root.quit
    )
    btn_exit.pack(pady=10)


# The main scene
root = Tk()
root.title("Game Selector")
root.geometry("1500x1000")
root.configure(bg="#555555")

# Open the start screen first
open_start_screen()

root.mainloop()