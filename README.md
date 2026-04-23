# Animal StackerSolver with AI Search

![Language](https://img.shields.io/badge/Language-Python-blue)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)

## 📋 Project Description
This project is a GUI-based implementation of the classic problem using animals. The program solves the puzzle using three different search algorithms and visualizes the solution step-by-step.The goal is to move all animals from the first peg (Peg0) to the last peg (Peg2) following the rule: **a larger animal cannot be placed on top of a smaller one**.

## 🎯 Algorithms Implemented
1. **BFS (Breadth-First Search)**: Uses a Queue to guarantee the shortest path/solution.
2. **DFS (Depth-First Search)**: Uses a Stack with a depth limit. Faster but does not guarantee an optimal solution.
3. **A Star Search**: Uses a Priority Queue with `f(n) = g(n) + h(n)` to find the optimal solution efficiently.
   - **Heuristic- Misplaced**: Counts animals not on the goal peg.

## ▶️ Demo Video
A explaining the project and showing the GUI in action:  
**https://drive.google.com/file/d/1boudfWAIaMwDAJ4S5txIGCTlMSupe89w/view?usp=drive_link**

## 📄 Project Report
For detailed analysis and results, see the full report:  
**https://drive.google.com/file/d/14G-H3ufIJGVdwfrPKhh2M9U_8PJkkL1v/view?usp=drive_link**

## 🖼️ Screenshot
**https://drive.google.com/file/d/1rQlaahWHl1BQ5ldQKswK77qsrNA_w9C6/view?usp=drive_link**

## 🚀 How to Run Locally
1. **Prerequisites**: Make sure you have Python 3.8+ installed.
2. **Clone the repository**:
   ```bash
   git clone https://github.com/Rahma/AI Project.git
   cd AI Project Run the application:bash   python animal_stacker.py   Note: Tkinter is included with standard Python installations. No extra packages needed.Use the GUI:Select the number of animals (3-5 recommended).Choose a search algorithm.Click Solve to generate the solution.Use Next Move or Play Animation to visualize the steps.📊 Performance Comparison
Example results for 4 animals:Algorithm Moves Found Nodes Explored Optimal Solution? Time Complexity BFS15∼1020 Yes High DFS 150+∼200 No Low A Violations15∼50YesLowConclusion: A_ with the Violations heuristic provides the optimal solution while exploring the fewest nodes, making it the most efficient for this problem.🧠 AI Concepts Used
Agent Type: Model-Based, Goal-Based, Utility-Based (for A_)Problem-Solving Framework: Classical SearchState Space Search: The program explores the state space of all possible peg configurations.Heuristic Design: Demonstrates how an informed heuristic drastically improves search efficiency.

👩‍💻 Author
Rahma
CS Department, 
Mansoura University Course: Artificial Intelligence
This project was developed as part of the AI course requirements.
