# Controller.py - Handles events and connects View with Model
import csv
from datetime import datetime
import shutil
from tkinter import filedialog, messagebox
import numpy as np
import os
from GOTY_View import GameView
from GOTY_Model import randomF_Strat
from Graph_maker import (
    load_goty_csv,
    build_similarity_graph_from_df,
    GraphWindow
)
from tkinter import *
from PIL import Image, ImageTk
# Create a controller class for the GUI
class GameController:
    def _init_(self, root):
# Link controller to root window and create view
        self.root = root
        self.view = GameView(root)
        self.ml_model = randomF_Strat
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
# Exit button for ease of access
        exit_button = Button(self.root, text="Exit", font=("Arial", 14), command=self.root.quit)
        exit_button.pack(pady=10)
        exit_button.place(x=1445, y=10)
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
# Clear previous widgets
        self.view.clear_screen()
# Set background image
        self.view.create_background("Back_ground_and_other_stuff/YES.png")
# Title for predictor screen
        title_label = Label(self.root, text="Single Game Predictor", font=("Arial", 32, "bold"),
                            bg="#555555", fg="white")
        title_label.pack(pady=20)
# Frame for the entire content
        main_frame = Frame(self.root, bg="#555555")
        main_frame.pack(pady=20)
# RIGHT SIDE: Image upload and display
        right_frame = Frame(main_frame, bg="#555555", width=400)
        right_frame.pack(side=RIGHT, padx=50)
# Game image display
        self.game_image_label = Label(right_frame, text="Upload Game Image",
                                      bg="#444444", fg="white",
                                      width=30, height=15, font=("Arial", 12))
        self.game_image_label.pack(pady=10)
# Upload image button
        upload_btn = Button(right_frame, text="Upload Game Image",
                            font=("Arial", 14), bg="#4CAF50", fg="white",
                            command=self.uploadGameImage)
        upload_btn.pack(pady=10)
# Predict button
        predict_btn = Button(right_frame, text="PREDICT GOTY SUCCESS",
                             font=("Arial", 18, "bold"), bg="#2196F3", fg="white",
                             width=21, height=2, command=self.runPrediction)
        predict_btn.pack(pady=10)
# LEFT SIDE: Input fields
        left_frame = Frame(main_frame, bg="#555555", width=500)
        left_frame.pack(side=LEFT, padx=50)
# Game name
        Label(left_frame, text="Game Name:", font=("Arial", 14),
              bg="#555555", fg="white").pack(anchor="w", pady=(0, 5))
        self.game_name_entry = Entry(left_frame, font=("Arial", 14), width=30)
        self.game_name_entry.pack(pady=(0, 15))
# Ratings (0-100)
        Label(left_frame, text="Ratings (0-100):", font=("Arial", 14),
              bg="#555555", fg="white").pack(anchor="w", pady=(0, 5))
        self.ratings_slider = Scale(left_frame, from_=0, to=100, orient=HORIZONTAL,
                                    bg="#444444", fg="white", length=300)
        self.ratings_slider.set(80)
        self.ratings_slider.pack(pady=(0, 15))
# Copies Sold
        Label(left_frame, text="Copies Sold (millions):", font=("Arial", 14),
              bg="#555555", fg="white").pack(anchor="w", pady=(0, 5))
        self.copies_entry = Entry(left_frame, font=("Arial", 14), width=30)
        self.copies_entry.insert(0, "5.0")
        self.copies_entry.pack(pady=(0, 15))
# Revenue
        Label(left_frame, text="Revenue ($ millions):", font=("Arial", 14),
              bg="#555555", fg="white").pack(anchor="w", pady=(0, 5))
        self.revenue_entry = Entry(left_frame, font=("Arial", 14), width=30)
        self.revenue_entry.insert(0, "200.0")
        self.revenue_entry.pack(pady=(0, 15))
