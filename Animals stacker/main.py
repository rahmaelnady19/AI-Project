# main.py
import tkinter as tk
from logic import AnimalStacker
from gui import AnimalStackerGUI

def main():
    rules = AnimalStacker(num_animals=3)

    root = tk.Tk()
    game = AnimalStackerGUI(root, rules)
    
    
    root.mainloop()

if __name__ == "__main__":
    main()