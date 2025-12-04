# Controller.py - Handles events and connects View with Model
from GOTY_View import GameView
#from GOTY_Model import RandomForestStrategy
#from Graph_maker import *
from tkinter import *
from PIL import Image, ImageTk
# Create a controller class for the GUI
class GameController:
    def __init__(self, root):
# Link controller to root window and create view
        self.root = root
        self.view = GameView(root)
# Descriptions for each game displayed in the detail window
        self.descriptions = {
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
            "Marvel's Spider-Man": "A fast and fluid open-world superhero game\nfeaturing Peter Parker's battles across New York City.",
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
# List of all games with associated image files
        self.games = [
            ("Training_fotos/Dragon_Age.jpg", "Dragon Age: Inquisition"),
            ("Training_fotos/Middle-earth.jpg", "Middle-earth: Shadow of Mordor"),
            ("Training_fotos/Bayonetta2.jpg", "Bayonetta 2"),
            ("Training_fotos/TheWitcher3.png", "The Witcher 3: Wild Hunt"),
            ("Training_fotos/Bloodborne.jpg", "Bloodborne"),
            ("Training_fotos/Fallout 4.jpg", "Fallout 4"),
            ("Training_fotos/Overwatch.jpg", "Overwatch"),
            ("Training_fotos/Uncharted 4.jpg", "Uncharted 4: A Thief's End"),
            ("Training_fotos/Doom.png", "Doom"),
            ("Training_fotos/The Legen.jpeg", "The Legend of Zelda: Breath of the Wild"),
            ("Training_fotos/Horizon.jpg", "Horizon Zero Dawn"),
            ("Training_fotos/Persona 5.jpg", "Persona 5"),
            ("Training_fotos/God of War.jpg", "God of War"),
            ("Training_fotos/Red Dead Redemption 2.jpg", "Red Dead Redemption 2"),
            ("Training_fotos/Marvel's Spider-Man.jpg", "Marvel's Spider-Man"),
            ("Training_fotos/SekiroShadows Die Twice.jpg", "Sekiro: Shadows Die Twice"),
            ("Training_fotos/Death Stranding.jpg", "Death Stranding"),
            ("Training_fotos/Control.jpg", "Control"),
            ("Training_fotos/The Last of Us Part II.jpg", "The Last of Us Part II"),
            ("Training_fotos/Ghost of Tsushima.jpg", "Ghost of Tsushima"),
            ("Training_fotos/Hades.jpg", "Hades"),
            ("Training_fotos/It Takes Two.jpg", "It Takes Two"),
            ("Training_fotos/Ratchet & Clank.jpeg", "Ratchet & Clank: Rift Apart"),
            ("Training_fotos/Resident Evil Village.jpg", "Resident Evil Village"),
            ("Training_fotos/Elden Ring.jpg", "Elden Ring"),
            ("Training_fotos/God of War Ragnarok.jpg", "God of War Ragnarok"),
            ("Training_fotos/Horizon Forbidden West.jpg", "Horizon Forbidden West"),
            ("Training_fotos/Baldur's Gate 3.jpg", "Baldur's Gate 3"),
            ("Training_fotos/The Legend of Zelda Tears.jpg", "The Legend of Zelda: Tears of the Kingdom"),
            ("Training_fotos/Alan Wake 2.jpeg", "Alan Wake 2")
        ]
# Open the first screen when the program starts
        self.open_start_screen()
# Opens the predictor screen with three options
    def open_predictor_screen(self):
# Clear previous widgets
        self.view.clear_screen()
        # Set background image
        self.view.create_background("Back_ground_and_other_stuff/YES.png")
        # --- Settings menu windows (Help, Credits, More, Dance) ---
        def open_help_window():
            win = Toplevel(self.root)
            win.title("Help")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="HELP", font=("Arial", 24), fg="white", bg="#444444").pack(pady=20)
            message = """Use the buttons to see the predictor.\nSingle Predictor: Predict success for one game.\nAll Predictions: See all game predictions.\nGraphs: Visualize data and results."""
            Label(win, text=message, font=("Arial", 14), fg="white", bg="#444444", justify=LEFT).pack(pady=10)
        def open_credits_window():
            win = Toplevel(self.root)
            win.title("Credits")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="CREDITS", font=("Arial", 24), fg="white", bg="#444444").pack(pady=20)
            Label(win, text="Created by Jomuel, Chris, and Kenneth \nMade with Python + Tkinter + .....",
                  font=("Arial", 14), fg="white", bg="#444444").pack(pady=10)
        def open_more_window():
            win = Toplevel(self.root)
            win.title("More")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="MORE", font=("Arial", 24), fg="white", bg="#444444").pack(pady=20)
            message = """What else do you want. there is no more.\n im just bored"""
            Label(win, text=message, font=("Arial", 14), fg="white", bg="#444444", justify=LEFT).pack(pady=10)
        def open_dance_window():
            win = Toplevel(self.root)
            win.title("Dance")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="DANCE TIME!", font=("Arial", 24), fg="white", bg="#444444").pack(pady=10)
