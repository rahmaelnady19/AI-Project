# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import time
from logic import BFS, DFS, AStar, AnimalStacker

class AnimalStackerGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Animal Stacker - Smart AI Game")
        self.root.geometry("1200x700")
        self.root.configure(bg="#462C7D") 
        self.animation_running = False
        
        # Colors for animals 
        self.colors = {
            1: "#f3e012",  # Yellow 
            2: "#039F44",  # Green 
            3: "#f36c12",  # Orange 
            4: '#FFF9C4',  # Light yello
            5: "#5E7AC4"   # Blue 
        }
        
        # Different sizes for animals
        self.animal_sizes = {
            1: (60, 55),    # Chick (width, height) 
            2: (90, 55),    # Turtle
            3: (120, 55),   # Fox
            4: (150, 55),   # Panda 
            5: (180, 55)    # Elephant 
        }
        
        # Peg positions on canvas
        self.peg_positions = [(200, 450), (600, 450), (1000, 450)]

        # Base dimensions for animals (used for scaling)
        self.base_animal_height = 55
        self.base_animal_width = 80
        
        # Create all GUI widgets
        self.create_widgets()
        self.draw_state()
        
    def create_widgets(self):
        # Frame
        title = tk.Frame(self.root, bg="#831C91") 
        title.pack(pady=10, padx=20, fill='x')

        # Title of the game        
        title = tk.Label(title, text="🐘 Animal Stacker 🐥", font=('Arial', 20, 'bold'), bg='#831C91', fg='#FF70BF')
        title.pack(pady=10)
        
        # Success Message Label
        self.success_label = tk.Label(self.root, text="", font=('Arial', 20, 'bold'),  bg='#462C7D', fg='#FCBF49')
        self.success_label.pack(pady=5)
        
        # Level Control
        level = tk.Frame(self.root, bg="#D552A3")  
        level.pack(pady=10, padx=20, fill='x')
        
        tk.Label(level, text="Animals:", font=('Arial', 14, 'bold'), bg='#D552A3', fg='white').pack(side='left', padx=10)
        
        self.down_btn = tk.Button(level, text="▼", font=('Arial', 16, 'bold'), command=self.level_down, bg='#462C7D', fg='#FF70BF', width=3, activebackground='#831C91')
        self.down_btn.pack(side='left', padx=5)
        
        self.level_var = tk.StringVar(value=f"{self.game.num_animals}")
        self.level_label = tk.Label(level, textvariable=self.level_var, font=('Arial', 14, 'bold'), bg='#462C7D', fg='#FF70BF', width=7)
        self.level_label.pack(side='left', padx=5)
        
        self.up_btn = tk.Button(level, text="▲", font=('Arial', 16, 'bold'), command=self.level_up, bg='#462C7D', fg='#FF70BF', width=3, activebackground='#831C91')
        self.up_btn.pack(side='left', padx=5)
        
        self.optimal = tk.Label(level, text=f"🎯 Optimal Moves: {self.game.maximum_moves()}", font=('Arial', 12), bg='#D552A3', fg='white')
        self.optimal.pack(side='left', padx=20)
        
        # Goal info
        goal = tk.Label(level, text="🎯 Goal: Move all animals to Peg 2", font=('Arial', 12), bg='#D552A3', fg='white')
        goal.pack(side='left', padx=20)
        
        # Algorithm Selection Frame
        algo = tk.Frame(self.root, bg="#831C91")  
        algo.pack(pady=10, padx=20, fill='x')
        
        tk.Label(algo, text="Algorithm:", font=('Arial', 14, 'bold'), bg='#831C91', fg='#FF70BF').pack(side='left', padx=20)
        
        self.algorithm_var = tk.StringVar(value="BFS")
        self.algo_menu = ttk.Combobox(algo, textvariable=self.algorithm_var, values=["BFS", "DFS", "A*"], state="readonly", width=15, font=('Arial', 12))
        self.algo_menu.pack(side='left', padx=10)
                     
        self.solve_btn = tk.Button(algo, text="🎀 SOLVE", command=self.solve_puzzle, bg='#FF70BF', fg='#462C7D', font=('Arial', 12, 'bold'), padx=30, activebackground='#D552A3', activeforeground='#462C7D')
        self.solve_btn.pack(side='left', padx=20)
        
        self.reset_btn = tk.Button(algo, text="🔄 RESET", command=self.reset_puzzle, bg='#FF70BF', fg='#462C7D', font=('Arial', 12, 'bold'), padx=30, activebackground='#D552A3', activeforeground='#462C7D')
        self.reset_btn.pack(side='left', padx=10)
        
        # Stats
        stats = tk.Frame(self.root, bg="#462C7D")  
        stats.pack(pady=10, padx=20, fill='x')
        
        self.nodes = tk.Label(stats, text="📊 Nodes Explored: 0", font=('Arial', 12), bg='#462C7D', fg='#FF70BF')
        self.nodes.pack(side='left', padx=20)
        
        self.moves = tk.Label(stats, text="🎯 Solution Length: 0", font=('Arial', 12), bg='#462C7D', fg='#FF70BF')
        self.moves.pack(side='left', padx=20)
        
        self.time = tk.Label(stats, text="⏳ Time: 0.00s", font=('Arial', 12), bg='#462C7D', fg='#FF70BF')
        self.time.pack(side='left', padx=20)
        
        # Canvas Frame
        canvas = tk.Frame(self.root, bg="#831C91")
        canvas.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(canvas, width=1100, height=550, bg='#FF70BF', highlightthickness=2, highlightbackground='#D552A3')
        self.canvas.pack(pady=10, padx=10, fill='both', expand=True)
        
    def on_algorithm_change(self, event=None):
        if self.algorithm_var.get() == "A*":
            self.heuristic_menu.config(state='readonly')
        else:
            self.heuristic_menu.config(state='disabled')
    
    def level_up(self):
        if self.animation_running:
            return
        new_level = self.game.num_animals + 1
        if new_level <= 5:
            self.game.set_level(new_level)
            self.update_level_display()
            self.draw_state()
            self.clear_stats()
            self.success_label.config(text="")
            
    def level_down(self):
        if self.animation_running:
            return
        new_level = self.game.num_animals - 1
        if new_level >= 3:
            self.game.set_level(new_level)
            self.update_level_display()
            self.draw_state()
            self.clear_stats()
            self.success_label.config(text="")
    
    def update_level_display(self):
        animals_count = self.game.num_animals
        if animals_count == 3:
            title_text = "🐘 Level 3: Cat 🐱 | Fox 🦊 | Panda 🐼"
        elif animals_count == 4:
            title_text = "🐘 Level 4: Cat 🐱 | Fox 🦊 | Panda 🐼 | Elephant 🐘"
        else:
            title_text = "🐘 Level 5: Chick 🐤 | Cat 🐱 | Fox 🦊 | Panda 🐼 | Elephant 🐘"
            
        self.level_var.set(f"{animals_count}")
        self.optimal.config(text=f"🎯 Optimal Moves: {self.game.maximum_moves()}")
        
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and child.cget('font') == ('Arial', 20, 'bold'):
                        child.config(text=f"🐘 ANIMAL STACKER - {title_text}")
                        break
    
    def clear_stats(self):
        self.nodes.config(text="📊 Nodes Explored: 0")
        self.moves.config(text="🎯 Solution Length: 0")
        self.time.config(text="⏱️ Time: 0.00s")
        
    def draw_state(self):
        self.canvas.delete("all")
        
        # Draw pegs with labels
        for i, (x, y) in enumerate(self.peg_positions):
            self.canvas.create_line(x, y, x, y - 300, width=20, fill='#462C7D')
            self.canvas.create_rectangle(x - 100, y, x + 100, y + 25, fill='#831C91', outline='#D552A3', width=2)
            self.canvas.create_text(x, y + 12, text=f"Peg {i}", font=('Arial', 12, 'bold'), fill='#D552A3')
        
        # Draw animals on each peg
        for peg_idx, peg in enumerate(self.game.state):
            x, y = self.peg_positions[peg_idx]

            # Start from the bottom of the peg
            current_y = y
            
            # Draw animals in order from bottom to top
            for animal in peg:
                y_pos = current_y - 60
                self.draw_animal(x, y_pos, animal)
                # Move up for the next animal
                current_y = y_pos 
    
    def draw_animal(self, x, y, animal_type):
        color = self.colors.get(animal_type, '#95a5a6')
        icon = self.game.animal_icons.get(animal_type, "?")
        
        # Get size for this animal
        width, height = self.animal_sizes.get(animal_type, (80, 60))
        
        # Adjust position to maintain bottom alignment
        y_top = y
        
        # Animal body with outline
        self.canvas.create_rectangle(x - width//2, y_top,
                                    x + width//2, y_top + height,
                                    fill=color, outline='#462C7D', width=3)
         # Animal name
        font_size = 30
        if animal_type == 5:  # Elephant
            font_size = 36
        elif animal_type == 4:  # Panda
            font_size = 32
        self.canvas.create_text(x, y_top + height//2, 
                               text=icon, font=('Arial', font_size))
    
    def solve_puzzle(self):

        self.solve_btn.config(state='disabled')
        self.reset_btn.config(state='disabled')
        self.up_btn.config(state='disabled')
        self.down_btn.config(state='disabled')
        
        self.success_label.config(text="")    
        algorithm = self.algorithm_var.get()
        
        # Start timer before solving
        start_time = time.time()

        # Solve using the selected algorithm
        if algorithm == "BFS":
            solver = BFS(self.game)
            solution = solver.search()
            nodes = solver.nodes_explored
        elif algorithm == "DFS":
            depth_limit = self.game.maximum_moves() * 3
            solver = DFS(self.game)
            solution = solver.search()
            nodes = solver.nodes_explored
        else:  # A*
            solver = AStar(self.game)
            solution = solver.search()
            nodes = solver.nodes_explored
        
        search_time = time.time() - start_time
        
        if solution:
            optimal = self.game.maximum_moves()
            cost = len(solution)
            
            # Store solution info for animation
            self.solution_info = {
                'nodes': nodes,
                'solution_len': cost,
                'optimal': optimal,
                'search_time': search_time
            }
            
            if cost == optimal:
                self.success_label.config(text="✅ SUCCESSFUL! 🎉", fg="#FFCA2A")
            else:
                self.success_label.config(text=f"✅ SUCCESSFUL! 🎉 ({cost} moves, optimal is {optimal})", fg='#FFCA2A')
            
            self.animate_solution(solution, search_time)
        else:
            self.success_label.config(text="❌ FAILED! No solution found", fg='#e74c3c')
            self.reset_buttons()   

        # Show search results 
        self.nodes.config(text=f"📊 Nodes Explored: {nodes}")
        self.moves.config(text=f"🎯 Solution Length: {cost}")
        self.time.config(text=f"⏱️ Search: {search_time:.3f}s")         
    
    def animate_solution(self, solution, search_time):
        self.animation_running = True    
        def make_move(index=0):
            if not self.animation_running or index >= len(solution):  
                self.animation_running = False
                self.time.config(text=f"⏱️ Search: {search_time:.3f}s")
                self.reset_buttons()
                return
            
            from_peg, to_peg = solution[index]
            new_state = self.game.step(self.game.state, from_peg, to_peg)
            if new_state:
                self.game.state = new_state
                self.draw_state()
                self.root.update()
            
            self.root.after(1200, lambda: make_move(index + 1))
        
        make_move()
    
    def reset_buttons(self):
        self.solve_btn.config(state='normal')
        self.reset_btn.config(state='normal')
        self.up_btn.config(state='normal')
        self.down_btn.config(state='normal')
    
    def reset_puzzle(self):
        if self.animation_running:
            self.animation_running = False
            
        self.game.reset_state()
        self.draw_state()
        self.clear_stats()
        self.reset_buttons()
        self.success_label.config(text="")    
