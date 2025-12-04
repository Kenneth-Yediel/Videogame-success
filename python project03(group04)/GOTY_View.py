# View.py - Pure UI components for the Game Selector application
from tkinter import *
from PIL import Image, ImageTk
# Create game view class
class GameView:
    def __init__(self, root):
# Main application window
        self.root = root
        self.root.title("Game Selector")
        self.root.geometry("1500x1000")
        self.root.configure(bg="#555555")
# Store images to prevent garbage collection
        self.images = {}
# Deletes all widgets from the window
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
# Creates a settings menu (dropdown)
    def create_settings_menu(self):
        settings_button = Menubutton(self.root, text="Settings", relief=RAISED)
# Create menu object and attach it to the button
        settings_button.menu = Menu(settings_button, tearoff=0)
        settings_button["menu"] = settings_button.menu
# Add menu options
        settings_button.menu.add_command(label="Help")
        settings_button.menu.add_command(label="Credits")
        settings_button.menu.add_command(label="More")
        settings_button.menu.add_command(label="Dance")
        settings_button.menu.add_separator()
# Exit option closes the entire app
        settings_button.menu.add_command(label="Exit", command=self.root.quit)
# Position menu
        settings_button.place(x=10, y=10)
        return settings_button
# Sets a background image
    def create_background(self, image_path):
        bg = PhotoImage(file=image_path)
        self.images["bg"] = bg  # Store reference to avoid garbage collection
        background_label = Label(self.root, image=bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        return background_label
# Creates a general-purpose label
    def create_label(self, text, font=("Arial", 14), bg="#555555", fg="white", **kwargs):
        label = Label(self.root, text=text, font=font, bg=bg, fg=fg, **kwargs)
        return label
# Creates a title label at the top of the screen
    def create_title(self, text, font_size=40, pady=80):
        title = Label(self.root, text=text, font=("Arial", font_size), bg="#555555", fg="white")
        title.pack(pady=pady)
        return title
# Creates a general-purpose button
    def create_button(self, text, command, font_size=20, width=20, pady=10, pack=True):
        btn = Button(self.root, text=text, font=("Arial", font_size), width=width, command=command)
# Optionally pack the button if desired
        if pack:
            btn.pack(pady=pady)
        return btn
# Creates a button using an image (game icon)
    def create_game_button(self, image_path, title, command):
        try:
# Load and resize image
            original = Image.open(image_path)
            resized = original.resize((150, 150))
            button_img = ImageTk.PhotoImage(resized)
        except:
    # Fallback placeholder if the image fails to load
            placeholder = Image.new("RGB", (150, 150), color="gray")
            button_img = ImageTk.PhotoImage(placeholder)
# Create button with the image
        btn = Button(self.root, image=button_img, command=command, bg="#555555", borderwidth=2, highlightthickness=0)
# Store reference so the image doesn't disappear
        btn.image = button_img
        return btn
# Creates only the image for a game button (without the button widget)
    def create_game_button_image(self, image_path, size=(150, 150)):
        try:
            original = Image.open(image_path)
            resized = original.resize(size)
            button_img = ImageTk.PhotoImage(resized)
            return button_img
        except:
            placeholder = Image.new("RGB", size, color="gray")
            button_img = ImageTk.PhotoImage(placeholder)
            return button_img
# Creates a scrollable container for game listings
    def create_scrollable_container(self, width=1000, height=600):
# Outer frame
        container = Frame(self.root, bg="#555555")
        container.pack()
# Scroll canvas
        canvas = Canvas(container, width=width, height=height, bg="#555555", highlightthickness=0)
        canvas.pack(side=LEFT)
# Manual scroll slider (not scrollbar)
        scroll_slider = Scale(container, from_=0, to=500, orient=VERTICAL, bg="#222222", fg="white", length=height)
        scroll_slider.pack(side=RIGHT, padx=10)
# Frame where buttons will be placed
        button_frame = Frame(canvas, bg="#555555")
# Insert button frame into the canvas
        canvas.create_window((0, 0), window=button_frame, anchor="nw")
        return container, canvas, scroll_slider, button_frame
# Creates a pop-up window displaying game details
    def create_game_detail_window(self, image_path, title, description):
        scene = Toplevel(self.root)
        scene.title(title)
        scene.geometry("1500x1000")
        scene.configure(bg="#555555")
        return scene
# Creates a general pop-up window
    def create_toplevel(self, title, geometry):
        toplevel = Toplevel(self.root)
        toplevel.title(title)
        toplevel.geometry(geometry)
        toplevel.configure(bg="#444444")
        return toplevel
# Creates a frame container
    def create_frame(self, bg="#555555"):
        frame = Frame(self.root, bg=bg)
        return frame
# Creates a menubutton widget (without menu items)
    def create_menubutton(self, text):
        menubutton = Menubutton(self.root, text=text, relief=RAISED)
        return menubutton
# Creates a menu and attaches it to a menubutton
    def create_menu(self, menubutton):
        menu = Menu(menubutton, tearoff=0)
        menubutton["menu"] = menu
        return menu
# Creates a canvas widget for drawing or scrolling
    def create_canvas(self, width, height, bg="#555555"):
        canvas = Canvas(self.root, width=width, height=height, bg=bg, highlightthickness=0)
        return canvas
# Creates a scale widget (slider) for scrolling or value selection
    def create_scale(self, from_, to, orient=VERTICAL, length=600):
        scale = Scale(self.root, from_=from_, to=to, orient=orient, bg="#222222", fg="white", length=length)
        return scale
# Creates a label with an image (for displaying game screenshots)
    def create_image_label(self, image_path, size=None):
        try:
            original = Image.open(image_path)
            if size:
                resized = original.resize(size)
            else:
                resized = original.copy()
                resized.thumbnail((650, 450))
            img = ImageTk.PhotoImage(resized)
            label = Label(self.root, image=img, bg="#555555")
            label.image = img
            return label
        except:
            return None
# Creates a text entry widget for user input
    def create_entry(self, **kwargs):
        entry = Entry(self.root, **kwargs)
        return entry