# Load dance image
            try:
                img_path = "Back_ground_and_other_stuff/skeleton-dance.jpg"
                original = Image.open(img_path)
                resized = original.copy()
                resized.thumbnail((500, 300))
                img = ImageTk.PhotoImage(resized)
            except:
                placeholder = Image.new("RGB", (500, 300), color="gray")
                img = ImageTk.PhotoImage(placeholder)
            img_label = Label(win, image=img, bg="#444444")
            img_label.image = img
            img_label.pack(pady=20)
# Create settings dropdown menu
        settings_button = Menubutton(self.root, text="Settings", relief=RAISED)
        settings_button.menu = Menu(settings_button, tearoff=0)
        settings_button["menu"] = settings_button.menu
        settings_button.menu.add_command(label="Help", command=open_help_window)
        settings_button.menu.add_command(label="Credits", command=open_credits_window)
        settings_button.menu.add_command(label="More", command=open_more_window)
        settings_button.menu.add_command(label="Dance", command=open_dance_window)
        settings_button.menu.add_separator()
        settings_button.menu.add_command(label="Exit", command=self.root.quit)
        settings_button.place(x=10, y=10)
# Return to main menu button
        return_button = Button(self.root, text="Return to Main Menu", font=("Arial", 14),
                               command=self.open_start_screen)
        return_button.pack(pady=10)
# Big text / title for predictor screen
        title_label = Label(self.root, text="Videogame Predictor", font=("Arial", 32), bg="#555555", fg="white")
        title_label.pack(pady=40)
# Frame for images (above buttons)
        image_frame = Frame(self.root, bg="#555555")
        image_frame.pack(pady=20)
# Load and display images for each button
# Single Predictor image
        try:
            original1 = Image.open("Back_ground_and_other_stuff/single_predictor.jpg")
            resized1 = original1.resize((200, 150))
            img1 = ImageTk.PhotoImage(resized1)
            img_label1 = Label(image_frame, image=img1, bg="#555555")
            img_label1.image = img1
            img_label1.grid(row=0, column=0, padx=50)
        except:
# If image not found, create placeholder
            placeholder1 = Image.new("RGB", (200, 150), "#252525")
            img1 = ImageTk.PhotoImage(placeholder1)
            img_label1 = Label(image_frame, image=img1, bg="#555555")
            img_label1.image = img1
            img_label1.grid(row=0, column=0, padx=50)
# All Predictions image
        try:
            original2 = Image.open("Back_ground_and_other_stuff/all_predictions.jpg")
            resized2 = original2.resize((200, 150))
            img2 = ImageTk.PhotoImage(resized2)
            img_label2 = Label(image_frame, image=img2, bg="#555555")
            img_label2.image = img2
            img_label2.grid(row=0, column=1, padx=50)
        except:
            placeholder2 = Image.new("RGB", (200, 150), "#252525")
            img2 = ImageTk.PhotoImage(placeholder2)
            img_label2 = Label(image_frame, image=img2, bg="#555555")
            img_label2.image = img2
            img_label2.grid(row=0, column=1, padx=50)
# Graphs image
        try:
            original3 = Image.open("Back_ground_and_other_stuff/graphs.jpg")
            resized3 = original3.resize((200, 150))
            img3 = ImageTk.PhotoImage(resized3)
            img_label3 = Label(image_frame, image=img3, bg="#555555")
            img_label3.image = img3
            img_label3.grid(row=0, column=2, padx=50)
        except:
            placeholder3 = Image.new("RGB", (200, 150), "#252525")
            img3 = ImageTk.PhotoImage(placeholder3)
            img_label3 = Label(image_frame, image=img3, bg="#555555")
            img_label3.image = img3
            img_label3.grid(row=0, column=2, padx=50)
