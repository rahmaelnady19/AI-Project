# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import time
from logic import BFS, DFS, AStar, AnimalStacker

class AnimalStackerGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Animal Stacker - Smart AI Puzzle Game")
        self.root.geometry("1200x700")
        self.root.configure(bg="#462C7D") 
        self.animation_running = False
        
        # Colors for animals with special visibility
        self.colors = {
            1: "#f3e012",  # Yellow (Chick)
            2: "#039F44",  # Brown (Turtle)
            3: "#f36c12",  # Orange (Fox)
            4: '#FFF9C4',  # Light yellowish for Panda (more visible)
            5: "#5E7AC4"   # Blue (Elephant)
        }
        
        # Different sizes for different animals
        self.animal_sizes = {
            1: (60, 55),   # Chick (width, height) - smaller
            2: (90, 55),   # Turtle
            3: (120, 55),   # Fox
            4: (150, 55),   # Panda - larger
            5: (180, 55)   # Elephant - largest
        }
        
        self.peg_positions = [(200, 450), (600, 450), (1000, 450)]
        self.base_animal_height = 55
        self.base_animal_width = 80
        
        self.create_widgets()
        self.draw_state()
        
    def create_widgets(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg="#831C91") 
        title_frame.pack(pady=10, padx=20, fill='x')
        
        title = tk.Label(title_frame, text="🐘 Animal Stacker 🐥", 
                        font=('Arial', 20, 'bold'), bg='#831C91', fg='#FF70BF')
        title.pack(pady=10)
        
        # Success Message Label
        self.success_label = tk.Label(self.root, text="", 
                                     font=('Arial', 20, 'bold'), 
                                     bg='#462C7D', fg='#FCBF49')
        self.success_label.pack(pady=5)
        
        # Level Control Frame
        level_frame = tk.Frame(self.root, bg="#D552A3")  
        level_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(level_frame, text="Animals:", font=('Arial', 14, 'bold'), 
                bg='#D552A3', fg='#462C7D').pack(side='left', padx=10)
        
        self.down_btn = tk.Button(level_frame, text="▼", font=('Arial', 16, 'bold'),
                                  command=self.level_down, bg='#462C7D', fg='white',
                                  width=3, activebackground='#831C91')
        self.down_btn.pack(side='left', padx=5)
        
        self.level_var = tk.StringVar(value=f"{self.game.num_animals} Animals")
        self.level_label = tk.Label(level_frame, textvariable=self.level_var, 
                                   font=('Arial', 14, 'bold'), bg='#462C7D', 
                                   fg='#FF70BF', width=12)
        self.level_label.pack(side='left', padx=5)
        
        self.up_btn = tk.Button(level_frame, text="▲", font=('Arial', 16, 'bold'),
                                command=self.level_up, bg='#462C7D', fg='white',
                                width=3, activebackground='#831C91')
        self.up_btn.pack(side='left', padx=5)
        
        self.optimal_label = tk.Label(level_frame, text=f"🎯 Optimal Moves: {self.game.maximum_moves()}",
                                     font=('Arial', 12), bg='#D552A3', fg='white')
        self.optimal_label.pack(side='left', padx=20)
        
        # Goal info
        goal_label = tk.Label(level_frame, text="🎯 Goal: Move all animals to Peg 2", 
                             font=('Arial', 12), bg='#D552A3', fg='white')
        goal_label.pack(side='left', padx=20)
        
        # Algorithm Selection Frame
        algo_frame = tk.Frame(self.root, bg="#831C91")  
        algo_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(algo_frame, text="Algorithm:", font=('Arial', 14, 'bold'), 
                bg='#831C91', fg='#FF70BF').pack(side='left', padx=20)
        
        self.algorithm_var = tk.StringVar(value="BFS")
        self.algo_menu = ttk.Combobox(algo_frame, textvariable=self.algorithm_var, 
                                      values=["BFS", "DFS", "A*"], 
                                      state="readonly", width=15, font=('Arial', 12))
        self.algo_menu.pack(side='left', padx=10)
                     
        self.solve_btn = tk.Button(algo_frame, text="🎀 SOLVE", 
                                   command=self.solve_puzzle, 
                                   bg='#FF70BF', fg='#462C7D', 
                                   font=('Arial', 12, 'bold'), padx=30,
                                   activebackground='#D552A3', activeforeground='#462C7D')
        self.solve_btn.pack(side='left', padx=20)
        
        self.reset_btn = tk.Button(algo_frame, text="🔄 RESET", 
                                   command=self.reset_puzzle,
                                   bg='#FF70BF', fg='#462C7D', 
                                   font=('Arial', 12, 'bold'), padx=30,
                                   activebackground='#D552A3', activeforeground='#462C7D')
        self.reset_btn.pack(side='left', padx=10)
        
        # Stats Frame
        stats_frame = tk.Frame(self.root, bg="#462C7D")  
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        self.nodes_label = tk.Label(stats_frame, text="📊 Nodes Explored: 0", 
                                   font=('Arial', 12), bg='#462C7D', fg='#FF70BF')
        self.nodes_label.pack(side='left', padx=20)
        
        self.moves_label = tk.Label(stats_frame, text="🎯 Solution Length: 0", 
                                   font=('Arial', 12), bg='#462C7D', fg='#FF70BF')
        self.moves_label.pack(side='left', padx=20)
        
        self.time_label = tk.Label(stats_frame, text="⏳ Time: 0.00s", 
                                  font=('Arial', 12), bg='#462C7D', fg='#FF70BF')
        self.time_label.pack(side='left', padx=20)
        
        # Canvas Frame
        canvas_frame = tk.Frame(self.root, bg="#831C91")
        canvas_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(canvas_frame, width=1100, height=550, 
                               bg='#FF70BF', highlightthickness=2, highlightbackground='#D552A3')
        self.canvas.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Progress bar
        progress_frame = tk.Frame(self.root, bg="#462C7D")
        progress_frame.pack(pady=10, padx=20, fill='x')
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', length=600)
        self.progress.pack(pady=5)
        
        # Configure ttk style for progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", 
                       background='#FF70BF',
                       troughcolor='#D552A3',
                       bordercolor='#831C91',
                       lightcolor='#FF70BF',
                       darkcolor='#831C91')
        
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
            title_text = "🐘 Level 3: Turtle 🐢 | Fox 🦊 | Panda 🐼"
        elif animals_count == 4:
            title_text = "🐘 Level 4: Turtle 🐢 | Fox 🦊 | Panda 🐼 | Elephant 🐘"
        else:
            title_text = "🐘 Level 5: Chick 🐤 | Turtle 🐢 | Fox 🦊 | Panda 🐼 | Elephant 🐘"
            
        self.level_var.set(f"{animals_count} Animals")
        self.optimal_label.config(text=f"🎯 Optimal Moves: {self.game.maximum_moves()}")
        
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and child.cget('font') == ('Arial', 20, 'bold'):
                        child.config(text=f"🐘 ANIMAL STACKER - {title_text}")
                        break
    
    def clear_stats(self):
        self.nodes_label.config(text="📊 Nodes Explored: 0")
        self.moves_label.config(text="🎯 Solution Length: 0")
        self.time_label.config(text="⏱️ Time: 0.00s")
        self.progress['value'] = 0
        
    def draw_state(self):
        self.canvas.delete("all")
        
        # Draw pegs with labels
        for i, (x, y) in enumerate(self.peg_positions):
            # Peg pole
            self.canvas.create_line(x, y, x, y - 300, width=20, fill='#462C7D')
            # Peg base
            self.canvas.create_rectangle(x - 100, y, x + 100, y + 25, 
                                        fill='#831C91', outline='#D552A3', width=2)
            # Peg label
            self.canvas.create_text(x, y + 12, text=f"Peg {i}", 
                                   font=('Arial', 12, 'bold'), fill='#D552A3')
        
        # Draw animals on each peg
        for peg_idx, peg in enumerate(self.game.state):
            x, y = self.peg_positions[peg_idx]
            # Start from the bottom of the peg
            current_y = y
            
            # Draw animals in order (first in list = bottom, last = top)
            for animal in peg:
                # Get height for this animal
                _, height = self.animal_sizes.get(animal, (80, 60))
                y_pos = current_y - height
                self.draw_animal(x, y_pos, animal)
                current_y = y_pos  # Move up for the next animal
    
    def draw_animal(self, x, y, animal_type):
        color = self.colors.get(animal_type, '#95a5a6')
        icon = self.game.animal_icons.get(animal_type, "?")
        
        # Get size for this animal
        width, height = self.animal_sizes.get(animal_type, (80, 60))
        
        # Animal body with outline
        self.canvas.create_rectangle(x - width//2, y,
                                    x + width//2, y + height,
                                    fill=color, outline='#462C7D', width=3)
        
        # Animal icon with size adjustment
        font_size = 30
        if animal_type == 5:  # Elephant
            font_size = 36
        elif animal_type == 4:  # Panda
            font_size = 32
            
        self.canvas.create_text(x, y + height//2, 
                               text=icon, font=('Arial', font_size))
    
    def solve_puzzle(self):
        if self.animation_running:
            messagebox.showwarning("Warning", "Animation running! Press Reset first.")
            return 
            
        self.solve_btn.config(state='disabled')
        self.reset_btn.config(state='disabled')
        self.up_btn.config(state='disabled')
        self.down_btn.config(state='disabled')
        
        self.progress['value'] = 0
        self.success_label.config(text="")
        
        algorithm = self.algorithm_var.get()
        
        # Start timer before solving
        start_time = time.time()
        
        if algorithm == "BFS":
            solver = BFS(self.game)
            solution = solver.search()
            nodes = solver.nodes_explored
        elif algorithm == "DFS":
            depth_limit = self.game.maximum_moves() * 3
            solver = DFS(self.game, depth_limit=depth_limit)
            solution = solver.search()
            nodes = solver.nodes_explored
        else:  # A*
            solver = AStar(self.game, heuristic_choice="misplaced")
            solution = solver.search()
            nodes = solver.nodes_explored
        
        search_time = time.time() - start_time
        
        if solution:
            optimal = self.game.maximum_moves()
            solution_len = len(solution)
            
            # Store solution info for animation
            self.solution_info = {
                'nodes': nodes,
                'solution_len': solution_len,
                'optimal': optimal,
                'search_time': search_time
            }
            
            # Show search results immediately
            self.nodes_label.config(text=f"📊 Nodes Explored: {nodes}")
            self.moves_label.config(text=f"🎯 Solution Length: {solution_len}")
            self.time_label.config(text=f"⏱️ Search: {search_time:.3f}s (Animating...)")
            
            if solution_len == optimal:
                self.success_label.config(text="✅ SUCCESSFUL! 🎉", fg="#FFCA2A")
            else:
                self.success_label.config(text=f"✅ SUCCESSFUL! 🎉 ({solution_len} moves, optimal is {optimal})", fg='#FFCA2A')
            
            self.animate_solution(solution, search_time)
        else:
            self.success_label.config(text="❌ FAILED! No solution found", fg='#e74c3c')
            self.reset_buttons()
    
    def animate_solution(self, solution, search_time):
        self.animation_running = True
        animation_start = time.time()
        
        def make_move(index=0):
            if not self.animation_running or index >= len(solution):
                # Animation finished
                animation_time = time.time() - animation_start
                total_time = search_time + animation_time
                
                self.animation_running = False
                self.progress['value'] = 100
                self.time_label.config(text=f"⏱️ Search: {search_time:.3f}s | Total: {total_time:.3f}s")
                self.reset_buttons()
                return
            
            from_peg, to_peg = solution[index]
            new_state = self.game.step(self.game.state, from_peg, to_peg)
            if new_state:
                self.game.state = new_state
                self.draw_state()
                self.progress['value'] = (index + 1) / len(solution) * 100
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


if __name__ == "__main__":
    root = tk.Tk()
    game_logic = AnimalStacker(num_animals=3)
    app = AnimalStackerGUI(root, game_logic)
    root.mainloop()