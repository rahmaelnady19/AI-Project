# main.py
import tkinter as tk
from logic import AnimalStacker
from gui import AnimalStackerGUI

def main():
    game = AnimalStacker(num_animals=3)
    root = tk.Tk()
    app = AnimalStackerGUI(root, game)
    root.mainloop()

if __name__ == "__main__":
    main()