# Frame for buttons (horizontal layout)
        button_frame = Frame(self.root, bg="#555555")
        button_frame.pack(pady=20)
# Create the 3 predictor buttons horizontally
        btn_single = Button(
            button_frame,
            text="Single Predictor",
            font=("Arial", 18),
            width=15,
            height=2,
            command=self.open_single_predictor  # Will implement this function
        )
        btn_single.grid(row=0, column=0, padx=30)
        btn_all = Button(
            button_frame,
            text="All Predictions",
            font=("Arial", 18),
            width=15,
            height=2,
            command=self.open_all_predictions  # Will implement this function
        )
        btn_all.grid(row=0, column=1, padx=30)
        btn_graphs = Button(
            button_frame,
            text="Graphs",
            font=("Arial", 18),
            width=15,
            height=2,
            command=self.open_graphs_screen  # Will implement this function
        )
        btn_graphs.grid(row=0, column=2, padx=30)
# Placeholder functions for predictor screens (to be implemented)
    def open_single_predictor(self):
        # This will open the single game prediction interface
        print("Opening Single Predictor...")

#============
    def open_all_predictions(self):
        # This will show predictions for all games
        print("Opening All Predictions...")

        win = Toplevel()
        win.title("All Predictions")
        win.geometry("750x500")
        win.configure(bg="#252525")

        # TITLES
        titles_frame = Frame(win, bg="#252525")
        titles_frame.pack(pady=10)

        Label(
            titles_frame,
            text="Winner",
            font=("Arial", 20, "bold"),
            bg="#252525",
            fg="white",
            width=15
        ).pack(side=LEFT, padx=100)

        Label(
            titles_frame,
            text="Lossers",
            font=("Arial", 20, "bold"),
            bg="#252525",
            fg="white",
            width=15
        ).pack(side=RIGHT, padx=100)

        # Sliders frame
        sliders_frame = Frame(win, bg="#252525")
        sliders_frame.pack(pady=20)

        # Winner slider
        slider_left = Scale(
            sliders_frame,
            from_=0,
            to=100,
            orient=VERTICAL,
            bg="#222222",
            fg="white",
            length=350
        )
        slider_left.pack(side=LEFT, padx=80)

        # Losers slider
        slider_right = Scale(
            sliders_frame,
            from_=0,
            to=100,
            orient=VERTICAL,
            bg="#222222",
            fg="white",
            length=350
        )
        slider_right.pack(side=RIGHT, padx=80)


    #=====================


    def open_graphs_screen(self):
        # This will show data visualizations
        print("Opening Graphs...")
        # TODO: Implement graphs and visualizations
# Opens a window showing the selected game's details
    def open_game_scene(self, image_path, game_title):
        scene = Toplevel(self.root)
        scene.title(game_title)
        scene.geometry("1500x1000")
        scene.configure(bg="#555555")
# Return button to go back to the main menu
        return_button = Button(scene, text="Return to Main Menu", font=("Arial", 14), command=self.open_start_screen)
        return_button.pack(pady=10)
# Load the game’s image
        try:
            original = Image.open(image_path)
            resized = original.copy()
            resized.thumbnail((650, 450))
            img = ImageTk.PhotoImage(resized)
            img_label = Label(scene, image=img, bg="#555555")
            img_label.image = img  # prevent garbage collection
            img_label.pack(side=LEFT, padx=20, pady=20)
        except:
            pass  # If image fails, skip image display
# Load the corresponding description
        game_desc = self.descriptions.get(game_title,
                                          "No description or not a game selected\n or something went wrong.")
# Show info text
        info = Label(
            scene,
            text=f"{game_title}\n\n{game_desc}",
            justify=LEFT,
            font=("Arial", 14),
            bg="#555555",
            fg="white"
        )
        info.pack(side=LEFT, padx=20)
# Opens the menu showing all available video games
    def open_videogames_screen(self):
# Clear previous widgets
        self.view.clear_screen()