# Narrative
        Label(left_frame, text="Narrative Quality (0-10):", font=("Arial", 14),
              bg="#555555", fg="white").pack(anchor="w", pady=(0, 5))
        self.narrative_slider = Scale(left_frame, from_=0, to=10, orient=HORIZONTAL,
                                      bg="#444444", fg="white", length=300)
        self.narrative_slider.set(7)
        self.narrative_slider.pack(pady=(0, 15))
# Innovation
        Label(left_frame, text="Innovation (0-10):", font=("Arial", 14),
              bg="#555555", fg="white").pack(anchor="w", pady=(0, 5))
        self.innovation_slider = Scale(left_frame, from_=0, to=10, orient=HORIZONTAL,
                                       bg="#444444", fg="white", length=300)
        self.innovation_slider.set(7)
        self.innovation_slider.pack(pady=(0, 15))
# Art Direction
        Label(left_frame, text="Art Direction (0-10):", font=("Arial", 14),
              bg="#555555", fg="white").pack(anchor="w", pady=(0, 5))
        self.art_slider = Scale(left_frame, from_=0, to=10, orient=HORIZONTAL,
                                bg="#444444", fg="white", length=300)
        self.art_slider.set(7)
        self.art_slider.pack(pady=(0, 15))
# Genre
        Label(left_frame, text="Genre:", font=("Arial", 14),
              bg="#555555", fg="white").pack(anchor="w", pady=(0, 5))
        genres = ["Action", "RPG", "Adventure", "Shooter", "Platformer", "Strategy",
                  "Simulation", "Sports", "Racing", "Fighting", "Action RPG", "Horror"]
        self.genre_var = StringVar(value="Action")
        genre_menu = OptionMenu(left_frame, self.genre_var, *genres)
        genre_menu.config(font=("Arial", 12), width=25)
        genre_menu.pack(pady=(0, 20))
# Result display area
        self.result_label = Label(right_frame, text="", font=("Arial", 16),
                                  bg="#555555", fg="white")
        self.result_label.pack(pady=5)
# Back button
        back_btn = Button(right_frame, text="← Back to Predictor Menu",
                          font=("Arial", 12), bg="#666666", fg="white",
                          command=self.open_predictor_screen)
        back_btn.pack(pady=10)
