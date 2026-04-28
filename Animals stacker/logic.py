# logic.py
import heapq
import itertools
from copy import deepcopy
from collections import deque

class AnimalStacker:
    def __init__(self, num_animals = 3):
        self.animal_icons = {
            1: "🐥",
            2: "🐢",
            3: "🦊",
            4: "🐼",
            5: "🐘"
        }
        self.num_animals = num_animals
        self.reset_state()

    def get_orders(self):
        return list(range(self.num_animals, 0, -1))

    def reset_state(self):
        animals = self.get_orders()
        self.state = [
            animals,
            [],
            []
        ]
        self.goal_state = [
            [],
            [],
            self.get_orders()
        ]

    def set_level(self, num_animals):
        self.num_animals = num_animals
        self.reset_state()

    def maximum_moves(self):
        return (2 ** self.num_animals) - 1

    def is_valid_move(self, state, from_peg, to_peg):
        if not state[from_peg]:
            return False
        if not state[to_peg]:
            return True
        top_from = state[from_peg][-1]
        top_to = state[to_peg][-1]
        return top_from < top_to

    def step(self, state, from_peg, to_peg):
        if not self.is_valid_move(state, from_peg, to_peg):
            return None
        new_state = deepcopy(state)
        animal = new_state[from_peg].pop()
        new_state[to_peg].append(animal)
        return new_state

    def actions(self, state):
        moves = []
        for from_peg in range(3):
            for to_peg in range(3):
                if from_peg!= to_peg:
                    if self.is_valid_move(state, from_peg, to_peg):
                        moves.append((from_peg, to_peg))
        return moves

    def is_goal_state(self, state):
        return state == self.goal_state

    def heuristic(self, state):
        misplaced = 0
        for i in range(3):
            if i!= 2:
                misplaced += len(state[i])
        return misplaced

    def get_state_key(self, state):
        return tuple(tuple(peg) for peg in state)

class BFS:
    def __init__(self, game):
        self.game = game
        self.nodes_explored = 0
        self.solution_path = []

    def search(self):
        start_state = self.game.state
        start_key = self.game.get_state_key(start_state)

        queue = deque([(start_state, [])])
        visited = set()

        while queue:
            current_state, path = queue.popleft()
            self.nodes_explored += 1

            if self.game.is_goal_state(current_state):
                self.solution_path = path
                return path

            for from_peg, to_peg in self.game.actions(current_state):
                new_state = self.game.step(current_state, from_peg, to_peg)
                if new_state:
                    new_key = self.game.get_state_key(new_state)
                    if new_key not in visited:
                        visited.add(new_key)
                        queue.append((new_state, path + [(from_peg, to_peg)]))
        return None

class DFS:
    def __init__(self, game, depth_limit=100):
        self.game = game
        self.nodes_explored = 0
        self.solution_path = []
        self.depth_limit = depth_limit

    def search(self):
        start_state = self.game.state
        start_key = self.game.get_state_key(start_state)

        stack = [(start_state, [], 0, {start_key})]

        while stack:
            current_state, path, depth, visited = stack.pop()
            self.nodes_explored += 1

            if self.game.is_goal_state(current_state):
                self.solution_path = path
                return path

            if depth >= self.depth_limit:
                continue

            for from_peg, to_peg in self.game.actions(current_state):
                new_state = self.game.step(current_state, from_peg, to_peg)
                if new_state:
                    new_key = self.game.get_state_key(new_state)
                    if new_key not in visited:
                        new_visited = visited.copy()
                        new_visited.add(new_key)
                        stack.append((new_state, path + [(from_peg, to_peg)], depth + 1, new_visited))
        return None

class AStar:
    def __init__(self, game, heuristic_name="misplaced"):  
        self.game = game
        self.nodes_explored = 0
        self.solution_path = []
        self.heuristic_name = heuristic_name

    def heuristic(self, state):
        return self.game.heuristic(state)

    def search(self):
        start_state = self.game.state
        start_key = self.game.get_state_key(start_state)

        counter = itertools.count()
        heap = []
        heapq.heappush(heap, (self.heuristic(start_state), next(counter), start_state, [], 0))
        
        g_costs = {start_key: 0}
        visited = set()

        while heap:
            f_cost, _, current_state, path, g_cost = heapq.heappop(heap)
            current_key = self.game.get_state_key(current_state)

            if current_key in visited:
                continue

            visited.add(current_key)
            self.nodes_explored += 1

            if self.game.is_goal_state(current_state):
                self.solution_path = path
                return path

            for from_peg, to_peg in self.game.actions(current_state):
                new_state = self.game.step(current_state, from_peg, to_peg)
                if new_state:
                    new_key = self.game.get_state_key(new_state)
                    new_g_cost = g_cost + 1

                    if new_key not in g_costs or new_g_cost < g_costs[new_key]:
                        g_costs[new_key] = new_g_cost
                        new_f_cost = new_g_cost + self.heuristic(new_state)
                        heapq.heappush(heap, (new_f_cost, next(counter), new_state, path + [(from_peg, to_peg)], new_g_cost))
        return None