# Set background image
        self.view.create_background("Back_ground_and_other_stuff/video_gamesbackground.png")
# --- Settings menu windows (Help, Credits, More, Dance) ---
        def open_help_window():
            win = Toplevel(self.root)
            win.title("Help")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="HELP", font=("Arial", 24), fg="white", bg="#444444").pack(pady=20)
            Label(win, text="Browse the game list.\nClick images to open info.",
                  font=("Arial", 14), fg="white", bg="#444444", justify=LEFT).pack(pady=10)
        def open_credits_window():
            win = Toplevel(self.root)
            win.title("Credits")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="CREDITS", font=("Arial", 24), fg="white", bg="#444444").pack(pady=20)
            Label(win, text="Created by Jomuel, Chris, and Kenneth \nMade with Python + Tkinter + .....",
                  font=("Arial", 14), fg="white", bg="#444444").pack(pady=10)
        def open_more_window():
            win = Toplevel(self.root)
            win.title("More")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="MORE", font=("Arial", 24), fg="white", bg="#444444").pack(pady=20)
            Label(win, text="What elss do you want. there is no more.\n im just board",
                  font=("Arial", 14), fg="white", bg="#444444").pack(pady=10)
        def open_dance_window():
            win = Toplevel(self.root)
            win.title("Dance")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="DANCE TIME!", font=("Arial", 24), fg="white", bg="#444444").pack(pady=10)
# Load dance image
            try:
                img_path = "Back_ground_and_other_stuff/skeleton-dance.jpg"
                original = Image.open(img_path)
                resized = original.copy()
                resized.thumbnail((500, 300))
                img = ImageTk.PhotoImage(resized)
            except:
                placeholder = Image.new("RGB", (500, 300), color="gray")
                img = ImageTk.PhotoImage(placeholder)
            img_label = Label(win, image=img, bg="#444444")
            img_label.image = img
            img_label.pack(pady=20)
# Create settings dropdown menu
        settings_button = Menubutton(self.root, text="Settings", relief=RAISED)
        settings_button.menu = Menu(settings_button, tearoff=0)
        settings_button["menu"] = settings_button.menu
        settings_button.menu.add_command(label="Help", command=open_help_window)
        settings_button.menu.add_command(label="Credits", command=open_credits_window)
        settings_button.menu.add_command(label="More", command=open_more_window)
        settings_button.menu.add_command(label="Dance", command=open_dance_window)
        settings_button.menu.add_separator()
        settings_button.menu.add_command(label="Exit", command=self.root.quit)
        settings_button.place(x=10, y=10)
# Return to main menu button
        return_button = Button(self.root, text="Return to Main Menu", font=("Arial", 14),
                               command=self.open_start_screen)
        return_button.pack(pady=10)
# Title label for the screen
        title_label = Label(self.root, text="GAMES", font=("Arial", 32), bg="#555555", fg="white")
        title_label.pack(pady=20)
# Create scrollable container manually (canvas + scale)
        scroll_container = Frame(self.root, bg="#555555")
        scroll_container.pack()
        canvas = Canvas(scroll_container, width=1000, height=600, bg="#555555", highlightthickness=0)
        canvas.pack(side=LEFT)
# Vertical slider to control scroll
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
# Frame inside canvas where game buttons will be placed
        button_frame = Frame(canvas, bg="#555555")
        canvas.create_window((0, 0), window=button_frame, anchor="nw")
# Link slider movement to canvas scrolling
        def update_scroll(pos):
            canvas.yview_moveto(int(pos) / 1000)
        scroll_slider.config(command=update_scroll)

# Store references to images to prevent garbage collection
        self.game_images = []

# Layout game images in a grid (5 per row)
        columns = 5
        row = 0
        col = 0
        for img_path, title in self.games:
            # Load each game image safely
            try:
                original = Image.open(img_path)
                resized = original.resize((150, 150))
                button_img = ImageTk.PhotoImage(resized)
            except:
                placeholder = Image.new("RGB", (150, 150), color="gray")
                button_img = ImageTk.PhotoImage(placeholder)

            # Create clickable button that opens game detail window
            btn = Button(
                button_frame,
                image=button_img,
                command=lambda p=img_path, t=title: self.open_game_scene(p, t),
                bg="#555555",
                borderwidth=2,
                highlightthickness=0
            )
            btn.image = button_img  # prevent garbage collection
            btn.grid(row=row, column=col, padx=20, pady=20)

            # Keep a reference in the list
            self.game_images.append(button_img)

            # Move to next row/column in grid
            col += 1
            if col >= columns:
                col = 0
                row += 1

        # Update scroll area to match content size
        button_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