# Handles image uploading
    def uploadGameImage(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp")]
        filename = filedialog.askopenfilename(title="Select Game Image",
                                              filetypes=filetypes)
        if filename:
            try:
# Store the image path
                self.current_uploaded_image = filename
# Load and resize image
                original = Image.open(filename)
                resized = original.resize((500, 300))
                img = ImageTk.PhotoImage(resized)
# Update the image label
                self.game_image_label.config(image=img, text="")
                self.game_image_label.image = img  # Keep reference
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
# Function for running the prediction
    def runPrediction(self):
        try:
# Get values from inputs
            game_name = self.game_name_entry.get()
            ratings = self.ratings_slider.get()
            # Get and validate numeric inputs safely fields
            copies_text = self.copies_entry.get().strip().replace(",", "")
            revenue_text = self.revenue_entry.get().strip().replace(",", "")
            if copies_text == "":
                messagebox.showerror("Input Error", "Copies Sold field is empty.")
                return
            if revenue_text == "":
                messagebox.showerror("Input Error", "Revenue field is empty.")
                return
            try:
                copies_sold = float(copies_text)
            except:
                messagebox.showerror("Input Error", "Copies Sold must be a valid number.")
                return
            try:
                revenue = float(revenue_text)
            except:
                messagebox.showerror("Input Error", "Revenue must be a valid number.")
                return
            narrative = self.narrative_slider.get()
            innovation = self.innovation_slider.get()
            art_direction = self.art_slider.get()
            genre = self.genre_var.get()
# Validate inputs
            if not game_name.strip():
                messagebox.showerror("Input Error", "Please enter a game name.")
                return
            if copies_sold <= 0:
                messagebox.showerror("Input Error", "Copies sold must be greater than 0.")
                return
            if revenue <= 0:
                messagebox.showerror("Input Error", "Revenue must be greater than 0.")
                return
# Calculate revenue per copy
            revenue_per_copy = revenue / copies_sold if copies_sold > 0 else 0
# Calculate log transformations
            log_copies = np.log1p(copies_sold)
            log_revenue = np.log1p(revenue)
# Prepare features array
            numeric_features = [
                ratings,  # 1. Ratings
                revenue_per_copy,  # 2. Revenue_per_copy
                log_copies,  # 3. Log_Copies
                log_revenue,  # 4. Log_Revenue
                narrative,  # 5. Narrative_Quality
                art_direction,  # 6. Art_Direction
                innovation  # 7. Innovation
            ]
            all_possible_genres = ["Genre_Action", "Genre_Action RPG", "Genre_Action-Adventure",
            "Genre_Adventure", "Genre_Battle Royale", "Genre_Deck-building", "Genre_Life Simulation",
            "Genre_Music", "Genre_Platformer", "Genre_Puzzle", "Genre_RPG", "Genre_RTS", "Genre_Racing",
            "Genre_Roguelike", "Genre_Run and Gun", "Genre_Shooter", "Genre_Simulation", "Genre_Sports",
            "Genre_Survival", "Genre_Survival Horror", "Genre_Tactical Shooter", "Genre_VR Shooter"]
# Create genre features: 1 for selected genre, 0 for others
            genre_features = []
            for possible_genre in all_possible_genres:
# Extract genre name from encoded column name
# "Genre_Action RPG" -> "Action RPG"
                genre_name = possible_genre.replace("Genre_", "")
                if genre_name == genre:
                    genre_features.append(1.0)
                else:
                    genre_features.append(0.0)
            allFeatures = numeric_features + genre_features
# Add genre encoding
            prediction = self.ml_model.predict(allFeatures)
# Map prediction to readable result
            prediction_map = {2: "WINNER", 1: "NOMINEE", 0: "NOT NOMINATED"}
            result_text = prediction_map.get(prediction, "Unknown")
# Create result message
            if self.current_uploaded_image:
                img_status = "✓ Image uploaded"
            else:
                img_status = "⚠ No image uploaded"
            result_message = f"""
            PREDICTION RESULT for '{game_name}':
             Status: {result_text}
             Confidence: {(prediction / 2) * 100:.1f}%
            {img_status}
            Input Summary:
             Ratings: {ratings}/100
             Copies Sold: {copies_sold:.1f} million
             Revenue: ${revenue:.1f} million
             Narrative: {narrative}/10
             Innovation: {innovation}/10
             Art Direction: {art_direction}/10
             Genre: {genre}
            """
# Display result
            self.result_label.config(text=result_message)
            saved_image_path = self.saveGameImage(self.current_uploaded_image, game_name)
# If we have an image, display it in a separate window
            if self.current_uploaded_image:
                self.showPredictionResults(game_name, result_text, self.current_uploaded_image)
# After successful prediction, save to CSV
                self.savePredictionToCSV(
                    game_name=game_name,
                    ratings=ratings,
                    copies_sold=copies_sold,
                    revenue=revenue,
                    narrative=narrative,
                    innovation=innovation,
                    art_direction=art_direction,
                    genre=genre,
                    prediction=result_text,
                    confidence=(prediction / 2) * 100,
                    image=saved_image_path
                )
        except Exception as e:
            messagebox.showerror("Prediction Error", f"An error occurred: {str(e)}")

        except Exception as e:
            messagebox.showerror("Prediction Error", f"An error occurred: {str(e)}")
# Save the prediction on a csv file
    def savePredictionToCSV(self, game_name, ratings, copies_sold, revenue, narrative,
                            innovation, art_direction, genre, prediction, confidence, image=None):
        filename = "Prediction_History.csv"
        # Check if file exists to write headers
        file_exists = os.path.isfile(filename)
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            # Write header if new file
            if not file_exists:
                writer.writerow([
                    'game_name', 'ratings', 'copies_sold',
                    'revenue', 'narrative', 'innovation', 'art_direction',
                    'genre', 'prediction', 'confidence', 'image'
                ])
            writer.writerow([
                game_name,
                ratings,
                copies_sold,
                revenue,
                narrative,
                innovation,
                art_direction,
                genre,
                prediction,
                f"{confidence:.1f}",
                image if image else "No image"
            ])
    # Method for saving user game image
    def saveGameImage(self, image_path, game_name):
        """Save uploaded game image to Saved_game_images folder"""
        try:
# Create Saved_game_images folder if it doesn't exist
            save_folder = "Saved_game_images"
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
# Get file extension from original image
            file_extension = os.path.splitext(image_path)[1]
# Create safe filename from game name (remove special characters)
            safe_name = "".join(c for c in game_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
# Add timestamp to avoid overwriting
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_filename = f"{safe_name}_{timestamp}{file_extension}"
# Full path for saved image
            save_path = os.path.join(save_folder, new_filename)
# Copy image to saved folder
            shutil.copy2(image_path, save_path)
            return save_path
        except Exception as e:
            messagebox.showerror(f"Error saving image: {str(e)}")
            return None
# The prediction results
    def showPredictionResults(self, game_name, result, image_path):
        result_window = Toplevel(self.root)
        result_window.title(f"Prediction Result - {game_name}")
        result_window.geometry("800x600")
        result_window.configure(bg="#444444")
# Result header
        header = Label(result_window, text=f" {game_name}",
                       font=("Arial", 28, "bold"), bg="#444444", fg="white")
        header.pack(pady=20)
# Prediction status with color coding
        status_color = "#4CAF50" if "WINNER" in result else "#FF9800" if "NOMINEE" in result else "#F44336"
        status_label = Label(result_window, text=result, font=("Arial", 24, "bold"),
                             bg=status_color, fg="white", padx=20, pady=10)
        status_label.pack(pady=10)
# Display uploaded image
        try:
            original = Image.open(image_path)
            resized = original.resize((400, 250))
            img = ImageTk.PhotoImage(resized)
            img_label = Label(result_window, image=img, bg="#444444")
            img_label.image = img
            img_label.pack(pady=20)
        except:
            pass  # Skip image if there's an error
# Close button
        close_btn = Button(result_window, text="Close", font=("Arial", 14),
                           bg="#2196F3", fg="white", width=15,
                           command=result_window.destroy)
        close_btn.pack(pady=20)
# Placeholder functions for all predictions screens (to be implemented)
    def open_all_predictions(self):
        self.view.clear_screen()
        self.view.create_background("Back_ground_and_other_stuff/YES.png")
        print("Opening All Predictions...")
        # Back button to Predictor Menu
        back_btn = Button(self.root, text="← Back to Predictor Menu", font=("Arial", 12),
                          bg="#666666", fg="white", command=self.open_predictor_screen)
        back_btn.place(relx=0.95, rely=0.02, anchor="ne")
# Title
        title_label = Label(self.root, text="ALL PREDICTIONS",
                            font=("Arial", 32, "bold"), bg="#555555", fg="white")
        title_label.pack(pady=20)
# Main container (left & right)
        main_container = Frame(self.root, bg="#555555")
        main_container.pack(pady=10)
# LEFT SIDE – NOMINEES
        left_side = Frame(main_container, bg="#555555")
        left_side.pack(side=LEFT, padx=40)
        Label(left_side, text="NOMINEES", font=("Arial", 24, "bold"),
              bg="#555555", fg="gold").pack()
        left_scroll_container = Frame(left_side, bg="#555555")
        left_scroll_container.pack(pady=10)
        left_canvas = Canvas(left_scroll_container, width=450, height=600,
                             bg="#353E43", highlightthickness=0)
        left_canvas.pack(side=LEFT)
        left_slider = Scale(left_scroll_container, from_=0, to=500,
                            orient=VERTICAL, bg="#222222", fg="white", length=600)
        left_slider.pack(side=RIGHT, padx=10)
        left_frame = Frame(left_canvas, bg="#252525")
        left_canvas.create_window((0, 0), window=left_frame, anchor="nw")
        def update_left_scroll(pos):
            left_canvas.yview_moveto(int(pos) / 1000)
        left_slider.config(command=update_left_scroll)
# RIGHT SIDE – NOT NOMINATED
        right_side = Frame(main_container, bg="#555555")
        right_side.pack(side=RIGHT, padx=40)
        Label(right_side, text="NOT NOMINATED", font=("Arial", 24, "bold"),
              bg="#555555", fg="white").pack()
        right_scroll_container = Frame(right_side, bg="#555555")
        right_scroll_container.pack(pady=10)
        right_canvas = Canvas(right_scroll_container, width=450, height=600,
                              bg="#353E43", highlightthickness=0)
        right_canvas.pack(side=LEFT)
        right_slider = Scale(right_scroll_container, from_=0, to=500,
                             orient=VERTICAL, bg="#222222", fg="white", length=600)
        right_slider.pack(side=RIGHT, padx=10)
        right_frame = Frame(right_canvas, bg="#252525")
        right_canvas.create_window((0, 0), window=right_frame, anchor="nw")
        def update_right_scroll(pos):
            right_canvas.yview_moveto(int(pos) / 1000)
        right_slider.config(command=update_right_scroll)
# csv loader
        predictions = []
        if os.path.isfile("Prediction_History.csv"):
            with open("Prediction_History.csv", "r", newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    predictions.append(row)
# Keep references to images so Tkinter doesn't garbage collect them and delets my hard work
        self.image_refs_all_predictions = []
# sort to left or right frame
        for row in predictions:
            game_name = row["game_name"]
            prediction = row["prediction"]
            img_path = row["image"]
# Left = NOMINEE, Right = WINNER + NOT NOMINATED
            target = left_frame if "NOMINEE" in prediction else right_frame
# Container for each game
            box = Frame(target, bg="#353E43", padx=10, pady=10)
            box.pack(pady=10)
# Prediction status color
            color = "#4CAF50" if "WINNER" in prediction else \
                "#FF9800" if "NOMINEE" in prediction else "#F44336"
            Label(box, text=prediction, font=("Arial", 14, "bold"),
                  bg=color, fg="white", width=20).pack()
# Load game image
            try:
                original = Image.open(img_path)
                resized = original.resize((200, 120))
                tk_img = ImageTk.PhotoImage(resized)
            except:
                placeholder = Image.new("RGB", (200, 120), color="gray")
                tk_img = ImageTk.PhotoImage(placeholder)
# Keep reference so image doesn't disappear
            self.image_refs_all_predictions.append(tk_img)
            Label(box, image=tk_img, bg="#353E43").pack(pady=5)
            Label(box, text=game_name, font=("Arial", 14),
                  bg="#353E43", fg="white").pack()
# Update scroll region for BOTH sides
        left_frame.update_idletasks()
        right_frame.update_idletasks()
        left_canvas.config(scrollregion=left_canvas.bbox("all"))
        right_canvas.config(scrollregion=right_canvas.bbox("all"))
        left_canvas.config(scrollregion=left_canvas.bbox("all"))
        right_canvas.config(scrollregion=right_canvas.bbox("all"))
# Placeholder functions for graphs screens (to be implemented)
    def open_graphs_screen(self):
# This will show data visualizations
        try:
            df = load_goty_csv("GOTY(2005-2023).csv")
            G = build_similarity_graph_from_df(df)
            GraphWindow(self.root, df=df, G=G)
        except FileNotFoundError:
            messagebox.showerror("Error: Could not find GOTY(2005-2023).csv file")
        except Exception as e:
            messagebox.showerror(f"Error opening graphs: {e}")
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
            Label(win, text="What else do you want. there is no more.\n we are just bored",
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