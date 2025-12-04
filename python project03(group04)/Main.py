# Main.py
from tkinter import *
from GOTY_Controller import GameController
if __name__ == "__main__":
    root = Tk()
    app = GameController(root)
    app.run()