# Main start screen of the application
    def open_start_screen(self):
# Clear previous screen
        self.view.clear_screen()
# Background image
        self.view.create_background("Back_ground_and_other_stuff/YES.png")
# --- Settings menu pop-ups ---
        def open_help_window():
            win = Toplevel(self.root)
            win.title("Help")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="HELP", font=("Arial", 24), fg="white", bg="#444444").pack(pady=20)
            Label(
                win,
                text="Use the buttons to explore the app.\nVideogames opens the game selection screen.\nExit closes the program.",
                font=("Arial", 14), fg="white", bg="#444444", justify=LEFT
            ).pack(pady=10)
        def open_credits_window():
            win = Toplevel(self.root)
            win.title("Credits")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="CREDITS", font=("Arial", 24), fg="white", bg="#444444").pack(pady=20)
            Label(
                win,
                text="Created by Jomuel, Chris, and Kenneth \nMade with Python + Tkinter + .....",
                font=("Arial", 14), fg="white", bg="#444444"
            ).pack(pady=10)
        def open_more_window():
            win = Toplevel(self.root)
            win.title("More")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="MORE", font=("Arial", 24), fg="white", bg="#444444").pack(pady=20)
            Label(
                win,
                text="What else do you want. there is no more.\n im just bored",
                font=("Arial", 14), fg="white", bg="#444444"
            ).pack(pady=10)
        def open_dance_window():
            win = Toplevel(self.root)
            win.title("Dance")
            win.geometry("600x400")
            win.configure(bg="#444444")
            Label(win, text="DANCE TIME!", font=("Arial", 24), fg="white", bg="#444444").pack(pady=10)
            try:
                img_path = "Back_ground_and_other_stuff/skeleton-dance.jpg"
                original = Image.open(img_path)
                resized = original.copy()
                resized.thumbnail((500, 300))
                img = ImageTk.PhotoImage(resized)
            except:
                placeholder = Image.new("RGB", (500, 300), color="gray")
                img = ImageTk.PhotoImage(placeholder)
            img_label = Label(win, image=img, bg="#444444")
            img_label.image = img
            img_label.pack(pady=20)
# Settings icon in top-left corner
        settings_button = Menubutton(self.root, text="Settings", relief=RAISED)
        settings_button.menu = Menu(settings_button, tearoff=0)
        settings_button["menu"] = settings_button.menu
        settings_button.menu.add_command(label="Help", command=open_help_window)
        settings_button.menu.add_command(label="Credits", command=open_credits_window)
        settings_button.menu.add_command(label="More", command=open_more_window)
        settings_button.menu.add_command(label="Dance", command=open_dance_window)
        settings_button.menu.add_separator()
        settings_button.menu.add_command(label="Exit", command=self.root.quit)
        settings_button.place(x=10, y=10)
# Title text for start screen
        start_title = Label(self.root, text="Videogame success", font=("Arial", 40), bg="#555555", fg="white")
        start_title.pack(pady=80)
# Frame for the main action buttons
        start_frame = Frame(self.root, bg="#555555")
        start_frame.pack(pady=20)
# Go to videogame selection screen
        btn_games = Button(
            start_frame,
            text="GOTY Nominees(2005-2023)",
            font=("Arial", 20),
            width=23,
            command=self.open_videogames_screen
        )
        btn_games.pack(pady=10)
# Predictor button
        btn_predictor = Button(
            start_frame,
            text="Video game Predictor",
            font=("Arial", 20),
            width=20,
            command=self.open_predictor_screen
        )
        btn_predictor.pack(pady=10)
# Exit program
        btn_exit = Button(
            start_frame,
            text="Exit",
            font=("Arial", 20),
            width=20,
            command=self.root.quit
        )
        btn_exit.pack(pady=10)


# Starts Tkinter event loop
    def run(self):
        self.root.mainloop()