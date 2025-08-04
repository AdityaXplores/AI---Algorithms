import tkinter as tk
from tkinter import messagebox
import heapq
import random

goal_state = "123456780"  # '0' is blank tile

def get_neighbors(state):
    neighbors = []
    zero = state.index('0')
    row, col = zero // 3, zero % 3
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in moves:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_pos = nr * 3 + nc
            new_state = list(state)
            new_state[zero], new_state[new_pos] = new_state[new_pos], new_state[zero]
            neighbors.append("".join(new_state))
    return neighbors

def heuristic(state):
    dist = 0
    for i, c in enumerate(state):
        if c == '0': continue
        val = int(c) - 1
        dist += abs(i // 3 - val // 3) + abs(i % 3 - val % 3)
    return dist

def is_solvable(state):
    inv = 0
    tiles = [c for c in state if c != '0']
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inv += 1
    return inv % 2 == 0

def astar(start):
    heap = [(heuristic(start), 0, start, [])]
    visited = set()
    while heap:
        est, cost, current, path = heapq.heappop(heap)
        if current == goal_state:
            return path + [current]
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                heapq.heappush(heap, (cost + 1 + heuristic(neighbor), cost + 1, neighbor, path + [current]))
    return None

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Solver (A*)")
        self.tiles = []
        self.board = "".join(random.sample("123456780", 9))
        while not is_solvable(self.board):
            self.board = "".join(random.sample("123456780", 9))
        self.create_ui()
        self.draw_board(self.board)

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(3):
            row = []
            for j in range(3):
                b = tk.Button(frame, text='', font=('Helvetica', 24), width=4, height=2)
                b.grid(row=i, column=j, padx=5, pady=5)
                row.append(b)
            self.tiles.append(row)

        solve_btn = tk.Button(self.root, text="Solve with A*", command=self.solve)
        solve_btn.pack(pady=10)

    def draw_board(self, state):
        for i in range(3):
            for j in range(3):
                val = state[i * 3 + j]
                self.tiles[i][j].config(text='' if val == '0' else val)

    def solve(self):
        solution = astar(self.board)
        if not solution:
            messagebox.showerror("Unsolvable", "This puzzle can't be solved.")
            return
        self.animate(solution)

    def animate(self, steps):
        def step(i):
            if i < len(steps):
                self.draw_board(steps[i])
                self.root.after(500, step, i + 1)
        step(0)

# Start GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
